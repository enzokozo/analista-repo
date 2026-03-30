from utils.reader import read_repository_file
from core.analyzer import CodeAnalyzer
from utils.logger import logger

def main():
    path_to_analyze = "data/raw"
    logger.info(f"Lendo os arquivos do repositório: {path_to_analyze}")
    arquivos = read_repository_file(path_to_analyze)

    if not arquivos:
        # Usa warning (aviso) para situações que não quebram o app, mas exigem atenção
        logger.warning(f"Nenhum arquivo encontrado para análise em {path_to_analyze}. Verifique o caminho e tente novamente.")
        return

    logger.info(f"Analisando {len(arquivos)} arquivos com LLM...")
    analyzer = CodeAnalyzer()
    relatorio = analyzer.generate_summary(arquivos)

    # Salva o resultado na pasta output
    output_path = "data/output/analise_tecnica.md"

    try: 
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(relatorio)
        
        logger.info(f"Análise concluída! Veja o resultado em: {output_path}")
    except Exception as e:
        # Usa error para falhas que impedem o funcionamento correto do app
        logger.error(f"Erro ao salvar o relatório: {str(e)}")

if __name__ == "__main__":
    main()