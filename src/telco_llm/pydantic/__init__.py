from langchain_core.pydantic_v1 import BaseModel , Field 

class TelcoQueryKPI(BaseModel): 
    """Extract user question regarding KPI in telecommunication field."""
    
    kpi_name : str = Field(description="KPI name for telecommunication field")
    technology: str = Field(description="Technology of radio communication")
    