#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import plotly.express as px

sales_NY = pd.read_csv('Property_sales_data_New_York.csv')
airbnb_NY = pd.read_csv('Airbnb_data_New_York.csv')

sales_NY.head(10)

sales_NY.info()



airbnb_NY.head(10)

airbnb_NY.info()

sales_NY = sales_NY.drop(columns=['Unnamed: 0'])

sales_NY.drop_duplicates()
airbnb_NY.drop_duplicates()

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

sales_NY["PRICE PER SQUARE FT"] = round(sales_NY["SALE PRICE"] / sales_NY["GROSS SQUARE FEET"],2)
airbnb_NY['neighbourhood'] = airbnb_NY['neighbourhood'].str.upper()

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

sales_NY = sales_NY[['BOROUGH NAME', 'Neighborhood', 'BUILDING CLASS CATEGORY',
       'TAX CLASS AT PRESENT', 'BLOCK', 'LOT', 'EASE-MENT',
       'BUILDING CLASS AT PRESENT', 'ADDRESS', 'APARTMENT NUMBER', 'ZIP CODE',
       'RESIDENTIAL UNITS', 'COMMERCIAL UNITS', 'TOTAL UNITS',
       'LAND SQUARE FEET', 'GROSS SQUARE FEET', 'YEAR BUILT',
       'TAX CLASS AT TIME OF SALE', 'BUILDING CLASS AT TIME OF SALE',
       'SALE PRICE', 'SALE DATE', 'PRICE PER SQUARE FT']].copy()

sales_NY = sales_NY.rename(str.title, axis='columns')
sales_NY = sales_NY.rename(columns = {"Borough Name" : "Borough"})
sales_NY['Address'] = sales_NY['Address'].str.title()
sales_NY['Building Class Category'] = sales_NY['Building Class Category'].str.title()
sales_NY["Sale Date"] = pd.to_datetime(sales_NY["Sale Date"])

for i in range(0, len(sales_NY["Neighborhood"])-1):
    if sales_NY["Neighborhood"][i] not in Neighborhoods_list:
        sales_NY = sales_NY.drop(index = i)
sales_NY = sales_NY.reset_index()
sales_NY['Neighborhood'] = sales_NY['Neighborhood'].str.title()
sales_NY = sales_NY.drop(columns=['index'])

airbnb_NY = airbnb_NY[['Neighborhood', 'name', 'host_id', 'host_name', 'neighbourhood_group',
       'neighbourhood', 'latitude', 'longitude', 'room_type', 'price',
       'minimum_nights', 'number_of_reviews', 'last_review',
       'reviews_per_month', 'calculated_host_listings_count',
       'availability_365']].copy()

airbnb_NY = airbnb_NY.rename(columns = {"neighbourhood_group" : "Borough"})
airbnb_NY.columns = airbnb_NY.columns.str.replace("_", " ", regex=True).str.title()
for i in range(0, len(airbnb_NY['Neighborhood'])-1):
    if airbnb_NY['Neighborhood'][i] not in Neighborhoods_list:
        airbnb_NY = airbnb_NY.drop(index = i)
airbnb_NY = airbnb_NY.reset_index()
airbnb_NY['Neighborhood'] = airbnb_NY['Neighborhood'].str.title()

airbnb_NY = airbnb_NY.drop(columns=['index'])

sales_NY.to_csv('sales_NY.csv', index=False)
airbnb_NY.to_csv('airbnb_NY.csv', index=False)

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

