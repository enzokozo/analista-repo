import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from utils.logger import logger

# Carrega as variáveis do arquivo .env
load_dotenv()

class CodeAnalyzer:
    def __init__(self):
        # Incializa o modelo (gemini-1.0-pro)
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                                          temperature=0,
                                          google_api_key=os.getenv("GOOGLE_API_KEY")
                                          )

    def generate_summary(self, repo_data):
        """
        Recebe o dicionário de arquivos e gera uma explicação técnica.
        """

        try:
            # Prepara o contexto: transformammos o dicionário em uma string formatada
            context = ""
            for path, content in repo_data.items():
                context += f"\n--- ARQUIVO: {path} ---\n {content}\n"

            # Limita a quantidade de caracteres
            LIMITE_CARACTERES = 10000
            if len(context) > LIMITE_CARACTERES:
                logger.warning(f"Contexto gigante detectado: {len(context)} caracteres. Truncando para evitar error na API...")
                context = context[:LIMITE_CARACTERES] + "\n\n... [CÓDIGO TRUNCADO POR SEGURANÇA] ..."

            # Cria o "Template de Prompt" que será o guia de como o modelo deve responder
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Você é um Engenheiro de Software Sênior especialista em análise de sistemas."),
                ("user", "Analise a estrutura deste repositório e faça um resumo técnico explicando o que cada arquivo faz e como eles se conectam:\n\n{codigo}")
            ])

            logger.info("Enviando prompt estruturado para o modelo...")

            # "Chain" une o prompt ao modelo
            chain = prompt | self.llm

            # Invoca a cadeia, passando o contexto formatado, e obtemos a resposta
            response = chain.invoke({"codigo": context})
            return response.content
        except Exception as e:
            logger.error(f"Falha de comunicação com o modelo: {str(e)}")
            return f"Erro ao gerar análise: {str(e)}."