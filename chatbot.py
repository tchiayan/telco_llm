from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage , SystemMessage , trim_messages
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from langchain_core.chat_history import (
    BaseChatMessageHistory, 
    InMemoryChatMessageHistory # Store chat message history in memory
)
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatOllama(
    model="llama3"
)
parser = StrOutputParser()

# Not working solution
# chain = llm | parser 

# # Chatbot don't access to earlier history
# print(chain.invoke([HumanMessage("Hi, I'm Chia Yan")]))
# print(chain.invoke([HumanMessage("What is my name")]))

# Solution 1: In mememory chat history
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory: 
    if session_id not in store: 
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]



prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful assistant. Answer all the questions to the best of your ability in {language}"), 
    ("user", "{message}") # equal as MessagePlaceholder(variable_name="message")
])
chain_2 =  prompt | llm | parser
with_message_history = RunnableWithMessageHistory(chain_2 , get_session_history=get_session_history , input_messages_key="message")
config  = {
    "configurable": {"session_id" : "abc3"}
}
while True: 
    user_input = input("Enter messsage:")
    for r in with_message_history.stream(
            {
                "message": [HumanMessage(content=user_input)],
                "language": "English",
            },
            config=config,
        ):
        print(r, end="" , flush=True)