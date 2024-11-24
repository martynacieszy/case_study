#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import plotly.express as px


def sales_figure(sales_NY):
    mean_sales = (
        sales_NY[["Borough", "Price Per Square Ft"]].groupby("Borough").agg("mean")
    )
    mean_sales.columns = ["Mean price per square ft"]
    mean_sales = mean_sales.sort_values("Mean price per square ft", ascending=False)
    mean_sales["Mean price per square ft"] = mean_sales[
        "Mean price per square ft"
    ].round(2)
    sales_fig = px.pie(
        mean_sales,
        values="Mean price per square ft",
        names=mean_sales.index,
        title="Figure: Average price per square feet in apartment in each district of New York",
    )
    # sales_figure.update_traces(textinfo='value')

    return sales_fig


def mean_rent_func(airbnb_NY):
    mean_rent = airbnb_NY[["Borough", "Price"]].groupby("Borough").agg("mean")
    mean_rent.columns = ["Mean rent rate"]
    mean_rent = mean_rent.sort_values("Mean rent rate", ascending=False)
    mean_rent["Mean rent rate"] = mean_rent["Mean rent rate"].round(2)
    rent_fig = px.pie(
        mean_rent,
        values="Mean rent rate",
        names=mean_rent.index,
        title="Figure: Average rent price in each district of New York",
    )
    # rent_fig.update_traces(marker={textinfo='value'})

    return rent_fig, mean_rent


def average_price(sales_NY, airbnb_NY, borough_name, room_type, room_type2, room_type3):
    mean_sales_n = (
        sales_NY[sales_NY["Borough"] == borough_name][
            ["Neighborhood", "Price Per Square Ft"]
        ]
        .groupby("Neighborhood")
        .agg(["mean"])
    )
    mean_sales_n.columns = mean_sales_n.columns.droplevel()
    mean_sales_n.columns = ["Mean price per square ft"]
    mean_sales_n = mean_sales_n.sort_values("Mean price per square ft", ascending=False)
    mean_sales_n["Mean price per square ft"] = mean_sales_n[
        "Mean price per square ft"
    ].round(2)
    fig = px.bar(
        mean_sales_n,
        x="Mean price per square ft",
        y=mean_sales_n.index,
        title="Figure: Average price per square feet (bar plot) and renting (scatter plot) in each neighborhood of "
        + str(borough_name),
    )
    fig.update_traces(marker={"color": "#FFABAB"})

    mean_rent_n = (
        airbnb_NY.loc[
            np.logical_and(
                airbnb_NY["Borough"] == borough_name,
                np.logical_or.reduce(
                    (
                        airbnb_NY["Room Type"] == room_type,
                        airbnb_NY["Room Type"] == room_type2,
                        airbnb_NY["Room Type"] == room_type3,
                    )
                ),
            )
        ][["Neighborhood", "Price"]]
        .groupby("Neighborhood")
        .agg(["mean"])
    )
    mean_rent_n.columns = mean_rent_n.columns.droplevel()
    mean_rent_n.columns = ["Mean rent price"]
    mean_rent_n = mean_rent_n.sort_values("Mean rent price", ascending=False)
    mean_rent_n["Mean rent price"] = mean_rent_n["Mean rent price"].round(2)
    fig2 = px.scatter(
        mean_rent_n,
        x="Mean rent price",
        y=mean_rent_n.index,
        color="Mean rent price",
        labels={"Mean rent price ": "Average rent price per apartament"},
    )
    try:
        fig.add_trace(fig2.data[0])
    except:
        pass

    return fig


def map_airbnb(airbnb_NY):
    px.set_mapbox_access_token(open("mapbox_token").read())
    df = airbnb_NY
    fig = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Neighborhood",
        size="Price",
        text="Name",
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=15,
        zoom=10,
    )
    return fig
