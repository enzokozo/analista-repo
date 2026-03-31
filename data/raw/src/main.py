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

    # Inicializa o analisador e carrega a memória inicial
    analyzer = CodeAnalyzer()
    analyzer.iniciar_sessao(arquivos)

    # Interface do terminal
    print("\n" + "="*55)
    print("🤖 ASSISTENTE DE ANÁLISE DE CÓDIGOS INICIADO")
    print("Faça perguntas sobre os arquivos ou digite 'sair' para encerrar.")
    print("="*55)

    while True:
        pergunta = input("\n 👤 Você: ")

        # Condição de saída
        if pergunta.strip().lower() in ['sair', 'exit', 'quit', 'fechar']:
            print("🤖 Encerrando o assistente. Até a próxima!")
            logger.info("Sessão encerrada pelo usuário.")
            break

        # Evita mandar mensagem vazia para a API
        if not pergunta.strip():
            continue

        # Chama o modelo
        logger.info("Enviando pergunta para o modelo...")
        resposta = analyzer.fazer_pergunta(pergunta)

        print(f"🤖 Assistente: {resposta}")

if __name__ == "__main__":
    main()