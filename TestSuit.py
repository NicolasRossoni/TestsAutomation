"""
================================================================================
--- Este arquivo implementa testes automatizados para o fluxo de criação de assinaturas
    na plataforma, utilizando Selenium WebDriver e o padrão Page Object Model.

--- Estrutura principal:
    1. TestLogin: Classe de teste que herda de unittest.TestCase e contém:
       - setUp(): Configura o ambiente de teste, faz login e navega até a área de criação
       - verificar_criacao_assinatura(): Método central que cria e verifica assinaturas
       - test_venda_mais_sem_asaas(): Teste específico para criação sem integração Asaas
       - tearDown(): Limpa o ambiente após cada teste

--- O teste monitora as requisições HTTP para verificar se a criação foi bem-sucedida,
    buscando por chamadas à API que contenham 'subscription' na URL.

--- Outros testes comentados ao final permitem verificar diferentes tipos de assinatura
    (Standard, Profissional) e diferentes configurações (com/sem integração Asaas).
================================================================================
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from auxiliar import logger
from time import sleep, time
import unittest
import Pages
import json
from pprint import pprint

# Lista de assinaturas disponíveis no sistema
nomes_de_assinaturas = ["Venda+", "Standard", "Professional", "Chile", "Portugal", "Telecom"]

# Classe de teste para o fluxo de login e criação de assinaturas
class TestLogin(unittest.TestCase):
    # Método executado antes de cada teste para configurar o ambiente
    def setUp(self):
        logger.debug("🛠️ Configurando ambiente para o teste")

        # Configura as opções do navegador Chrome
        self.options = Options()
        #self.options.add_argument("--headless")
        self.options.add_argument("--start-maximized")
        self.service = Service("drivers/chromedriver")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        # Acessa a URL da plataforma
        self.driver.get("https://platform.ecotx.dev/")
        
        # Inicializa as páginas que serão utilizadas nos testes
        self.login_page = Pages.LoginPage(self.driver)
        self.web_page = Pages.MainWebPage(self.driver)
        self.backoffice = Pages.Backoffice(self.driver)
        self.backoffice_criar_assinatura = Pages.BackofficeCriarAssinatura(self.driver)

        # Efetua login na plataforma
        self.login_page.preencher_usuario("nicolas.o.rossoni@gmail.com")
        self.login_page.preencher_senha("123456")
        self.login_page.clicar_login()
        self.login_page.aguardar_carregar()
        
        # Navega até a área de criação de assinaturas no backoffice
        self.web_page.trocar_org("Vigilant")
        self.web_page.trocar_area("Backoffice")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.backoffice.aguardar_carregar() 
        self.backoffice.trocar_area("Gerenciamento de Assinaturas")
        self.backoffice.trocar_sub_area("Criar nova assinatura")

    # Método para verificar a criação de uma assinatura
    def verificar_criacao_assinatura(self, tipo_assinatura, com_asaas):
        max_wait_time = 120
        start_time = time()
        
        # Cria a assinatura para um usuário existente
        acessos, cobrança_no_asaas, chave_da_assinatura = self.backoffice_criar_assinatura.criar_assinatura_usuario_existente(tipo_assinatura, com_asaas)
        
        # Verifica se a requisição foi bem sucedida dentro do tempo limite
        while time() - start_time < max_wait_time:
            # Percorre todas as requisições feitas pelo navegador
            for request in self.driver.requests:
                # Verifica se é uma requisição relacionada a assinaturas e se tem resposta
                if 'subscription' in request.url and request.response:
                    # Verifica se a resposta não foi bem sucedida (status diferente de 200)
                    if request.response.status_code != 200:
                        logger.error(f"❌ Erro: A requisição teve status {request.response.status_code}")
                        print("\n=== RESPOSTA DA API ===")
                        pprint(json.loads(request.response.body.decode('utf-8')))  # Exibe formatado de forma legível
                        print("======================\n")
                        self.fail(f"Erro na requisição para {tipo_assinatura}: Status {request.response.status_code}")
                        
                    logger.info(f"✅ Assinatura criada para o acesso '{acessos}' com cobrança no Asaas[{cobrança_no_asaas}] e chave = {chave_da_assinatura}.")
                    return
            sleep(2)  
        
        # Se o tempo expirar sem encontrar a requisição esperada, o teste falha
        self.fail(f"Timeout: Nenhuma requisição para subscription foi detectada em {max_wait_time} segundos")
    
    """
    # Teste para criar assinatura do tipo Venda+, Standard e Profissional sem integração com Asaas
    def test_venda_mais_sem_asaas(self):
        self.verificar_criacao_assinatura("Venda+", False)

    def test_standard_sem_asaas(self):
        self.verificar_criacao_assinatura("Standard", False)
        
    def test_professional_sem_asaas(self):
        self.verificar_criacao_assinatura("Professional", False)
    """
    
    # Teste para criar assinatura do tipo Venda+, Standard e Profissional com integração com Asaas
    def test_venda_mais_com_asaas(self):
        self.verificar_criacao_assinatura("Venda+", True)
        
    """   
    def test_standard_com_asaas(self):
        self.verificar_criacao_assinatura("Standard", True)
        
    def test_professional_com_asaas(self):
        self.verificar_criacao_assinatura("Professional", True)
    """
    
    # Método executado após cada teste para limpar o ambiente
    def tearDown(self):
        self.driver.quit()
        logger.debug("🔄 Ambiente zerado após o teste.")

if __name__ == "__main__":
    unittest.main()

# Para rodar e gerar relatório:
# pytest TestSuit.py -n auto --html=TestSuit_report.html