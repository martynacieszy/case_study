#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import plotly.express as px

sales_NY = pd.read_json('sales_NY.json')
airbnb_NY = pd.read_json('airbnb_NY.json')

mean_sales = (sales_NY[['Borough', 'Price Per Square Ft']]
    .groupby('Borough')
    .agg('mean'))
mean_sales.columns = ['Mean price per square ft']
mean_sales = mean_sales.sort_values('Mean price per square ft', ascending=False)
mean_sales['Mean price per square ft'] = mean_sales['Mean price per square ft'].round(2)
sales_fig = px.pie(mean_sales, values = "Mean price per square ft", names = mean_sales.index, 
             title = "Average price per apartament in each district of New York")

def mean_rent_func(airbnb_NY, room_type):
    mean_rent = (airbnb_NY[airbnb_NY['Room Type'] == room_type][['Borough', 'Price']]
        .groupby('Borough')
        .agg('mean'))
    mean_rent.columns = ['Mean rent rate']
    mean_rent = mean_rent.sort_values('Mean rent rate', ascending=False)
    mean_rent['Mean rent rate'] = mean_rent['Mean rent rate'].round(2)

    rent_fig = px.pie(mean_rent, values = "Mean rent rate", names = mean_rent.index, 
                         title = "Average rent price per " + str.lower(room_type) + " in each district of New York")
    
    return rent_fig, mean_rent


def fig_neighborhood_by_brough(sales_NY, brough_name):
    mean_sales_n = (sales_NY[sales_NY['Borough'] == brough_name][['Neighborhood', 'Price Per Square Ft']]
    .groupby('Neighborhood')
    .agg(['mean']))
    mean_sales_n.columns = mean_sales_n.columns.droplevel()
    mean_sales_n.columns = ['Mean price per square ft']
    mean_sales_n = mean_sales_n.sort_values('Mean price per square ft', ascending=False)
    fig = px.bar(mean_sales_n, x = "Mean price per square ft", y = mean_sales_n.index,
              title = "Average price per apartament in each neighborhood of " + str(brough_name))
    return fig

def fig_neighborhood_by_brough_rent(airbnb_NY, brough_name):
    mean_sales_n = (airbnb_NY[airbnb_NY['Borough'] == brough_name][['Neighborhood', 'Price']]
    .groupby('Neighborhood')
    .agg(['mean']))
    mean_sales_n.columns = mean_sales_n.columns.droplevel()
    mean_sales_n.columns = ['Mean rent price']
    mean_sales_n = mean_sales_n.sort_values('Mean rent price', ascending=False)
    fig = px.bar(mean_sales_n, x = "Mean rent price", y = mean_sales_n.index,
              title = "Average rent price per apartament in each neighborhood of " + str(brough_name))
    return fig


import streamlit as st
from streamlit_jupyter import StreamlitPatcher, tqdm
StreamlitPatcher().jupyter() 

st.write(""" 
# My first app 
Hello *word!*
""")

boroughs = sales_NY["Borough"].unique()

st.write(sales_fig)

for i in boroughs:
    check_i = st.checkbox(i)
    if check_i:
        st.write(fig_neighborhood_by_brough(sales_NY, i))

