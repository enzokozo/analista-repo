import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

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

            # Cria o "Template de Prompt" que será o guia de como o modelo deve responder
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Você é um Engenheiro de Software Sênior especialista em análise de sistemas."),
                ("user", "Analise a estrutura deste repositório e faça um resumo técnico explicando o que o sistema faz e como os arquivos se conectam:\n\n{codigo}")
            ])

            # "Chain" une o prompt ao modelo
            chain = prompt | self.llm


            # Invoca a cadeia, passando o contexto formatado, e obtemos a resposta
            response = chain.invoke({"codigo": context})
            return response.content
        except Exception as e:
            return f"Erro ao gerar análise: {str(e)}."