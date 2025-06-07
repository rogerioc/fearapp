from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import BaseMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from pydantic import BaseModel, Field

# Classe para armazenar o histórico de mensagens em memória
class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list)
    def add_messages(self, messages: list[BaseMessage]) -> None:        
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []


class QuestionAnswerChain:
    # Template para a conversa
       
    def __init__(self,template, inMemoryHistory):
        self.template = template + """
    Current conversation:
    {history}
    Human: {input}
    TerrorSpecialist:"""
        
        self.question_prompt = PromptTemplate(input_variables = ["history", "input"], template = template)
        self.store = {}
        self.inMemoryHistory = inMemoryHistory        

    def settingKey(self,openai_api_key):
        self.chatGpt = ChatOpenAI(temperature = 0.5, openai_api_key=openai_api_key)
        self.__configChain()
    
    # Função para obter o histórico de mensagens por ID de sessão
    def __get_by_session_id(self,session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = self.inMemoryHistory
        return self.store[session_id]

    def __configChain(self):
        chain = self.question_prompt | self.chatGpt
        ## CobnversationChain será descontinuado em breve, então comecei a usar o RunnableWithMessageHistory para entender as diferenças
        self.conversation = RunnableWithMessageHistory(chain, self.__get_by_session_id,
                                            input_messages_key="input",
                                            history_messages_key="history")

    def get_response(self,question):
        prompt = { "ability": "filmes", "input": question}        
        resultado = self.conversation.invoke(prompt, config={"configurable": {"session_id": "1"}})
        print(self.store)
        return "Especialista: " + resultado.content