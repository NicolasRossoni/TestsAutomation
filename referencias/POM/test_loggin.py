import unittest
from selenium import webdriver
from loggin_page import LoginPage  # Importando a classe do POM

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://exemplo.com/login")
        self.login_page = LoginPage(self.driver)

    def test_login_valido(self):
        self.login_page.aguardar_pagina_carregar()
        self.login_page.preencher_usuario("meu_usuario")
        self.login_page.preencher_senha("minha_senha")
        self.login_page.clicar_login()

        # Verificar se o login foi bem-sucedido (exemplo: checando a URL)
        self.assertIn("dashboard", self.driver.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()