import os
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from telco_llm.prompts.prompt import database_prompt
from telco_llm.pydantic import TelcoQueryKPI
from telco_llm.database.kpi_database import get_kpi_database
from langchain.chains import create_sql_query_chain
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough , RunnableLambda , chain
from langchain_core.output_parsers import StrOutputParser
from google.oauth2 import service_account 
import pandas_gbq 

project_id = os.getenv("BIGQUERY_PROJECT_ID")
dataset_id = os.getenv("BIGQUERY_DATASET_ID")
openai_api_key = os.getenv("OPENAI_API_KEY")
service_account_file = os.getenv("GOOGLE_SERVICE_FILE")

assert project_id is not None , "BIGQUERY_PROJECT_ID is not set"
assert dataset_id is not None , "BIGQUERY_DATASET_ID is not set"
assert openai_api_key is not None , "OPENAI_API_KEY is not set"
assert service_account_file is not None , "GOOGLE_SERVICE_FILE is not set"

llm = ChatOpenAI(
    model="gpt-4o-mini" ,
    api_key=openai_api_key
)

def create_telco_kpi_chain():
    # create kpi rag 
    structured_llm = llm.with_structured_output(TelcoQueryKPI)
    rag_chain = (
        ChatPromptTemplate.from_template(
        """You are telecommunication field specialist agent. Given user question below, classify the question is related to which radio field topic, output in '4G', '3G', '2G' or 'unclear' only. 
        You should also identify the kpi name related to telecommunication that user is asking and kpi name shall not contain any technology word such as LTE, 4G, etc.
        
        User: {messages}
        """
        ) | structured_llm
    )
    
    return {
        "kpi_extraction": rag_chain , "messages": lambda x: x['messages'] # , "table_names_to_use": lambda x: x['table_names_to_use']
    } | RunnableLambda(route)
    
def create_telco_sql_query_chain(): 
    
    # create db
    sqlalchemy_url = f'bigquery://{project_id}/{dataset_id}'
    db = SQLDatabase.from_uri(sqlalchemy_url , {"credentials_path":service_account_file})
    
    
    return create_sql_query_chain(
        llm , db , database_prompt
    )
    
    
def get_kpiname(input)->str: 
    return input['kpi_extraction'].kpi_name

def route(info): 
    vector_4g , vector_2g = get_kpi_database()
    retriever = (vector_4g if ("4G" in info['kpi_extraction'].technology or "LTE" in info['kpi_extraction'].technology ) else vector_2g).as_retriever()
    
    return {
        "context": get_kpiname | retriever , 
        "messages": lambda x: x['messages']
    } | ChatPromptTemplate.from_template("""
        You are specialize agent in telecommunication field that extract relevent KPI formula from chat history. 
        Identify the user question what KPI they are asking and answer the kpi formula based on only provided reteiver context. 
        Do not format the answer in multiple line and return the correct kpi formula only. 
        If provided context does not contain any information about the KPI, just return what are the problem with the context.

        Chat History:
        {messages}

        Retriever Context: 
        {context}
    """) | llm | StrOutputParser()
    
def create_performance_chain():
    
    kpi_chain = create_telco_kpi_chain()
    sql_chain = create_telco_sql_query_chain()
    
    # TO-DO: 
    # 1. Execute the SQL from the sql_chain and return return result as pandas dataframe
    
    return {
        "formula": kpi_chain , 
        "question": lambda x: x['messages'][-1] , 
        "table_names_to_use": lambda x: ["mc4g_cell_combined" , "mc2g_cell_combined"]
    } | sql_chain | query_data
    
@chain
def query_data(sql): 
    try:
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        return pandas_gbq.read_gbq(sql , project_id=project_id , credentials=credentials).to_json(date_format='iso')
    except Exception as e:
        return "Unable to execute the query correctly"
     