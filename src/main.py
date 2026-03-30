from utils.reader import read_repository_file

def main():
    path_to_analyze = "data/raw"
    print(f"--- Iniciando leitura de: {path_to_analyze} ---")

    arquivos = read_repository_file(path_to_analyze)

    for nome, conteudo in arquivos.items():
        print(f"Arquivo encontrado: {nome} ({len(conteudo)} caracteres)")

if __name__ == "__main__":
    main()