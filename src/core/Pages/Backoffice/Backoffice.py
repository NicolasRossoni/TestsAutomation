"""
Classe que gerencia a navegação na área de backoffice.

Responsabilidades:
- Aguardar carregamento da página
- Navegar entre áreas do backoffice
- Navegar entre sub-áreas específicas
"""
from selenium.webdriver.common.by import By
from core import auxiliar as aux
from core.auxiliar import logger
from time import sleep
from selenium.common.exceptions import TimeoutException

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