"""
================================================================================
--- Este arquivo fornece funções auxiliares para os testes de automação,
    encapsulando operações comuns do Selenium WebDriver e configurações de logging.

--- Estrutura principal:
    1. Funções de interação com elementos da interface:
       - find_element: Localiza um elemento na página com timeout
       - wait_for_element: Aguarda um elemento desaparecer da página
       - find_element_in_element: Busca um elemento dentro de outro elemento

    2. Configuração do sistema de logging:
       - Configuração do logger para registrar informações no arquivo TestSuit.log
       - Formatação das mensagens com timestamp e níveis de log (DEBUG, INFO, ERROR)

--- Estas funções auxiliares são utilizadas pelos arquivos Pages.py e TestSuit.py
    para simplificar o código de automação, reduzir duplicação e melhorar a
    legibilidade ao centralizar a lógica de espera e tratamento de exceções.
================================================================================
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging
from time import sleep

# Função que espera elemento aparecer e retorna o elemento
def find_element(driver, path, tempo=120):
    try:
        element = WebDriverWait(driver, tempo).until(
        EC.presence_of_element_located(path)
        )
        return element

    except TimeoutException:
        logger.error(f"❌ Erro: O elemento não apareceu dentro de {tempo} segundos. -> Elemento:{path}")
        raise
    
# Função que espera elemento desaparecer e retorna True
def wait_for_element(driver, path, tempo=120):
    try:
        WebDriverWait(driver, tempo).until(
        EC.invisibility_of_element_located(path)
        )
        return True

    except TimeoutException:
        logger.error(f"❌ Erro: O elemento não desapareceu dentro de {tempo} segundos. -> Elemento:{path}")
        raise

# Função que encontra um elemento dentro de um elemento pai
def find_element_in_element(elemento_pai, texto_busca, tentativas=10):
    for tentativa in range(tentativas):
        for element in elemento_pai.find_elements(By.XPATH, ".//*"):
            if texto_busca.lower() in element.text.strip().lower():
                return element
        logger.debug(f"⚠️ Tentativa {tentativa + 1}: O elemento de texto {texto_busca}, não apareceu na seleção.")
        sleep(3)
    
    logger.error(f"❌ Erro: O elemento de texto {texto_busca}, não apareceu na seleção.") 
    raise

# Configuração do logger
logger = logging.getLogger("MeuLogger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Handler para o arquivo de log
file_handler = logging.FileHandler("fluxo_assinatura/TestSuit.log", mode="w")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
