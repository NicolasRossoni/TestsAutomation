"""
Classe que gerencia a navegação na página principal da plataforma.

Responsabilidades:
- Trocar entre organizações
- Navegar entre áreas da plataforma
- Aguardar carregamento de elementos
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from core import auxiliar as aux
from core.auxiliar import logger
from time import sleep
from selenium.common.exceptions import TimeoutException

# Classe para manipular a página principal da web
class Web:
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
                logger.debug("ℹ️ Ambiente Web carregado!")
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