"""
================================================================================
--- Este arquivo implementa o padrão Page Object Model para automação da plataforma,
    definindo classes que representam cada uma das páginas e componentes da interface.

--- Estrutura principal:
    1. LoginPage: Manipula a página de login e autenticação
    2. MainWebPage: Manipula a navegação da página principal (troca de org, área)
    3. Backoffice: Manipula a página de backoffice e navegação entre suas áreas
    4. BackofficeCriarAssinatura: Manipula o formulário de criação de assinaturas

--- Cada classe encapsula os seletores (XPath) dos elementos da interface e 
    implementa métodos que simulam as ações do usuário (cliques, preenchimento
    de campos, navegação), abstraindo as complexidades da interação com o Selenium.

--- O BackofficeCriarAssinatura implementa o fluxo completo de criação de assinaturas,
    desde a seleção do tipo de usuário até a confirmação final, com suporte a diferentes
    configurações (com/sem integração Asaas, diferentes tipos de assinatura).
================================================================================
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import auxiliar as aux
from auxiliar import logger
from time import sleep
from random import randint
from selenium.common.exceptions import TimeoutException
        
# Classe para manipular a página de login
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.XPATH, "//input[@id='username']")
        self.password_input = (By.XPATH, "//input[@id='password']")
        self.submit_button = (By.XPATH, "//button[@id='kt_sign_in_submit']")
        self.splash_screen = (By.XPATH, '//*[@id="splash-screen"]')

    # Método para preencher o campo de usuário
    def preencher_usuario(self, usuario):
        aux.find_element(self.driver, self.username_input).send_keys(usuario)

    # Método para preencher o campo de senha
    def preencher_senha(self, senha):
        aux.find_element(self.driver, self.password_input).send_keys(senha)

    # Método para clicar no botão de login
    def clicar_login(self):
        aux.find_element(self.driver, self.submit_button).click()
    
    # Método para aguardar o carregamento da página após o login
    def aguardar_carregar(self):
        for tentativa in range(3):
            try:
                aux.wait_for_element(self.driver, self.splash_screen)
                logger.debug("ℹ️ Login efetuado e ambiente Web carregado!")
                return
            except TimeoutException:
                if tentativa < 2:
                    logger.debug(f"⚠️ Tentativa {tentativa + 1}: Recarregando a página...")
                    self.driver.refresh()
                else:
                    logger.error("❌ Erro: Página não carregou após 3 tentativas de refresh")
                    raise

# Classe para manipular a página principal da web
class MainWebPage:
    def __init__(self, driver):
        self.driver = driver
        self.org_button = (By.XPATH, "/html/body/app-layout/div/app-main-side-menu/div/div/div[2]/div[1]/ul/app-menu-item")
        self.org_list = (By.XPATH, "/html/body/app-layout/div/app-org-sub-menu-item/div/div/div[3]")
        self.areas_lsit = (By.XPATH, "/html/body/app-layout/div/app-main-side-menu/div/div/div[2]/div[1]/ul")
        self.splash_screen = (By.XPATH, '//*[@id="splash-screen"]')
    
    # Método para trocar de organização
    def trocar_org(self, org_name):
        aux.find_element(self.driver, self.org_button).click()
        org_list = aux.find_element(self.driver, self.org_list)
        
        aux.find_element_in_element(org_list, org_name).click()
        logger.debug(f"ℹ️ Organização trocada para: {org_name}.")
                
        self.aguardar_carregar()
    
    # Método para aguardar o carregamento da página após a troca de organização
    def aguardar_carregar(self):
        for tentativa in range(3):
            try:
                aux.wait_for_element(self.driver, self.splash_screen)
                logger.debug("ℹ️ Login efetuado e ambiente Web carregado!")
                return
            except TimeoutException:
                if tentativa < 2:
                    logger.debug(f"⚠️ Tentativa {tentativa + 1}: Recarregando a página...")
                    self.driver.refresh()
                else:
                    logger.error("❌ Erro: Página não carregou após 3 tentativas de refresh")
                    raise

    # Método para trocar de área na plataforma
    def trocar_area(self, area):
        areas_list = aux.find_element(self.driver, self.areas_lsit)
        aux.find_element_in_element(areas_list, area).click()
        logger.debug(f"ℹ️ Area trocada para: {area}.")

# Classe para manipular a área de backoffice
class Backoffice:
    def __init__(self, driver):
        self.driver = driver
        self.active_area = None
        self.areas_lsit = (By.XPATH, '/html/body/app-layout/div/div/app-aside/div[2]/div/ul')
        self.splash_screen = (By.XPATH, '/html/body/app-splash-screen')
    
    # Método para aguardar o carregamento do backoffice
    def aguardar_carregar(self):
        for tentativa in range(3):
            try:
                aux.wait_for_element(self.driver, self.splash_screen)
                logger.debug("ℹ️ Login efetuado e ambiente Backoffice carregado!")
                return
            except TimeoutException:
                if tentativa < 2:
                    logger.debug(f"⚠️ Tentativa {tentativa + 1}: Recarregando a página...")
                    self.driver.refresh()
                else:
                    logger.error("❌ Erro: Página não carregou após 3 tentativas de refresh")
                    raise
    
    # Método para trocar de área no backoffice
    def trocar_area(self, area):
        areas_list = aux.find_element(self.driver, self.areas_lsit)
        self.active_area = aux.find_element_in_element(areas_list, area)
        self.active_area.click()
        logger.debug(f"ℹ️ Area trocada para: {area}.")
    
    # Método para trocar para uma sub-área dentro da área atual
    def trocar_sub_area(self, sub_area):
        aux.find_element_in_element(self.active_area, sub_area).click()
        logger.debug(f"ℹ️ Sub-area trocada para: {sub_area}.")
    
# Classe para manipular a criação de assinaturas no backoffice
class BackofficeCriarAssinatura:
    def __init__(self, driver):
        self.driver = driver
        self.tipo_usuario_existente = (By.XPATH, '//*[@id="inlineRadio1"]')
        self.tipo_novo_usuario = (By.XPATH, '//input[@id="inlineRadio2"]')
        self.selecione_usuario_existente = (By.XPATH, "/html[1]/body[1]/app-layout[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/app-subscriptions-management[1]/app-create-new-subscription[1]/div[1]/div[2]/div[1]/div[2]/div[1]/form[1]/div[2]/div[1]/ng-select[1]/div[1]/div[1]/div[3]/input[1]")
        self.selecione_assinatura = (By.XPATH, "/html[1]/body[1]/app-layout[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/app-subscriptions-management[1]/app-create-new-subscription[1]/div[1]/div[2]/div[1]/div[2]/div[1]/form[1]/div[3]/div[1]/ng-select[1]/div[1]/div[1]/div[3]/input[1]")
        self.campo_acessos = (By.XPATH, "/html/body/app-layout/div/div/div/div/div/div/app-subscriptions-management/app-create-new-subscription/div/div[2]/div/div[2]/div[1]/form/div[4]/div[2]/input")
        self.campo_preco = (By.XPATH, "/html[1]/body[1]/app-layout[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/app-subscriptions-management[1]/app-create-new-subscription[1]/div[1]/div[2]/div[1]/div[2]/div[1]/form[1]/div[5]/div[1]/input[1]")
        self.flag_asaas = (By.XPATH, "/html/body/app-layout/div/div/div/div/div/div/app-subscriptions-management/app-create-new-subscription/div/div[2]/div/div[2]/div[1]/form/div[9]/div/span/label")
        self.concluir_assinatura = (By.XPATH, "/html[1]/body[1]/app-layout[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/app-subscriptions-management[1]/app-create-new-subscription[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/button[1]")
        self.confirmar_assinatura = (By.XPATH, "/html[1]/body[1]/app-layout[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/app-subscriptions-management[1]/app-create-new-subscription[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/button[1]")
        self.user = "nicolas.rossoni@datlaz.com"
        self.org = "TesteSegments"
    
    # Método para criar uma assinatura para um usuário existente
    def criar_assinatura_usuario_existente(self, assinatura, cobrança_no_asaas):
        # Gera uma chave aleatória para identificar a assinatura
        chave_da_assinatura = randint(10, 99)
        
        # Clica no radio button de usuário existente
        aux.find_element(self.driver, self.tipo_usuario_existente).click()

        # Preenche o campo de usuário
        campo_usuario = aux.find_element(self.driver, self.selecione_usuario_existente)
        campo_usuario.send_keys(self.user[:5])
        sleep(3)
        campo_usuario.send_keys(self.user[5:])
        sleep(5)
        campo_usuario.send_keys(Keys.ENTER)
        campo_usuario.send_keys(Keys.TAB)

        # Preenche o campo de organização
        self.driver.switch_to.active_element.send_keys(self.org[:5])
        sleep(3)
        self.driver.switch_to.active_element.send_keys(self.org[5:])
        sleep(5)
        self.driver.switch_to.active_element.send_keys(Keys.ENTER)
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        
        self.driver.switch_to.active_element.send_keys(Keys.ENTER)
        logger.debug("ℹ️ Usuário e Organização selecionados.")
        
        # Preenche o campo de assinatura
        campo_assinatura = aux.find_element(self.driver, self.selecione_assinatura)
        campo_assinatura.send_keys(assinatura[:2])
        sleep(3)
        campo_assinatura.send_keys(assinatura[2:])
        sleep(5)
        campo_assinatura.send_keys(Keys.ENTER)
        campo_assinatura.send_keys(Keys.TAB)

        # Preenche o campo de data de validade
        self.driver.switch_to.active_element.send_keys("01")
        self.driver.switch_to.active_element.send_keys("01")
        self.driver.switch_to.active_element.send_keys("2026")
        
        # Salvando os acessos para retornar no final
        campo_acessos = aux.find_element(self.driver, self.campo_acessos)
        acessos = campo_acessos.get_attribute('value')
        campo_acessos.send_keys(Keys.TAB)
        
        # Preenche os campos de preço
        campo_preco = aux.find_element(self.driver, self.campo_preco)
        campo_preco.send_keys(str(chave_da_assinatura)+"000")
        campo_preco.send_keys(Keys.TAB)
        
        # Preenche os dados de cobrança (nome, email, CPF e telefone)
        self.driver.switch_to.active_element.send_keys("SeleniumBot" + str(chave_da_assinatura))
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        self.driver.switch_to.active_element.send_keys("SeleniumBot" + str(chave_da_assinatura) + "@gmail.com")
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        self.driver.switch_to.active_element.send_keys("10017074940")
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        self.driver.switch_to.active_element.send_keys("41" + "9999" + "00" + str(chave_da_assinatura))
        
        # Desativa a integração com ASAAS se necessário
        if not cobrança_no_asaas:
            sleep(2)
            aux.find_element(self.driver, self.flag_asaas).click()
        
        # Clica no botão para concluir a criação da assinatura
        sleep(2)    
        aux.find_element(self.driver, self.concluir_assinatura).click()
                
        # Confirma a criação da assinatura
        sleep(2)
        aux.find_element(self.driver, self.confirmar_assinatura).click()
        
        # Registra a conclusão da criação da assinatura
        logger.debug(f"ℹ️ Assinatura preenchida para o acesso '{acessos}' com cobrança no Asaas[{cobrança_no_asaas}] e chave = {chave_da_assinatura}.")
        
        # Retorna informações sobre a assinatura criada
        return acessos, cobrança_no_asaas, chave_da_assinatura

        