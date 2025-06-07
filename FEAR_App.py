# App web para responder perguntas sobre filmes de terror usando ChatGPT e langchain.
# Imports
import streamlit as st
import ChatVersion as ch
# Carrega o arquivo de variáveis de ambiente
# Configure seu .env com as variáveis necessárias
# OPENAI_API_KEY
# Usar se for utilizar variáveis de ambiente
# load_dotenv()

template = """Esta é uma conversa entre um cinéfilo e um especialista em filmes de terror. 
                Você é o especialista em filmes de terror, conhece bem os filmes clássicos e novos de terror e deve responder 
                com a maior precisão possível. E somente sobre este assunto."""

cv = ch.ChatVersion(prompt_template= template)
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
st.header("Tudo sobe Filmes de terrors")
if len(cv.getMessages()) == 0 or st.sidebar.button("Reset"):
    # Limpa o histórico de mensagens e inicia a conversa
    cv.clear()
    st.session_state.steps = {}

# Definição de avatares para os participantes da conversa
avatars = {"human": "user", "ai": "assistant"}

# Exibe mensagens no chat
# Loop para exibir mensagens no chat
# Itera sobre cada mensagem no histórico de mensagens
for idx, msg in enumerate(cv.getMessages()):  

    # Cria uma mensagem no chat com o avatar correspondente ao tipo de usuário (humano ou IA)
    with st.chat_message(avatars[msg.type]):  
        print(msg.type)
        # Itera sobre os passos armazenados para cada mensagem, se houver
        for step in st.session_state.steps.get(str(idx), []):  

            # Se o passo atual indica uma exceção, pula para o próximo passo
            if step[0].tool == "_Exception":  
                continue

            # Cria um expander para cada ferramenta usada na resposta, mostrando o input
            with st.expander(f"✅ **{step[0].tool}**: {step[0].tool_input}"): 

                # Exibe o log de execução da ferramenta 
                st.write(step[0].log)  

                # Exibe o resultado da execução da ferramenta
                st.write(f"**{step[1]}**")  

        # Exibe o conteúdo da mensagem no chat
        st.write(msg.content)

if prompt := st.chat_input(placeholder = "Digite uma pergunta para começar!"):
    # Verificação da chave de API
    if not openai_api_key:
        st.info("Adicione sua OpenAI API key para continuar.")
        st.stop()
    else:
        # Configuração do modelo de linguagem da OpenAI
        cv.configure(openai_api_key)

    st.chat_message("user").write(prompt)            
    # Exibição da resposta do assistente
    with st.chat_message("assistant"):

        # Adiciona a mensagem do usuário e executa o agente
        response = cv.add_user_message(prompt, st.container())        
        st.write(response["output"])
        # st.write(response["output"])

        # Armazenamento dos passos intermediários
        st.session_state.steps[str(len(cv.getMessages()) - 1)] = response["intermediate_steps"]  
