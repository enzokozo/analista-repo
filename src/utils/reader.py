import os

def read_repository_file(root_path):
    """
    Percorre a pasta raiz e lê o conteúdo de arquivos de texto/código.
    Retorna um dicionário: { 'nome_do_arquivo': 'conteúdo_do_arquivo' }
    """
    repo_data = {}

    # Extensões de arquivos que queremos ler
    allowed_extensions = ('.py', '.txt', '.md', '.js')

    # os.walk navega por todas as subpastas automaticamente
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(allowed_extensions): # Verifica se o arquivo tem uma extensão permitida
                file_path = os.path.join(root, file) # Une o caminho da pasta com o nome do arquivo

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # Guarda o caminho relativo para o LLM entender a estrutura
                        relative_path = os.path.relpath(file_path, root_path) # Caminho relativo em relação à pasta raiz
                        repo_data[relative_path] = f.read()
                except Exception as e:
                    print(f"Erro ao ler {file_path}: {e}")

    return repo_data    