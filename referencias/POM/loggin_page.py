from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "user")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login")

    def preencher_usuario(self, usuario):
        self.driver.find_element(*self.username_input).send_keys(usuario)

    def preencher_senha(self, senha):
        self.driver.find_element(*self.password_input).send_keys(senha)

    def clicar_login(self):
        self.driver.find_element(*self.login_button).click()

    def aguardar_pagina_carregar(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.login_button)
        )