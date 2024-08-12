from langchain_community.document_loaders.csv_loader import CSVLoader 
from langchain_chroma import Chroma 
from langchain_openai.embeddings import OpenAIEmbeddings

def get_kpi_database():
    """
    Retrieves the KPI database for 4G and 2G networks.
    
    Returns:
        tuple: A tuple containing the 4G KPI database and the 2G KPI database.
    """
    
    # 4g kpis 
    documents_4g = CSVLoader(file_path="./documents/kpi_4g.csv").load() 
    vectordb_4g = Chroma.from_documents(
        documents_4g , 
        OpenAIEmbeddings() , 
        collection_name="4g_kpi"
    )
    
    # 2g kpis
    documents_2g = CSVLoader(file_path="./documents/kpi_2g.csv").load()
    vectordb_2g = Chroma.from_documents(
        documents_2g , 
        OpenAIEmbeddings() , 
        collection_name="2g_kpi"
    )
    
    return vectordb_4g , vectordb_2g