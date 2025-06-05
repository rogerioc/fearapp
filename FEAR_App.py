# App web para responder perguntas sobre filmes de terror usando ChatGPT e langchain.
# Imports
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import BaseMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from pydantic import BaseModel, Field

# Carrega o arquivo de variáveis de ambiente
# Configure seu .env com as variáveis necessárias
# OPENAI_API_KEY
# Usar se for utilizar variáveis de ambiente
# load_dotenv()


# Template para a conversa
template = """Esta é uma conversa entre um cinéfilo e um especialista em filmes de terror. 
                Você é o especialista em filmes de terror, conhece bem os filmes clássicos e novos de terror e deve responder com a maior precisão possível.

Current conversation:
{history}
Human: {input}
TerrorSpecialist:"""

question_prompt = PromptTemplate(input_variables = ["history", "input"], template = template)

# Classe para armazenar o histórico de mensagens em memória
class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list)
    def add_messages(self, messages: list[BaseMessage]) -> None:        
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []

store = {}

# Função para obter o histórico de mensagens por ID de sessão
def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

def config(chatGpt):
    chain = question_prompt | chatGpt
    ## CobnversationChain será descontinuado em breve, então comecei a usar o RunnableWithMessageHistory para entender as diferenças
    return RunnableWithMessageHistory(chain, get_by_session_id,
                                          input_messages_key="input",
                                          history_messages_key="history")

def get_response(question, conversation):
    prompt = { "ability": "filmes", "input": question}        
    resultado = conversation.invoke(prompt, config={"configurable": {"session_id": "1"}})
    print(store)
    return "Especialista: " + resultado.content

########## App Web ##########

# Configuração da página do Streamlit
st.set_page_config(page_title="FEAR App", page_icon=":skull:", layout="wide")

openai_api_key = st.sidebar.text_input("Adicione sua OpenAI API Key", type = "password")
st.sidebar.markdown("""
https://platform.openai.com/
""")                    
# Configuração do modelo ChatGPT
def configModel(openai_api_key):
    chatGpt = ChatOpenAI(temperature = 0.5, openai_api_key=openai_api_key)
    return config(chatGpt)
    
# Barra Lateral com instruções
st.sidebar.title("Instruções")
st.sidebar.markdown("""
### Como Utilizar a App:
- Primeiro, adicione sua OpenAI API Key no campo de texto na barra lateral.
- Insira a pergunta sobre filmes de terror no campo de texto.

### Finalidade da App:
Um pequeno assistente para responder perguntas sobre filmes de terror, utilizando o modelo ChatGPT da OpenAI e LangChain.
                    
## Contato
- **Linkedin:** https://www.linkedin.com/in/rogeriocs/
- **GitHub:** https://github.com/rogerioc/fearapp
""")

# Interface principal
st.header("Tudo Respostas sobe Filmes de terrors")

# Caixa de texto para input do usuário
question = st.text_input("Digite a pergunta:",  placeholder = "Digite uma pergunta!").upper()

# Se o usuário pressionar o botão, entramos neste bloco
if st.button("Analisar"):
    # Verificação da chave de API
    if not openai_api_key:
        st.info("Adicione sua OpenAI API key para continuar.")
        st.stop()
    else:
        # Configura o modelo ChatGPT com a chave de API fornecida
        conversation = configModel(openai_api_key)
    # Se temos o código da ação (ticker)
    if question:

        # Inicia o processamento
        with st.spinner("Buscando a resposta. Aguarde..."):                                            
            resposta = get_response(question, conversation)
            # Imprime a resposta
            st.markdown(resposta)            
            
    else:
        st.error("Verifique se a pergunta foi preenchida corretamente ou se a chave de API foi adicionada.")

# Fim
# Obrigado!




