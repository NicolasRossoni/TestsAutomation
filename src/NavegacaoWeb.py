"""
================================================================================
--- Este arquivo implementa testes automatizados para verificar a navegação
    entre diferentes áreas da plataforma, utilizando Selenium WebDriver e o 
    padrão Page Object Model.

--- Estrutura principal:
    1. TestNavegacaoWeb: Classe de teste que herda de unittest.TestCase e contém:
       - setUp(): Configura o ambiente de teste e faz login na plataforma
       - test_entrar_mapa(): Testa a navegação para a área de mapas
       - test_entrar_backoffice(): Testa a navegação para o backoffice
       - test_entrar_workspaces(): Testa a navegação para a área de workspaces
       - test_entrar_dashboards(): Testa a navegação para a área de dashboards
       - tearDown(): Fecha o navegador após cada teste

--- Cada teste verifica se a URL após a navegação contém o texto esperado,
    garantindo que o redirecionamento para a área correta foi realizado com sucesso.
================================================================================
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
import unittest
import core.Pages as Pages
import core.auxiliar as aux
from core.auxiliar import logger


# Classe de teste para o fluxo de login e criação de assinaturas
class TestSuit(unittest.TestCase):
    # Método executado antes de cada teste para configurar o ambiente
    def setUp(self):
        logger.debug("🛠️ Configurando ambiente para o teste")

        # Configura as opções do navegador Chrome
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--start-maximized")
        self.service = Service("../drivers/chromedriver")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        # Acessa a URL da plataforma
        self.driver.get("https://platform.ecotx.dev/")
        
        # Inicializa as páginas que serão utilizadas nos testes
        self.login_page = Pages.LoginPage(self.driver)
        self.web_page = Pages.MainWebPage(self.driver)

        # Efetua login na plataforma
        self.login_page.preencher_usuario("nicolas.o.rossoni@gmail.com")
        self.login_page.preencher_senha("123456")
        self.login_page.clicar_login()
        self.login_page.aguardar_carregar()
        
        # Troca para org com todos os acessos
        self.web_page.trocar_org("Vigilant")
    
    def test_entrar_mapa(self): 
        #Faz o teste
        self.web_page.trocar_area("mapa")
        
        # Verifica se deu certo
        self.assertIn("maps", self.driver.current_url, "URL do incorreta")
        logger.info(f"✅ URL verificada com sucesso: {self.driver.current_url}")
    
    def test_entrar_backoffice(self):
        #Faz o teste
        self.web_page.trocar_area("Backoffice")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        # Verifica se deu certo
        self.assertIn("backoffice", self.driver.current_url, "URL do incorreta")
        logger.info(f"✅ URL verificada com sucesso: {self.driver.current_url}")
    
    def test_entrar_workspaces(self):
        #Faz o teste
        self.web_page.trocar_area("workspaces")
        
        # Verifica se deu certo
        self.assertIn("workspaces", self.driver.current_url, "URL do incorreta")
        logger.info(f"✅ URL verificada com sucesso: {self.driver.current_url}")
    
    def test_entrar_dashboards(self):
        #Faz o teste
        self.web_page.trocar_area("dashboards")
        
        # Verifica se deu certo
        self.assertIn("dashboards", self.driver.current_url, "URL do incorreta")
        logger.info(f"✅ URL verificada com sucesso: {self.driver.current_url}")
    
    # Método executado após cada teste para limpar o ambiente
    def tearDown(self):
        self.driver.quit()
        logger.debug("🔄 Ambiente zerado após o teste.")

if __name__ == "__main__":
    unittest.main()

# Para rodar e gerar relatório:
# pytest NavegacaoWeb.py -n auto --html=core/TestSuit_report.html