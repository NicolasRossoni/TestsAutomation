"""
Classe que gerencia as interações com a página de login.

Responsabilidades:
- Preencher campos de login
- Submeter o formulário
- Aguardar carregamento após login
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from core import auxiliar as aux
from core.auxiliar import logger
from time import sleep
from random import randint
from selenium.common.exceptions import TimeoutException

# Classe para manipular a página de login
class Login:
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