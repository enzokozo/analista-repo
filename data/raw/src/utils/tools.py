import os
import sys
import io
from langchain_core.tools import tool
from utils.logger import logger

# @tool avisa o LangChain que o LLM pode usar essa função
@tool
def salvar_nota_tecnica(nome_arquivo: str, conteudo: str) -> str:
    """
    ÚTIL PARA SALVAR ARQUIVOS.
    Cria e salva uma nota técnica, documentação ou relatório na pasta data/output.
    O nome do arquivo deve conter a extensão (ex: resumo.md, relatorio.txt)
    """

    caminho_pasta = "data/output"
    os.makedirs(caminho_pasta, exist_ok=True)
    caminho_completo = os.path.join(caminho_pasta, nome_arquivo)

    try:
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        logger.info(f"Arquivo '{nome_arquivo}' criado.")
        return f"Arquivo salvo em {caminho_completo}."
    except Exception as e:
        logger.error(f"Error na ferramenta salvar_nota_tecnica: {e}")
        return f"Erro ao tentar salvar o arquivo: {e}"
    
@tool
def executar_codigo_python(codigo: str) -> str:
    """
    ÚTIL PARA ANALISAR DADOS (CSV, JSON, EXCEL) OU FAZER CÁLCULOS MATEMÁTICOS.
    Recebe uma string com código Python puro, executa localmente e retorna o texto do console (stdout).
    DICA PARA O MODELO: Para ler arquivos, lembre-se que eles estarão na pasta 'data/raw/'.
    Sempre use a função print() no seu código para retornar os resultados, pois o que for impresso será capturado e retornado como resposta.
    """
    logger.info("O modelo acionou o interpretador Python. Executando código gerado...")

    # Redireciona a saída padrão para capturar o resultado do código
    old_stdout = os.sys.stdout
    redirected_output = sys.stdout = io.StringIO()

    try:
        # Avalia e roda a string de código como se fosse um script real
        exec(codigo)

        # Devolve o fluxo do terminal ao normal
        sys.stdout = old_stdout
        resultado = redirected_output.getvalue()

        logger.info("Código Python executado com sucesso.")
        return f"Resultado da execução:\n{resultado}" if resultado else "Código executado, mas sem saída visível."
    except Exception as e:
        sys.stdout = old_stdout
        logger.error(f"Erro ao executar código Python gerado pelo modelo: {e}")
        return f"Erro ao executar o código Python: {e}. Revise a sintaxe e tente novamente."