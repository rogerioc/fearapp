
# Callback para interação com a interface do Streamlit
from langchain_community.callbacks import StreamlitCallbackHandler  

# Histórico de mensagens para o Streamlit
from langchain_community.chat_message_histories import StreamlitChatMessageHistory 

# Ferramenta de busca DuckDuckGo para o agente 
from langchain_community.tools import DuckDuckGoSearchRun  

# Integração com o modelo de linguagem da OpenAI
from langchain_openai import ChatOpenAI  

from langchain.agents import AgentExecutor, create_tool_calling_agent

# Histórico de mensagens para o Streamlit
from langchain_community.chat_message_histories import StreamlitChatMessageHistory 

# Ferramenta de busca DuckDuckGo para o agente 
from langchain_community.tools import DuckDuckGoSearchRun 

from langchain.tools import tool

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from duckduckgo_search import DDGS
from tenacity import retry, wait_fixed, stop_after_attempt, RetryError
from langchain.tools import Tool


# Retry automático com delay de 2 segundos e até 3 tentativas
@retry(wait=wait_fixed(2), stop=stop_after_attempt(1))
def _duckduckgo_search(query: str) -> str:
    with DDGS() as ddgs:
        results = ddgs.text(query)
        return "\n".join([r["body"] for r in results][:3]) or "Nenhum resultado encontrado."

def duckduckgoSearch(query: str) -> str:
    try:
        return _duckduckgo_search(query)
    except RetryError:
        return "⚠️ Não consegui buscar no momento (rate limit)."
    except Exception as e:
        return f"❌ Erro inesperado: {str(e)}"


class ChatVersion:
    """
    A class to represent the version of a chat application.
    """    
    def __init__(self, prompt_template):
        # Inicialização do histórico de mensagens                
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompt_template),
            MessagesPlaceholder("chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder("agent_scratchpad")])

        
        # ChatPromptTemplate.from_messages(
        #     [system_message_prompt, human_message_prompt]
        # )
        self.msgs = StreamlitChatMessageHistory(key="chat_history")       
       
    def configure(self, openai_api_key):
        self.llm = ChatOpenAI(openai_api_key = openai_api_key, 
                              temperature = 0.5)
        # self.chain = self.prompt_template | self.llm
                 
        # Configuração da ferramenta de busca do agente
        # mecanismo_busca = [DuckDuckGoSearchRun(name = "Search")]       
        search_tool = Tool.from_function(
            name="duckduckgoSearch",
            description="Busca informações na web sobre tópicos atuais ou desconhecidos.",
            func=duckduckgoSearch,
        )
        mecanismo_busca = [search_tool]

        # Criação do agente conversacional com a ferramenta de busca
        self.chat_agent = create_tool_calling_agent(llm = self.llm, 
                                                    tools= mecanismo_busca, 
                                                    prompt = self.prompt_template)

        # Executor para o agente, incluindo memória e tratamento de erros
        self.executor = AgentExecutor(agent = self.chat_agent, 
                                      tools = mecanismo_busca, 
                                      verbose = True,
                                      return_intermediate_steps=True,
                                      handle_parsing_errors = True)

        # Configuração da memória do chat        
        # self.runnable = RunnableWithMessageHistory(
        #                 self.executor,
        #                 lambda session_id: self.msgs,
        #                 input_messages_key="input",
        #                 history_messages_key="chat_history")
        
        
    def clear(self):
        """
        Resets the chat memory and message history.
        """
        self.msgs.clear()
        self.msgs.add_ai_message("O que sobre terror você deseja saber?")

    def add_user_message(self, prompt, container): 
        self.msgs.add_user_message(prompt)       
        st_cb = StreamlitCallbackHandler(container, expand_new_thoughts = False)
        output = self.executor.invoke(
            {"input": prompt, "chat_history": self.msgs.messages},
            config={"callbacks": [st_cb]}
        )
        self.msgs.add_ai_message(output["output"])
        return output
            
    def getMessages(self):
        """
        Returns the current chat messages.
        """
        return self.msgs.messages
