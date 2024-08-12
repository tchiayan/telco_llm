from langchain_core.documents import Document 
from langchain_chroma import Chroma 
from langchain_community.embeddings import OllamaEmbeddings 
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

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

vector_store = Chroma.from_documents(documents=documents , embedding=OllamaEmbeddings(model="llama3"))
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k":4}
)

message = """
Answer this question using the provided context only. 

{question}

Context: 
{context}
"""
prompt = ChatPromptTemplate.from_template(message)
llm = ChatOllama(
    model="llama3"
)
parser = StrOutputParser()
chain = {
    "context": retriever, 
    "question": RunnablePassthrough()
} | prompt | llm | parser 

for r in chain.stream({"question":"Tell me more about cat"}):
    print(r , end="" , flush=True)
print("\n")