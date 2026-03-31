import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from utils.logger import logger
from utils.tools import salvar_nota_tecnica

# Carrega as variáveis do arquivo .env
load_dotenv()

class CodeAnalyzer:
    def __init__(self):
        # Incializa o modelo (gemini-1.0-pro)
        modelo_base = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                                          temperature=0,
                                          google_api_key=os.getenv("GOOGLE_API_KEY")
                                          )
        
        # Inicializa a memória de mensagens
        self.chat_history = []

        # Conecta a ferramenta ao modelo
        self.llm = modelo_base.bind_tools([salvar_nota_tecnica])

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
            self.chat_history.append(resposta)

            # Caso o modelo decida usar a ferramenta
            if resposta.tool_calls:
                for tool_call in resposta.tool_calls:
                    logger.info(f"Modelo decidiu usar a ferramenta {tool_call['name']}")

                    if tool_call["name"] == "salvar_nota_tecnica":
                        # Executa o código da ferramenta
                        resultado_ferramenta = salvar_nota_tecnica.invoke(tool_call["args"])

                        # Devolve o resultado da execução para o modelo ler
                        mensagem_resultado = ToolMessage(
                            content=resultado_ferramenta, tool_call_id=tool_call["id"]
                        )
                        self.chat_history.append(mensagem_resultado)

                # O modelo formula a resposta final após usar a ferramenta
                resposta_final = self.llm.invoke(self.chat_history)
                self.chat_history.append(resposta_final)
                return resposta_final.content
            
            # Se o modelo não usou nenhuma ferramenta, retorna a resposta normalmente
            return resposta.content
                
            return resposta.content
        except Exception as e:
            logger.error(f"Falha de comunicação com o modelo: {e}")
            return "Desculpe, ocorreu um erro ao tentar obter a resposta do modelo. Por favor, tente novamente mais tarde."