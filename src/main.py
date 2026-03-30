from utils.reader import read_repository_file
from core.analyzer import CodeAnalyzer

def main():
    path_to_analyze = "data/raw"
    print(f"Lendo os arquivos do repositório: {path_to_analyze}")
    arquivos = read_repository_file(path_to_analyze)

    if not arquivos:
        print(f"Nenhum arquivo encontrado para análise em {path_to_analyze}. Verifique o caminho e tente novamente.")
        return

    print(f"Analisando {len(arquivos)} arquivos com LLM...")
    analyzer = CodeAnalyzer()
    relatorio = analyzer.generate_summary(arquivos)

    # Salva o resultado na pasta output
    output_path = "data/output/analise_tecnica.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(relatorio)
    
    print(f"Análise concluída! Veja o resultado em: {output_path}")

if __name__ == "__main__":
    main()