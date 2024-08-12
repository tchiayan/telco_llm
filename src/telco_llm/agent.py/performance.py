from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from telco_llm.tools.trending import trending_analysis

def create_agent(llm , tools ):
    
    """Create performance agent"""
    
    prompt  = ChatPromptTemplate.from_messages([
        ("system" , """
            You are telecommunication performance analysis agent that analyse the performance of telecommunication network.
            
            You are required to make the following analysis: 
            1. Is the KPI performance is degraded or improved? 
            2. If the KPI performance is degraded, which top 5 cells are the most poorest performance? 
            3. Draw the trending analysis of the KPI performance to user. 
        """), 
        MessagesPlaceholder("question")
    ])
    
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    
    return prompt | llm  

