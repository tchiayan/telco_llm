# Test vector search as function calling 
from langchain_core.documents import Document 
from langchain_community.embeddings import OllamaEmbeddings 
from langchain_chroma import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.tools import tool , create_retriever_tool
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain.agents import create_tool_calling_agent , AgentExecutor
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from pprint import pprint
import asyncio

# Create documents
documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc"},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"source": "bird-pets-doc"},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

# Build vector store and retriever
vector_store = Chroma.from_documents(
    documents=documents,
    embedding=OllamaEmbeddings(model="llama3")
)
retriever = vector_store.as_retriever(
    search_type="similarity", 
    search_kwargs={"k": 1}
)

# # create tool 
# @tool 
# def rag_search(animal): 
#     """Search information about animal. For any question about animal, you must use this tool!"""
#     global retriever 
#     return retriever.invoke(animal)
rag_search = create_retriever_tool(
    retriever=retriever , 
    name="retrieve_animal_information" , 
    description="Search information about animal. For any question about animal, you must use this tool!"
)

@tool 
def multiply(a: int , b:int):
    """Multiply two numbers. When user ask about multiply two number, must use this function"""
    return a*b
print(multiply)

@tool 
def get_weather_temperature(location:str):
    """Get the current weather temperature in celcius"""
    return 19

tools = [ rag_search , multiply , get_weather_temperature]
# The following 2 lines not going to work due to ChatOllama do not support bind_tools function compare to ChatOpenAI
# llm = ChatOllama(model="llama3")
# llm.bind_tools(retriever)


# LLM model using open ai
llm = ChatOpenAI(
    model='gpt-3.5-turbo',
    api_key="API_KEY",
    #base_url="http://localhost:11434/v1"
) #.with_config({"tags": ["agent_llm"]})

# llm = OllamaFunctions(
#     model="llama3"
# )
# llm_with_tool = llm.bind_tools(tools)
# response = llm_with_tool.invoke("Tell me about cat")
# print(f"Content: {response.content}")
# print(f"ToolCall: {response.tool_calls}")

prompt = ChatPromptTemplate.from_messages([
    ("ai", "you are helpfull assistance"),
    MessagesPlaceholder("chat_history"),
    ("user" , "{input}") ,
    MessagesPlaceholder("agent_scratchpad")
])
agent = create_tool_calling_agent(llm , tools ,  prompt )
#agent.invoke({"input": "Multiply 2 by 4"})

agent_exec = AgentExecutor(agent=agent , tools=tools) #.with_config({"run_name": "Agent"})

# get history function 
store = {}
def get_history(session_id:str) -> BaseChatMessageHistory: 
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    
    return store[session_id]

agent_exec_with_message_history = RunnableWithMessageHistory(
    runnable=agent_exec, 
    get_session_history=get_history , 
    input_messages_key='input', 
    history_messages_key='chat_history' 
)

chunks = []

# for chunk in agent_exec_with_message_history.stream(
#         {"input" , "Multiply 2 by 8"} , {"configurable": {"session_id": "session_abc"}}
#     ):
#     chunks.append(chunk)
#     print("---------")
#     pprint(chunk , depth=1)
while True: 
    user = input("Prompt: ")
    for r in agent_exec_with_message_history.stream({"input":user} , {"configurable":{"session_id":"sessionabc"}}):
        print(r , end="" , flush=True)
    print("\n")
     

# # create prompt 
# prompt = PromptTemplate.from_template(""" 
#     Answer the question based on given context:
#     Context: {context} 
#     Question: {question}                                  
# """)

# # create output parser
# parser = StrOutputParser()

# # create rag_chain
# rag_chain = {
#     "context": retriever, 
#     "question": RunnablePassthrough()
# } | prompt | llm | parser 

# while True: 
#     question = input("Enter question: ")
#     for r in rag_chain.stream(question):
#         print(r , end="" , flush=True)
#     print("\n")