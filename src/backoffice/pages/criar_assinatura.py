"""
Classe que gerencia o fluxo de criação de assinaturas.

Responsabilidades:
- Criar assinaturas para usuários existentes ou novos
- Preencher campos do formulário de assinatura
- Configurar integrações e enviar o formulário
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import src.core.utils as utils
from src.core.utils import logger
from time import sleep
from random import randint

# Classe para manipular a criação de assinaturas no backoffice
class CriarAssinatura:
    def __init__(self, driver):
        self.driver = driver
        self.tipo_usuario_existente = (By.XPATH, '//*[@id="inlineRadio1"]')
        self.tipo_novo_usuario = (By.XPATH, '//input[@id="inlineRadio2"]')
        self.selecione_usuario_existente = (By.XPATH, "/html[1]/body[1]/app-layout[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/app-subscriptions-management[1]/app-create-new-subscription[1]/div[1]/div[2]/div[1]/div[2]/div[1]/form[1]/div[2]/div[1]/ng-select[1]/div[1]/div[1]/div[3]/input[1]")
        self.email_novo_usuario = (By.XPATH, "/html[1]/body[1]/app-layout[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/app-subscriptions-management[1]/app-create-new-subscription[1]/div[1]/div[2]/div[1]/div[2]/div[1]/form[1]/div[2]/div[1]/input[1]")
        self.selecione_assinatura = (By.XPATH, "/html[1]/body[1]/app-layout[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/app-subscriptions-management[1]/app-create-new-subscription[1]/div[1]/div[2]/div[1]/div[2]/div[1]/form[1]/div[3]/div[1]/ng-select[1]/div[1]/div[1]/div[3]/input[1]")
        self.campo_acessos = (By.XPATH, "/html/body/app-layout/div/div/div/div/div/div/app-subscriptions-management/app-create-new-subscription/div/div[2]/div/div[2]/div[1]/form/div[4]/div[2]/input")
        self.campo_preco = (By.XPATH, "/html[1]/body[1]/app-layout[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/app-subscriptions-management[1]/app-create-new-subscription[1]/div[1]/div[2]/div[1]/div[2]/div[1]/form[1]/div[5]/div[1]/input[1]")
        self.flag_asaas = (By.XPATH, "/html/body/app-layout/div/div/div/div/div/div/app-subscriptions-management/app-create-new-subscription/div/div[2]/div/div[2]/div[1]/form/div[9]/div/span/label")
        self.concluir_assinatura = (By.XPATH, "/html[1]/body[1]/app-layout[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/app-subscriptions-management[1]/app-create-new-subscription[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/button[1]")
        self.confirmar_assinatura = (By.XPATH, "/html[1]/body[1]/app-layout[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/app-subscriptions-management[1]/app-create-new-subscription[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/button[1]")
        
    # Método para criar uma assinatura para um usuário existente
    def criar_assinatura(self, assinatura, cobrança_no_asaas, type):
        chave_da_assinatura = randint(10, 99) # "Chave" da assinatura(2 digitos aleatorios)
        
        # Dados da assinatura
        self.new_user = "nicolas.o.rossoni@usp.br"
        self.user = "nicolas.rossoni@datlaz.com"
        self.org = "TesteNicolas"
        
        self.cpf = "10017074940"
        self.name = "SeleniumBot" + str(chave_da_assinatura)
        self.email = "SeleniumBot" + str(chave_da_assinatura) + "@gmail.com"
        self.telefone = "41999900" + str(chave_da_assinatura)
        
        self.data_validade = ["01", "01", "2026"]
        self.preco = str(chave_da_assinatura) + "000"
        
        if type == "existente":
            # Preenche o campo de usuário
            campo_usuario = utils.find_element(self.driver, self.selecione_usuario_existente)
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
            sleep(10)
            self.driver.switch_to.active_element.send_keys(Keys.ENTER)
            self.driver.switch_to.active_element.send_keys(Keys.TAB)
            
            self.driver.switch_to.active_element.send_keys(Keys.ENTER)
            logger.debug("ℹ️ Usuário e Organização já existentes selecionados.")

        elif type == "novo":
            utils.find_element(self.driver, self.tipo_novo_usuario).click()
            campo_email = utils.find_element(self.driver, self.email_novo_usuario)
            campo_email.send_keys(self.new_user)
            self.driver.switch_to.active_element.send_keys(Keys.TAB)
            self.driver.switch_to.active_element.send_keys(self.cpf)
            self.driver.switch_to.active_element.send_keys(Keys.TAB)
            self.driver.switch_to.active_element.send_keys(self.name)
            self.driver.switch_to.active_element.send_keys(Keys.TAB)
            self.driver.switch_to.active_element.send_keys(self.telefone)
            self.driver.switch_to.active_element.send_keys(Keys.TAB)
            self.driver.switch_to.active_element.send_keys(Keys.ENTER)
            logger.debug("ℹ️ Dados do novo usuário preenchidos.")
        
        else:
            logger.error("❌ Erro: Tipo de usuário inválido.")
            raise
        
        # Preenche o resto dos dados da assinatura
        acessos = self.preencher_assinatura(assinatura, cobrança_no_asaas, chave_da_assinatura)
        
        # Retorna informações sobre a assinatura criada
        return acessos, cobrança_no_asaas, chave_da_assinatura
        
    def preencher_assinatura(self, assinatura, cobrança_no_asaas, chave_da_assinatura):
        # Preenche o campo de assinatura
        campo_assinatura = utils.find_element(self.driver, self.selecione_assinatura)
        campo_assinatura.send_keys(assinatura[:2])
        sleep(3)
        campo_assinatura.send_keys(assinatura[2:])
        sleep(5)
        campo_assinatura.send_keys(Keys.ENTER)
        campo_assinatura.send_keys(Keys.TAB)

        # Preenche o campo de data de validade
        self.driver.switch_to.active_element.send_keys(self.data_validade[0])
        self.driver.switch_to.active_element.send_keys(self.data_validade[1])
        self.driver.switch_to.active_element.send_keys(self.data_validade[2])
        
        # Salvando os acessos para retornar no final
        campo_acessos = utils.find_element(self.driver, self.campo_acessos)
        acessos = campo_acessos.get_attribute('value')
        campo_acessos.send_keys(Keys.TAB)
        
        # Preenche os campos de preço
        campo_preco = utils.find_element(self.driver, self.campo_preco)
        campo_preco.send_keys(self.preco)
        campo_preco.send_keys(Keys.TAB)
        
        # Preenche os dados de cobrança (nome, email, CPF e telefone)
        self.driver.switch_to.active_element.send_keys(self.name)
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        self.driver.switch_to.active_element.send_keys(self.email)
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        self.driver.switch_to.active_element.send_keys(self.cpf)
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        self.driver.switch_to.active_element.send_keys(self.telefone)
        
        # Desativa a integração com ASAAS se necessário
        if not cobrança_no_asaas:
            sleep(2)
            utils.find_element(self.driver, self.flag_asaas).click()
        
        # Clica no botão para concluir a criação da assinatura
        sleep(2)    
        utils.find_element(self.driver, self.concluir_assinatura).click()
                
        # Confirma a criação da assinatura
        sleep(2)
        utils.find_element(self.driver, self.confirmar_assinatura).click()
        
        return acessos 