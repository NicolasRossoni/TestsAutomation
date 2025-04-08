"""
Funções auxiliares para automação de testes com Selenium.

Funcionalidades:
- Interação com elementos da interface (busca, espera)
- Verificação de chamadas API
- Configuração de logging para os testes
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging
from time import sleep, time
import pprint
import json

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

# Função que verifica se a requisição foi bem sucedida
def verifica_chamada_api(driver, url, max_wait_time=120):
    start_time = time()
    
    # Verifica se a requisição foi bem sucedida dentro do tempo limite
    while time() - start_time < max_wait_time:
        # Percorre todas as requisições feitas pelo navegador
        for request in driver.requests:
            if url in request.url and request.response:
                if request.response.status_code != 200:
                    logger.error(f"❌ Erro: A requisição com {url} teve status {request.response.status_code}\n==== RESPOSTA DA API ====\n{pprint.pformat(json.loads(request.response.body.decode('utf-8')))}\n======================")
                    return False
                logger.info(f"✅ A requisição com {url} teve status {request.response.status_code}")
                return True
        sleep(2)
    logger.error(f"❌ Erro: A requisição com {url} não foi encontrada dentro de {max_wait_time} segundos.")
    return False

# Configuração do logger
logger = logging.getLogger("MeuLogger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Handler para o console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
