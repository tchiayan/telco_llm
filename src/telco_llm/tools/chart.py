from langchain.tools import tool 
from typing import List

import matplotlib.pyplot as plt

@tool
def plot_timeseries(times_or_objects:List[str], values:List[float], chart_title:str):
    """Plot the trending given the times series or object series and KPI performance values"""
    plt.clf()  # Clear any previous plot
    plt.plot(times_or_objects, values)
    plt.xticks(rotation=90)
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title(chart_title)
    return plt.gcf()