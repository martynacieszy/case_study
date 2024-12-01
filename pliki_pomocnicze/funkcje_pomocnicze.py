#!/usr/bin/env python
# coding: utf-8

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
        title="Wykres: Średnia cena stopy kwadratowej w poszczególnych dzielnicach Nowego Jorku",
    )
    sales_fig.update_traces(textinfo="value")

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
        title="Wykres: Średnia cena wynajmu w poszczególnych dzielnicach Nowego Jorku",
    )
    rent_fig.update_traces(textinfo="value")

    return rent_fig, mean_rent


def average_price(sales_NY, airbnb_NY, borough_name):
    mean_sales_n = (
        sales_NY[sales_NY["Borough"] == borough_name][
            ["Neighborhood", "Price Per Square Ft"]
        ]
        .groupby("Neighborhood")
        .agg(["mean"])
    )
    mean_sales_n.columns = mean_sales_n.columns.droplevel()
    mean_sales_n.columns = ["Średnia cena stopy kwadratowej"]
    mean_sales_n = mean_sales_n.sort_values(
        "Średnia cena stopy kwadratowej", ascending=False
    )
    mean_sales_n["Średnia cena stopy kwadratowej"] = mean_sales_n[
        "Średnia cena stopy kwadratowej"
    ].round(2)
    fig = px.bar(
        mean_sales_n,
        x="Średnia cena stopy kwadratowej",
        y=mean_sales_n.index,
        labels={"Neighborhood": "Osiedle"},
        title="Wykres: Średnia cena stopy kwadratowej (wykres słupkowy) i wynajmu (wykres punktowy)<br>dla każdego z osiedli w dzielnicy "
        + str(borough_name),
    )
    fig.update_traces(marker={"color": "#FFABAB"})
    fig.update_layout(xaxis_title='Średnia cena stopy kwadratowej', yaxis_title='Osiedle')

    mean_rent_n = (
        airbnb_NY.loc[airbnb_NY["Borough"] == borough_name][["Neighborhood", "Price"]]
        .groupby("Neighborhood")
        .agg(["mean"])
    )
    mean_rent_n.columns = mean_rent_n.columns.droplevel()
    mean_rent_n.columns = ["Średnia cena wynajmu"]
    mean_rent_n = mean_rent_n.sort_values("Średnia cena wynajmu", ascending=False)
    mean_rent_n["Średnia cena wynajmu"] = mean_rent_n["Średnia cena wynajmu"].round(2)
    fig2 = px.scatter(
        mean_rent_n,
        x="Średnia cena wynajmu",
        y=mean_rent_n.index,
        labels={"Neighborhood": "Osiedle"},
        color="Średnia cena wynajmu",
    )

    try:
        fig.add_trace(fig2.data[0])
    except:
        pass

    return fig


def map_airbnb(airbnb_NY):
    px.set_mapbox_access_token(open("pliki_pomocnicze/mapbox_token").read())
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
        height=700,
    )
    names = {
        "Latitude": "Szerokość geograficzna",
        "Longitude": "Długość geograficzna",
        "Neighborhood": "Osiedle",
        "Price": "Cena wynajmu",
        "Name": "Nazwa obiektu",
    }
    for i in names:
        fig.for_each_trace(
            lambda t: t.update(hovertemplate=t.hovertemplate.replace(i, names[i]))
        )
    fig.update_layout(legend_title_text=names["Neighborhood"])

    return fig
