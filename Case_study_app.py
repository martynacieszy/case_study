#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import plotly.express as px

sales_NY = pd.read_json('sales_NY.json')
airbnb_NY = pd.read_json('airbnb_NY.json')

    
def sales_figure(sales_NY):
    mean_sales = (sales_NY[['Borough', 'Price Per Square Ft']]
        .groupby('Borough')
        .agg('mean'))
    mean_sales.columns = ['Mean price per square ft']
    mean_sales = mean_sales.sort_values('Mean price per square ft', ascending=False)
    mean_sales['Mean price per square ft'] = mean_sales['Mean price per square ft'].round(2)
    sales_fig = px.pie(mean_sales, values = "Mean price per square ft", names = mean_sales.index, 
                 title = "Figure: Average price per square feet in apartment in each district of New York")
    #sales_figure.update_traces(textinfo='value')
    
    return sales_fig

def mean_rent_func(airbnb_NY):
    mean_rent = (airbnb_NY[['Borough', 'Price']]
        .groupby('Borough')
        .agg('mean'))
    mean_rent.columns = ['Mean rent rate']
    mean_rent = mean_rent.sort_values('Mean rent rate', ascending=False)
    mean_rent['Mean rent rate'] = mean_rent['Mean rent rate'].round(2)
    rent_fig = px.pie(mean_rent, values = "Mean rent rate", names = mean_rent.index, 
                         title = "Figure: Average rent price in each district of New York")
    #rent_fig.update_traces(marker={textinfo='value'})
    
    return rent_fig, mean_rent


def fig_neighborhood_by_brough(sales_NY, brough_name):
    mean_sales_n = (sales_NY[sales_NY['Borough'] == brough_name][['Neighborhood', 'Price Per Square Ft']]
    .groupby('Neighborhood')
    .agg(['mean']))
    mean_sales_n.columns = mean_sales_n.columns.droplevel()
    mean_sales_n.columns = ['Mean price per square ft']
    mean_sales_n = mean_sales_n.sort_values('Mean price per square ft', ascending=False)
    fig = px.bar(mean_sales_n, x = "Mean price per square ft", y = mean_sales_n.index,
              title = "Figure: Average price per apartament in each neighborhood of " + str(brough_name))
    return fig

def fig_neighborhood_by_brough_rent(airbnb_NY, brough_name):
    mean_sales_n = (airbnb_NY[airbnb_NY['Borough'] == brough_name][['Neighborhood', 'Price']]
    .groupby('Neighborhood')
    .agg(['mean']))
    mean_sales_n.columns = mean_sales_n.columns.droplevel()
    mean_sales_n.columns = ['Mean rent price']
    mean_sales_n = mean_sales_n.sort_values('Mean rent price', ascending=False)
    fig = px.bar(mean_sales_n, x = "Mean rent price", y = mean_sales_n.index,
              title = "Figure: Average rent price per apartament in each neighborhood of " + str(brough_name))
    return fig

def average_price(sales_NY, airbnb_NY, borough_name, room_type, room_type2, room_type3):
    mean_sales_n = (sales_NY[sales_NY['Borough'] == borough_name][['Neighborhood', 'Price Per Square Ft']]
                    .groupby('Neighborhood')
                    .agg(['mean']))    
    mean_sales_n.columns = mean_sales_n.columns.droplevel()
    mean_sales_n.columns = ['Mean price per square ft']
    mean_sales_n = mean_sales_n.sort_values('Mean price per square ft', ascending=False)
    mean_sales_n['Mean price per square ft'] = mean_sales_n['Mean price per square ft'].round(2)
    fig = px.bar(mean_sales_n, x = "Mean price per square ft", y = mean_sales_n.index, 
              title = "Figure: Average price per square feet (bar plot) and renting (scatter plot) in each neighborhood of " + str(borough_name))
    fig.update_traces(marker={"color":"#FFABAB"})
    
    mean_rent_n = (airbnb_NY.loc[np.logical_and(airbnb_NY['Borough'] == borough_name, 
                                                np.logical_or.reduce((airbnb_NY['Room Type'] == room_type,
                                                                     airbnb_NY['Room Type'] == room_type2,
                                                                     airbnb_NY['Room Type'] == room_type3)))]
                   [['Neighborhood', 'Price']]
                   .groupby('Neighborhood')
                   .agg(['mean']))
    mean_rent_n.columns = mean_rent_n.columns.droplevel()
    mean_rent_n.columns = ['Mean rent price']
    mean_rent_n = mean_rent_n.sort_values('Mean rent price', ascending=False)
    mean_rent_n['Mean rent price'] = mean_rent_n['Mean rent price'].round(2)
    fig2 = px.scatter(mean_rent_n, x = "Mean rent price", y = mean_rent_n.index, color = "Mean rent price",
                      labels = { "Mean rent price " : "Average rent price per apartament"})
    try:
        fig.add_trace(fig2.data[0])
    except:
        pass
        
    return fig

import streamlit as st
from streamlit_jupyter import StreamlitPatcher, tqdm
StreamlitPatcher().jupyter() 
tab1, tab2 = st.tabs(["Graphs","Areas comparison"])
  
boroughs = sales_NY["Borough"].unique()

with st.sidebar:
    st.write(""" ### New York estate market analysis: buying and renting an apartment""")
    add_radio = st.radio(
        "Choose borough to see details about it:",
        (boroughs)
    )
    
    area = st.slider("What is the gross square feet area you are interested in buying?", value=[min(sales_NY["Gross Square Feet"]),max(sales_NY["Gross Square Feet"])],
                     step=1)
    st.write("What type of place are you interested in renting?")      
    check_sr = st.checkbox("Shared room")
    check_pr = st.checkbox("Private room")
    check_ent = st.checkbox("Entire home/apt")

    min_nights = st.slider("Number of minimum nights to rent a room/apartment:", value=[min(airbnb_NY["Minimum Nights"]),max(airbnb_NY["Minimum Nights"])],
                     step=1)
    min_rev = st.slider("Number of minimum reviews from renting of a room/apartment:", value=[min(airbnb_NY["Number Of Reviews"]),max(airbnb_NY["Number Of Reviews"])],
                     step=1)
    
    all_neighborhoods = sales_NY["Neighborhood"].unique()
    all_neighborhoods.sort()
    chosen_areas = st.multiselect("Choose neighborhoods for comparison:", all_neighborhoods)

     
sales_NY = sales_NY[np.logical_and(sales_NY["Gross Square Feet"] > area[0], sales_NY["Gross Square Feet"] < area[1])]
airbnb_NY = airbnb_NY[np.logical_and(airbnb_NY["Minimum Nights"] > min_nights[0], airbnb_NY["Minimum Nights"] < min_nights[1])]
airbnb_NY = airbnb_NY[np.logical_and(airbnb_NY["Number Of Reviews"] > min_rev[0], airbnb_NY["Number Of Reviews"] < min_rev[1])]

with tab1:
    with st.expander("Average prices for each borough", expanded=True):
        st.markdown(":red[Mean price per square feet in New York is **" + str(sales_NY.describe()["Price Per Square Ft"]["mean"].round(2)) + "**.]")

        st.plotly_chart(sales_figure(sales_NY), use_container_width=True)
        st.markdown(":red[Average price for rent in New York is **" + str(airbnb_NY.describe()["Price"]["mean"].round(2)) + "**.]")
        st.plotly_chart(mean_rent_func(airbnb_NY)[0], use_container_width=True)
    
    with st.expander("Average prices for each neighborhood in " + str(add_radio), expanded=True):
        for i in boroughs:
            with st.container():
                if add_radio == i:
                    if check_sr:
                        if check_pr:
                            if check_ent:
                                st.plotly_chart(average_price(sales_NY, airbnb_NY, i, "Shared room", "Private room", "Entire home/apt"), use_container_width=True)
                            else:
                                st.plotly_chart(average_price(sales_NY, airbnb_NY, i, "Shared room", "Private room", ""), use_container_width=True)
                        else:
                            st.plotly_chart(average_price(sales_NY, airbnb_NY, i, "Shared room", "", ""), use_container_width=True)
                    elif check_pr:
                        if check_ent:
                            st.plotly_chart(average_price(sales_NY, airbnb_NY, i, "", "Private room", "Entire home/apt"), use_container_width=True)
                        else:
                            st.plotly_chart(average_price(sales_NY, airbnb_NY, i, "", "Private room", ""), use_container_width=True)
                    elif check_ent:
                                st.plotly_chart(average_price(sales_NY, airbnb_NY, i, "", "", "Entire home/apt"), use_container_width=True)
                    else:
                        st.plotly_chart(average_price(sales_NY, airbnb_NY, i, "", "", ""), use_container_width=True)

with tab2:
    st.write("""**Here you can compare mean prices from chosen neighborhoods:**""")

    areas_df = pd.DataFrame(columns = ['Borough',
                                       'Land Square Feet', 
                                       'Gross Square Feet', 
                                       'Year Built', 
                                       'Sale Price', 
                                       'Price Per Square Ft'])
    for i in range(0,len(chosen_areas)):
        areas_df = areas_df.append(chosen_areas, ignore_index=True)
        col_list = ['Land Square Feet', 'Gross Square Feet', 'Year Built', 'Sale Price', 'Price Per Square Ft']
        describe_df = sales_NY[sales_NY["Neighborhood"] == chosen_areas[i]].describe()[['Land Square Feet', 'Gross Square Feet', 'Year Built',
           'Sale Price', 'Price Per Square Ft']]
        for j in col_list:
            areas_df.loc[areas_df[0] == chosen_areas[i], j] = float(describe_df[describe_df.index == "mean"][j].round(2))
    if len(areas_df) > 0:
        areas_df = areas_df.rename(columns={0 : "Neighborhood"})
        dict_b = {}
        for i in set(sales_NY["Neighborhood"]):
            dict_b[i] = sales_NY["Borough"][sales_NY["Neighborhood"] == i].unique()[0]
        areas_df = areas_df.drop_duplicates(subset="Neighborhood")
        for i in range(0, len(areas_df["Neighborhood"])):
            areas_df["Borough"].iloc[i] = dict_b[areas_df["Neighborhood"][i]]
        areas_df['Year Built'] = areas_df['Year Built'].astype(int)
        areas_df['Year Built'] = areas_df['Year Built'].astype(str)

    if len(chosen_areas) == 0:
        st.write("Choose neighborhoods for comparison in the sidebar.")
    else:
        st.write(areas_df)
