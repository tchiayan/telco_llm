from statsmodels.tsa.seasonal import seasonal_decompose 
import pandas as pd 
from langchain.tools import tool

@tool
def trending_analysis(data: pd.DataFrame  , value_col: str , date_col: str = 'time' , freq: int = 30): 
    """
    Function to perform trending analysis using seasonal_decompose from statsmodels.tsa.seasonal. Return the trending component of the data
    
    Args: 
    data: pd.DataFrame: input data
    date_col: str: date column name
    value_col: str: value column name
    freq: int: frequency of the data
    
    Returns: 
    dict: dictionary containing the trending component of the data
    """
    data = data.set_index(date_col)
    result = seasonal_decompose(data[value_col] , model='additive' , period=freq)
    return {
        "trend": result.trend.dropna() , 
    }