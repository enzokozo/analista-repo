import os
from utils.logger import logger

def read_repository_file(root_path, max_file_size_kb=50):
    """
    Percorre a pasta raiz e lê o conteúdo de arquivos de texto/código.
    Ignora arquivos maiores que 'max_file_size_kb'
    Retorna um dicionário: { 'nome_do_arquivo': 'conteúdo_do_arquivo' }
    """
    repo_data = {}

    # Extensões de arquivos que queremos ler
    allowed_extensions = ('.py', '.txt', '.md', '.js')

    max_bytes = max_file_size_kb * 1024 # Converte KB para Bytes

    # os.walk navega por todas as subpastas automaticamente
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(allowed_extensions): # Verifica se o arquivo tem uma extensão permitida
                file_path = os.path.join(root, file) # Une o caminho da pasta com o nome do arquivo

                tamanho_arquivo = os.path.getsize(file_path) # Checa o tamanho do arquivo antes de abrir

                if tamanho_arquivo > max_bytes:
                    logger.warning(f"Arquivo {file_path} ignorado por exceder o limite de tamanho: ({tamanho_arquivo/1024:.1f} KB).")
                    continue # Pula para o próximo arquivo

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # Guarda o caminho relativo para o LLM entender a estrutura
                        relative_path = os.path.relpath(file_path, root_path) # Caminho relativo em relação à pasta raiz
                        repo_data[relative_path] = f.read()
                        logger.info(f"Arquivo lido com sucesso: {relative_path}")
                except Exception as e:
                    logger.error(f"Erro ao ler {file_path}: {e}")

    return repo_data    