from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage , SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate , ChatPromptTemplate

llm = ChatOllama(
    model="llama3"
)

# messages = [
#     SystemMessage(content="Translate the following from English to Chinese") , 
#     HumanMessage(content="Hi, how are you?")
# ]
prompt = ChatPromptTemplate.from_template(
    "Translate the following from English to {language}. \
    Input: {input}"
)
## Similary can be as follow
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "Translate the following from Englisht to {language}") , 
#     ("user" , "{input}")
# ])

parser = StrOutputParser()

chain = prompt | llm | parser
print(chain.invoke({"language":"chinese" , "input":"how are you?"}))


