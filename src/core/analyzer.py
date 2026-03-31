import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
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
        
        # Inicializa a memória de mensagens
        self.chat_history = []

    def iniciar_sessao(self, repo_data):
        """
        Pega todos os arquivos e injeta como uma instrução de sistema oculta.
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

            # SystemMessage é a mensagem de configuração do modelo
            instrucao_sistema = (
                "Você é um Engenheiro de Software Sênior e um Assistente Especialista neste repositório. "
                "Use estritamente o código fornecido abaixo como sua base de conhecimento para responder às perguntas do usuário. "
                "Se a resposta não estiver no código, diga que não encontrou nos arquivos fornecidos.\n\n"
                f"REPOSITÓRIO:\n{context}"    
            )

            # A primeira coisa da memória é o contexto do repositório
            self.chat_history = [SystemMessage(content=instrucao_sistema)]
            logger.info("Sessão iniciada com o contexto do repositório injetado na memória.")
        except Exception as e:
            logger.error(f"Erro ao iniciar sessão: {e}")
            raise

    def fazer_pergunta(self, pergunta_usuario):
        """
        Recebe a pergunta do usuário, adiciona à memória e gera a resposta usando o modelo.
        """

        try:
            # Adiciona a pergunta do usuário na memória
            self.chat_history.append(HumanMessage(content=pergunta_usuario))

            # Passa o histórico completo para o modelo gerar a resposta (repositório + perguntas anteriores + nova pergunta)
            resposta = self.llm.invoke(self.chat_history)

            # Guarda a resposta do modelo na memória
            self.chat_history.append(AIMessage(content=resposta.content))
            
            return resposta.content
        except Exception as e:
            logger.error(f"Falha de comunicação com o modelo: {e}")
            return "Desculpe, ocorreu um erro ao tentar obter a resposta do modelo. Por favor, tente novamente mais tarde."