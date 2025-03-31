import logging

# Configuração avançada do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="testes/logging_test.log",
    filemode="w"
)

logging.info("Este log será salvo no arquivo.")
logging.warning("⚠️ Isso também!")

logging.debug("Isso é um log de debug (não será mostrado por padrão).")
logging.info("Isso é um log de informação.")
logging.warning("⚠️ Aviso! Algo pode estar errado.")
logging.error("❌ Erro! Algo falhou.")
logging.critical("🔥 Erro crítico! O sistema pode falhar!")