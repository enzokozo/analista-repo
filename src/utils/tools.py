import os
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