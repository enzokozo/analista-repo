import logging
import os
from datetime import datetime

def setup_logger():
    # Garante que a pasta de logs existe
    log_dir = "data/logs"
    os.makedirs(log_dir, exist_ok=True)

    # Cria um arquivo com a data de hoje
    log_filename = datetime.now().strftime("%Y-%m-%d_execucao.log")
    log_filepath = os.path.join(log_dir, log_filename)

    # Define a "cara" da mensagem: Data/Hora - Nível - Mensagem
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    # Configura o comportamento do logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_filepath, encoding="utf-8"), # Escreve no arquivo de log
            logging.StreamHandler() # Mostra no terminal
        ]
    )

    return logging.getLogger(__name__)

# Deixa uma instância do logger pronta para ser usada em outros arquivos
logger = setup_logger()
