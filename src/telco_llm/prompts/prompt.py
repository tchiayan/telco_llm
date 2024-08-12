from langchain_core.prompts  import FewShotPromptTemplate , PromptTemplate , ChatPromptTemplate
from telco_llm.prompts.fewshot import database_few_shot

database_prompt = FewShotPromptTemplate(
    examples = database_few_shot, 
    example_prompt=PromptTemplate.from_template("User input: {input}\nSQL Query: {query}"), 
    prefix="""
    You are a SQLite expert with Telecommunication RF Domain Expert. Given an input question, create a syntactically correct SQLite query to run. Generate and return SQL command only in single line. \
    Unless otherwise specificed, do not limit the number of row. {top_k}\n\n \
    Here is the relevant table info: {table_info}\n\n \
        
        
    Provided the formula information as follows: 
    {formula}

    Below are a number of examples of questions and their corresponding SQL queries.
    """, 
    suffix="User input: {input}\n SQL query:" , 
    input_variables=["input" , "top_k" , "table_info" , "formula"]
)

