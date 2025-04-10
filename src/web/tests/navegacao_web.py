"""
Testes automatizados de navegação entre áreas da plataforma.

Testa a navegação entre as diferentes áreas:
- Mapa
- Backoffice
- Workspaces
- Dashboards

Cada teste verifica se a URL após a navegação contém o texto esperado.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
import unittest
import src.web.pages as WebPages
import src.backoffice.pages as BackofficePages
import src.workspace.pages as WorkspacePages
import src.core.utils as utils
from src.core.utils import logger


# Classe de teste para o fluxo de navegação entre áreas da plataforma
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
        self.login_page = WebPages.Login(self.driver)
        self.web_page = WebPages.Web(self.driver)

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
# pytest src/web/tests/navegacao_web.py -n auto --html=src/core/report.html