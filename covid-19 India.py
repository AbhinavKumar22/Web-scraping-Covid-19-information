#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


from urllib.request import urlopen
from bs4 import BeautifulSoup


# # Web Scraping

# In[3]:


url = "link of the website"
html = urlopen(url)


# In[4]:


soup = BeautifulSoup(html, 'html.parser')
type(soup)


# In[5]:


text = soup.get_text()
#print(soup.text)


# In[6]:


all_links = soup.find_all("a")
#for link in all_links:
    #print(link.get("href"))


# In[7]:


rows = soup.find_all('tr')
print(rows[:5])


# In[8]:


for row in rows:
    row_td = row.find_all('td')
print(row_td)
type(row_td)


# In[9]:


import re

list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)
print(clean2)
type(clean2)


# In[10]:


df = pd.DataFrame(list_rows)
df.head(10)


# In[11]:


df1 = df[0].str.split(',', expand=True)
df1.head(10)


# In[12]:


df1[0] = df1[0].str.strip('[')
df1[4] = df1[4].str.strip(']')
df1.head(10)


# In[13]:


col_labels = soup.find_all('th')
print(col_labels)


# In[14]:


all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
print(all_header)


# In[15]:


df2 = pd.DataFrame(all_header)
df2 = df2[0].str.split(',', expand=True)


df2[0] = df2[0].str.strip('[')
df2[4] = df2[4].str.strip(']')




df2.head()


# In[16]:


frames = [df2, df1]

df3 = pd.concat(frames)
df3.head(10)


# In[17]:


df4 = df3.rename(columns=df3.iloc[0])
df4.head()


# In[18]:


df5 = df4.dropna(axis=0, how='any')
df5.head()


# In[19]:


df6 = df5.drop(df5.index[0])
df6.head()


# In[20]:


df7 = df6.drop(['S. No.'], axis = 1) 
df7


# Now we have the latest data, we will perform some visual analysis.

# # Data Visualization

# In[21]:


df7.columns


# In[22]:


import plotly.graph_objects as go

fig2 = go.Figure(
    data=[
        
        go.Bar(name="Number of cases",
            x=df7[" Name of State / UT"],
            y=df7[" Total Confirmed cases (Including 77 foreign Nationals) "],
               text=df7[" Total Confirmed cases (Including 77 foreign Nationals) "],
               textposition='auto',
            offsetgroup=0),
        
        
        go.Bar(name="Number of Deaths",
            x=df7[" Name of State / UT"],
            y=df7[" Death"],
               text=df7[" Death"],
               textposition='auto',
            offsetgroup=1),
        
       go.Bar(name="Cured/Recovered",
            x=df7[" Name of State / UT"],
            y=df7[" Cured/Discharged/Migrated"],
             text = df7[" Cured/Discharged/Migrated"],
            textposition='auto',
            offsetgroup=2), 
        
        
    ],
    layout=go.Layout(
        title="State wise Statistics",
        xaxis_title="States/Provinces",
        yaxis_title=" "
        
    )
)

fig2.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig2.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

fig2.show()


fig2.write_html('Covid-19 India.html', auto_open=True)


# In[23]:


len(df7)


# In[24]:


total  = 0
death_toll = 0
cured = 0

for i in range(int(len(df7))):
    total = total + int(df7[' Total Confirmed cases (Including 77 foreign Nationals) '][i+1])


for i in range(int(len(df7))):
    death_toll = death_toll + int(df7[' Death'][i+1])

for i in range(int(len(df7))):
    cured = cured + int(df7[' Cured/Discharged/Migrated'][i+1])


data = {'info':['Total cases','Deaths','Recovered'],'count':[total,death_toll,cured]}
frame = pd.DataFrame(data)
frame.head()


# In[25]:


fig = go.Figure(data=[go.Pie(labels=frame['info'], values=frame['count'], hole=.3)])
colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=10,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))


fig.show()
fig.write_html('Covid-19 summary.html', auto_open=True)


# In[ ]:




