import bs4 
from langchain.chat_models.ollama import ChatOllama 
from langchain_chroma import Chroma 
from langchain_community.document_loaders import WebBaseLoader 
from langchain_core.output_parsers import StrOutputParser 
from langchain_community.embeddings import OllamaEmbeddings
