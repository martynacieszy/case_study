#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
from streamlit_jupyter import StreamlitPatcher, tqdm


sales_NY = pd.read_csv('Property_sales_data_New_York.csv')
airbnb_NY = pd.read_csv('Airbnb_data_New_York.csv')

sales_NY = sales_NY.drop(columns=['Unnamed: 0'])

brough_names = {1: "Manhattan",
2: "Bronx",
3: "Brooklyn",
4: "Queens",
5: "Staten Island"}

for i in list(brough_names.keys()):
    sales_NY.loc[sales_NY["BOROUGH"] == i, "BOROUGH NAME"] = brough_names[i]
    
sales_NY["SALE PRICE"] = sales_NY["SALE PRICE"].str.replace('\D', "", regex=True)
sales_NY = sales_NY[sales_NY["SALE PRICE"] != ""]
sales_NY = sales_NY.reset_index()

sales_NY["GROSS SQUARE FEET"] = sales_NY["GROSS SQUARE FEET"].str.replace('\D', "", regex=True)
sales_NY = sales_NY[np.logical_and(sales_NY["GROSS SQUARE FEET"] != "", sales_NY["GROSS SQUARE FEET"] != "0")]
sales_NY = sales_NY.reset_index()
sales_NY = sales_NY.drop(columns=['level_0'])

sales_NY["LAND SQUARE FEET"] = sales_NY["LAND SQUARE FEET"].str.replace('\D', "", regex=True)
sales_NY = sales_NY[np.logical_and(sales_NY["LAND SQUARE FEET"] != "", sales_NY["LAND SQUARE FEET"] != "0")]
sales_NY = sales_NY.reset_index()
sales_NY = sales_NY.drop(columns=['level_0'])

for column in list(sales_NY.columns):
    try:
        sales_NY[column] = sales_NY[column].apply(pd.to_numeric)
    except:
        pass

sales_NY["PRICE PER SQUARE FT"] = sales_NY["SALE PRICE"] / sales_NY["GROSS SQUARE FEET"]

mean_sales = (sales_NY[['BOROUGH NAME', 'PRICE PER SQUARE FT']]
    .groupby('BOROUGH NAME')
    .agg(['mean', 'median']))
mean_sales.columns = mean_sales.columns.droplevel()
mean_sales.columns = ['mean_price_per_sq_ft', 'median_price_per_sq_ft']
mean_sales = mean_sales.sort_values('mean_price_per_sq_ft', ascending=False)
mean_sales['mean_price_per_sq_ft'] = mean_sales['median_price_per_sq_ft'].round(2)

sales_fig = px.pie(mean_sales, values = "mean_price_per_sq_ft", names = mean_sales.index, 
             title = "Average price per apartament in each district of New York")

airbnb_NY['neighbourhood'] = airbnb_NY['neighbourhood'].str.upper()

mean_rent = (airbnb_NY[airbnb_NY['room_type'] == "Private room"][['neighbourhood_group', 'price']]
    .groupby('neighbourhood_group')
    .agg('mean'))
#mean_rent.columns = mean_rent.columns.droplevel()
mean_rent.columns = ['Mean rent rate']
mean_rent = mean_rent.sort_values('Mean rent rate', ascending=False)

rent_fig = px.pie(mean_rent, values = "Mean rent rate", names = mean_sales.index, title = "Average rent price per room in each district of New York")

sales_NY["NEIGHBORHOOD"] = sales_NY["NEIGHBORHOOD"].str.replace("'", "", regex=True)
sales_NY["NEIGHBORHOOD"] = sales_NY["NEIGHBORHOOD"].str.replace("-", " ", regex=True)
sales_NY = sales_NY.reset_index()
try: 
    sales_NY = sales_NY.drop(columns=['level_0','index'])
except:
    pass

airbnb_NY['neighbourhood'] = airbnb_NY['neighbourhood'].str.replace("'", "", regex=True)
airbnb_NY["neighbourhood"] = airbnb_NY["neighbourhood"].str.replace("-", " ", regex=True)
airbnb_NY = airbnb_NY.reset_index()
try: 
    airbnb_NY = airbnb_NY.drop(columns=['level_0','index'])
except:
    pass

sales_NY["Neighborhood"] = sales_NY["NEIGHBORHOOD"]
airbnb_NY["Neighborhood"] = airbnb_NY['neighbourhood']

Neighborhood_dict = {'BAY TERRACE' : 'BAY TERRACE, STATEN ISLAND',
             'CASTLE HILL' : 'CASTLE HILL/UNIONPORT',
             'UNIONPORT' : 'CASTLE HILL/UNIONPORT',
             'FLATBUSH CENTRAL' : 'FLATBUSH',
             'FLATBUSH EAST' : 'EAST FLATBUSH',
             'FLATBUSH LEFFERTS GARDEN' : 'FLATBUSH',
             'FLATBUSH NORTH' : 'FLATBUSH',
             'FLUSHING NORTH' : 'FLUSHING',
             'FLUSHING SOUTH' : 'FLUSHING',
             'FLATIRON DISTRICT' : 'FLATIRON',
             'FINANCIAL DISTRICT' : 'FINANCIAL',
             'GREENWICH VILLAGE CENTRAL' : 'GREENWICH VILLAGE',
             'GREENWICH VILLAGE WEST' : 'GREENWICH VILLAGE',
             'EAST HARLEM' : 'HARLEM EAST',
             'HARLEM CENTRAL' : 'HARLEM',
             'HARLEM UPPER' : 'HARLEM',
             'HARLEM WEST' : 'HARLEM',
             'HIGHBRIDGE' : 'HIGHBRIDGE/MORRIS HEIGHTS',
             'MORRIS HEIGHTS' : 'HIGHBRIDGE/MORRIS HEIGHTS',
             'KINGSBRIDGE' : 'KINGSBRIDGE/JEROME PARK',
             'MELROSE' : 'MELROSE/CONCOURSE',
             'CONCOURSE' : 'MELROSE/CONCOURSE',
             'MIDTOWN CBD' : 'MIDTOWN',
             'MIDTOWN EAST' : 'MIDTOWN',
             'MIDTOWN WEST'  : 'MIDTOWN',
             'VAN NEST' : 'MORRIS PARK/VAN NEST',
             'MORRIS PARK' : 'MORRIS PARK/VAN NEST',
             'MOUNT HOPE' : 'MOUNT HOPE/MOUNT EDEN',
             'MOUNT EDEN' : 'MOUNT HOPE/MOUNT EDEN',
             'MORRISANIA' : 'MORRISANIA/LONGWOOD',
             'LONGWOOD' : 'MORRISANIA/LONGWOOD',
             'MOTT HAVEN' : 'MOTT HAVEN/PORT MORRIS',
             'PORT MORRIS' : 'MOTT HAVEN/PORT MORRIS',
             'SCHUYLERVILLE' : 'SCHUYLERVILLE/PELHAM BAY',
             'PELHAM BAY' : 'SCHUYLERVILLE/PELHAM BAY',
             'UPPER EAST SIDE (59 79)' : 'UPPER EAST SIDE',
             'UPPER EAST SIDE (79 96)' : 'UPPER EAST SIDE',
             'UPPER EAST SIDE (96 110)' : 'UPPER EAST SIDE',
             'UPPER WEST SIDE (59 79)' : 'UPPER WEST SIDE',
             'UPPER WEST SIDE (79 96)' : 'UPPER WEST SIDE',
             'UPPER WEST SIDE (96 116)' : 'UPPER WEST SIDE',
             'WASHINGTON HEIGHTS LOWER' : 'WASHINGTON HEIGHTS',
             'WASHINGTON HEIGHTS UPPER' : 'WASHINGTON HEIGHTS',
             'WILLIAMSBURG CENTRAL' : 'WILLIAMSBURG',
             'WILLIAMSBURG EAST' : 'WILLIAMSBURG',
             'WILLIAMSBURG NORTH' : 'WILLIAMSBURG',
             'WILLIAMSBURG SOUTH' : 'WILLIAMSBURG'
            }

for i in list(Neighborhood_dict.keys()):
    if i in set(sales_NY["Neighborhood"]):
        sales_NY.loc[sales_NY["NEIGHBORHOOD"] == i, "Neighborhood"] = Neighborhood_dict[i]
    elif i in set(airbnb_NY['Neighborhood']):
        airbnb_NY.loc[airbnb_NY['Neighborhood'] == i, "Neighborhood"] = Neighborhood_dict[i]
        
Neighborhoods_list = list(set(sales_NY["Neighborhood"]).intersection(set(airbnb_NY['Neighborhood'])))
Neighborhoods_list.sort()

def fig_neighborhood_by_brough(brough_name):
    mean_sales_n = (sales_NY[sales_NY['BOROUGH NAME'] == brough_name][['Neighborhood', 'PRICE PER SQUARE FT']]
    .groupby('Neighborhood')
    .agg(['mean']))
    mean_sales_n.columns = mean_sales_n.columns.droplevel()
    mean_sales_n.columns = ['Mean price per square ft']
    mean_sales_n = mean_sales_n.sort_values('Mean price per square ft', ascending=False)
    fig = px.bar(mean_sales_n, x = "Mean price per square ft", y = mean_sales_n.index,
              title = "Average price per apartament in each neighborhood of " + str(brough_name))
    return fig

def fig_neighborhood_by_brough_rent(brough_name):
    mean_sales_n = (airbnb_NY[airbnb_NY['Neighborhood_group'] == brough_name][['Neighborhood', 'price']]
    .groupby('Neighborhood')
    .agg(['mean']))
    mean_sales_n.columns = mean_sales_n.columns.droplevel()
    mean_sales_n.columns = ['Mean rent price']
    mean_sales_n = mean_sales_n.sort_values('Mean rent price', ascending=False)
    fig = px.bar(mean_sales_n, x = "Mean rent price", y = mean_sales_n.index,
              title = "Average rent price per apartament in each neighborhood of " + str(brough_name))
    return fig






dropdown = widgets.Dropdown(
    options=list(set(sales_NY['BOROUGH NAME'])),
    value=sales_NY['BOROUGH NAME'][0],
    description='Brough:',
    disabled=False,
)
display(dropdown)


# In[ ]:


fig_neighborhood_by_brough(dropdown.value)


StreamlitPatcher().jupyter() 

st.write(""" 
# My first app 
Hello *word!*
""")



