"""
Testes automatizados para criação de assinaturas na plataforma.

Funcionalidades:
- Criação de assinaturas de diferentes tipos (Venda+, Standard, Professional)
- Suporte a usuários novos e existentes
- Opções com e sem integração com Asaas
"""
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
import unittest
import src.web.pages as WebPages
import src.backoffice.pages as BackofficePages
import src.workspace.pages as WorkspacePages
import src.core.utils as utils
from src.core.utils import logger

# Lista de assinaturas disponíveis no sistema
nomes_de_assinaturas = ["Venda+", "Standard", "Professional", "Chile", "Portugal", "Telecom"]

# Classe de teste para o fluxo de login e criação de assinaturas
class TestSuit(unittest.TestCase):
    # Método executado antes de cada teste para configurar o ambiente
    def setUp(self):
        logger.debug("🛠️ Configurando ambiente para o teste")

        # Configura as opções do navegador Chrome
        self.options = Options()
        #self.options.add_argument("--headless")
        self.options.add_argument("--start-maximized")
        self.service = Service("resources/drivers/chromedriver")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        # Acessa a URL da plataforma
        self.driver.get("https://platform.ecotx.dev/")
        
        # Inicializa as páginas que serão utilizadas nos testes
        self.login_page = Pages.Login(self.driver)
        self.web_page = Pages.Web(self.driver)
        self.backoffice = Pages.Backoffice(self.driver)
        self.backoffice_criar_assinatura = Pages.CriarAssinatura(self.driver)

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

    # Método para criar uma assinatura
    def criar_assinatura(self, tipo_assinatura, com_asaas, tipo_usuario):
        acessos, cobrança_no_asaas, chave_da_assinatura = self.backoffice_criar_assinatura.criar_assinatura(tipo_assinatura, com_asaas, tipo_usuario)
        status = utils.verifica_chamada_api(self.driver, "subscription")
        if status:
            logger.info(f"✅ Assinatura criada para o acesso '{acessos}' com cobrança no Asaas[{cobrança_no_asaas}], chave = {chave_da_assinatura} e usuario {tipo_usuario}.")
        else:
            self.fail(f"A requisição para a API falhou, para o acesso '{acessos}' com Asaas[{cobrança_no_asaas}] e usuario {tipo_usuario}.")
    
    """
    # Teste para criar assinatura do tipo Venda+, Standard e Profissional sem integração com Asaas
    def test_venda_mais_sem_asaas(self):
        self.criar_assinatura("Venda+", False)
        
    def test_standard_sem_asaas(self):
        self.criar_assinatura("Standard", False)
        
    def test_professional_sem_asaas(self):
        self.criar_assinatura("Professional", False)
    
    # Teste para criar assinatura do tipo Venda+, Standard e Profissional com integração com Asaas
    def test_venda_mais_com_asaas(self):
        self.criar_assinatura("Venda+", True)
        
      
    def test_standard_com_asaas(self):
        self.criar_assinatura("Standard", True)
        
    def test_professional_com_asaas(self):
        self.criar_assinatura("Professional", True)
    """
    
    def test_venda_mais_sem_asaas_novo_usuario(self):
        self.criar_assinatura("Venda+", False, "novo")
        
    
    # Método executado após cada teste para limpar o ambiente
    def tearDown(self):
        self.driver.quit()
        logger.debug("🔄 Ambiente zerado após o teste.")

if __name__ == "__main__":
    unittest.main()

# Para rodar e gerar relatório:
# pytest src/backoffice/tests/assinaturas.py -n auto --html=src/core/report.html

