# App web para responder perguntas sobre filmes de terror usando ChatGPT e langchain.
# Imports
import streamlit as st
import QuestionAnswerChain as qa
from QuestionAnswerChain import InMemoryHistory
# Carrega o arquivo de variáveis de ambiente
# Configure seu .env com as variáveis necessárias
# OPENAI_API_KEY
# Usar se for utilizar variáveis de ambiente
# load_dotenv()

template = """Esta é uma conversa entre um cinéfilo e um especialista em filmes de terror. 
                Você é o especialista em filmes de terror, conhece bem os filmes clássicos e novos de terror e deve responder com a maior precisão possível.

    Current conversation:
    {history}
    Human: {input}
    TerrorSpecialist:"""

questionAnswer = qa.QuestionAnswerChain(template = template, inMemoryHistory = InMemoryHistory())
########## App Web ##########

# Configuração da página do Streamlit
st.set_page_config(page_title="FEAR App", page_icon=":skull:", layout="wide")

openai_api_key = st.sidebar.text_input("Adicione sua OpenAI API Key", type = "password")
st.sidebar.markdown("""
https://platform.openai.com/
""")                    
    
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
        questionAnswer.settingKey(openai_api_key)
    # Se temos o código da ação (ticker)
    if question:

        # Inicia o processamento
        with st.spinner("Buscando a resposta. Aguarde..."):                                            
            resposta =  questionAnswer.get_response(question)
            # Imprime a resposta
            st.markdown(resposta)            
            
    else:
        st.error("Verifique se a pergunta foi preenchida corretamente ou se a chave de API foi adicionada.")

# Fim
# Obrigado!




