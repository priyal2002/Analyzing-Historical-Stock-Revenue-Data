#!/usr/bin/env python
# coding: utf-8

# # ANALYZING HISTORICAL STOCK/REVENUE DATA
# 
# As a data scientist in an investment firm, I have undertaken a data science project aimed at analyzing the revenue data for various companies. The goal of this project is to build a dashboard that allows the company's stakeholders to compare the price of the stock versus the revenue.

# In[1]:


import yfinance as yf
import pandas as pd


# __Question1: Using the yfinance Library to Extract Stock Data
# 
# Using the Ticker module we can create an object that will allow us to access functions to extract data. To do this we need to provide the ticker symbol for the stock, here the company is Tesla and the ticker symbol is TSLA.
# 
# Reset the index, save, and display the first five rows of the tesla_data dataframe using the head function.
# 

# In[2]:


tesla = yf.Ticker("TSLA")


# In[3]:


tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
tesla_data.head()


# __Question 2: Use Webscraping to Extract Tesla Revenue Data
# 
# Display the last five rows of the tesla_revenue dataframe using the tail function.
# 

# In[4]:


import pandas as pd
import requests
from bs4 import BeautifulSoup


# In[5]:


url = " https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text
soup = BeautifulSoup(html_data,"html5lib")


# In[42]:


tables = soup.find_all('table')
for index,table in enumerate(tables):
    if ("Tesla Quarterly Revenue" in str(table)):
        table_index = index
Tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        Tesla_revenue = Tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)
        
Tesla_revenue.tail()


# __Question 3: Use yfinance to Extract Stock Data
# 
# The stock is GameStop and its ticker symbol is GME.
# Reset the index, save, and display the first five rows of the gme_data dataframe using the head function. 

# In[7]:


gme = yf.Ticker("GME")


# In[8]:


gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.head()


# __Question 4: Use Webscraping to Extract GameStop Revenue Data
# 
# Display the last five rows of the gme_revenue dataframe using the tail function.

# In[9]:


url="https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
data= requests.get(url).text


# In[10]:


soup = BeautifulSoup(data,"html5lib")


# In[11]:


tables = soup.find_all('table')
for index,table in enumerate(tables):
    if ("GameStop Quarterly Revenue" in str(table)):
        table_index = index
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        gme_revenue = gme_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[12]:


gme_revenue.tail()


# __Question 5: Plotting Tesla Stock Graph
# 
# Use the make_graph function to graph the Tesla Stock Data, also provide a title for the graph.

# In[26]:


import plotly
from plotly.subplots import make_subplots
import plotly.graph_objs as go


# In[27]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[43]:


make_graph(tesla_data, Tesla_revenue, 'TSLA')


# __Question 6: Plotting GameStop Stock Graph
# 
# Use the make_graph function to graph the GameStop Stock Data, also provide a title for the graph.

# In[32]:


make_graph(gme_data, gme_revenue, 'GameStop')

