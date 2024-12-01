#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import streamlit as st
from pliki_pomocnicze.funkcje_pomocnicze import (
    sales_figure,
    mean_rent_func,
    average_price,
    map_airbnb,
)
from streamlit_jupyter import StreamlitPatcher

st.set_page_config(layout="wide")

StreamlitPatcher().jupyter()

# Wczytaj przekształcone dane
sales_NY = pd.read_json("dane_przeksztalcone/sales_NY.json")
airbnb_NY = pd.read_json("dane_przeksztalcone/airbnb_NY.json")

# Utworzenie trzech zakładek
tab1, tab2 = st.tabs(["Wykresy", "Mapa z mieszkaniami na wynajem"])

boroughs = sales_NY["Borough"].unique()
all_neighborhoods = sales_NY["Neighborhood"].unique()
borough_neigh_dict = dict(zip(sales_NY["Neighborhood"], sales_NY["Borough"]))

# Zdafiniowanie paska bocznego
with st.sidebar:
    st.write(
        """ ### Analiza rynku nieruchomości w Nowym Jorku: kupno i wynajem mieszkań """
    )
    st.write("Dzielnica:")
    Manhattan = st.checkbox("Manhattan", value=True)
    Bronx = st.checkbox("Bronx", value=True)
    Brooklyn = st.checkbox("Brooklyn", value=True)
    Queens = st.checkbox("Queens", value=True)
    Staten_Island = st.checkbox("Staten Island", value=True)

    boroughs_checkbox = {
        "Manhattan": Manhattan,
        "Bronx": Bronx,
        "Brooklyn": Brooklyn,
        "Queens": Queens,
        "Staten Island": Staten_Island,
    }

    building_types = list(sales_NY["Building Class Category"].unique())
    chosen_building_types = st.multiselect(
        "Wybrane typ obiektu do kupienia:",
        building_types,
        placeholder="Wybierz typ obiektu",
        default=[
            "01 One Family Dwellings",
            "02 Two Family Dwellings",
            "03 Three Family Dwellings",
            "07 Rentals - Walkup Apartments",
            "08 Rentals - Elevator Apartments",
            "09 Coops - Walkup Apartments",
            "14 Rentals - 4-10 Unit",
        ],
    )
    
    if len(chosen_building_types) != 0:
        sales_NY = sales_NY[sales_NY["Building Class Category"].isin(chosen_building_types)]

    area = st.slider(
        "Powierzchnia lokalu na sprzedaż (w stopach kwadratowych):",
        value=[min(sales_NY["Gross Square Feet"]), max(sales_NY["Gross Square Feet"])],
        step=1,
    )
    st.write("Rodzaj obiektu na wynajem:")
    check_sr = st.checkbox("Pokój współdzielony", value=True)
    check_pr = st.checkbox("Pokój prywatny", value=True)
    check_ent = st.checkbox("Cały dom/apartament", value=True)

    min_nights = st.slider(
        "Ilość nocy wynajmu:",
        value=[min(airbnb_NY["Minimum Nights"]), max(airbnb_NY["Minimum Nights"])],
        step=1,
    )
    min_avail = st.slider(
        "Dostepność obiektu w dniach w ciągu roku:",
        value=[min(airbnb_NY["Availability 365"]), max(airbnb_NY["Availability 365"])],
        step=1,
    )
    min_rev = st.slider(
        "Ilość recenzji obiektu:",
        value=[
            min(airbnb_NY["Number Of Reviews"]),
            max(airbnb_NY["Number Of Reviews"]),
        ],
        step=1,
    )

    all_neighborhoods.sort()
    chosen_areas = st.multiselect(
        "Wybrane osiedla do porównania:",
        all_neighborhoods,
        placeholder="Wybierz osiedla",
    )


# Filtrowanie ramek danych na podstawie widgetów
sales_NY = sales_NY[
    np.logical_and(
        sales_NY["Gross Square Feet"] > area[0], sales_NY["Gross Square Feet"] < area[1]
    )
]
airbnb_NY = airbnb_NY[
    np.logical_and(
        airbnb_NY["Minimum Nights"] > min_nights[0],
        airbnb_NY["Minimum Nights"] < min_nights[1],
    )
]
airbnb_NY = airbnb_NY[
    np.logical_and(
        airbnb_NY["Availability 365"] > min_avail[0],
        airbnb_NY["Availability 365"] < min_avail[1],
    )
]
airbnb_NY = airbnb_NY[
    np.logical_and(
        airbnb_NY["Number Of Reviews"] > min_rev[0],
        airbnb_NY["Number Of Reviews"] < min_rev[1],
    )
]

if not check_sr:
    airbnb_NY = airbnb_NY[~(airbnb_NY["Room Type"] == "Shared room")]
if not check_pr:
    airbnb_NY = airbnb_NY[~(airbnb_NY["Room Type"] == "Private room")]
if not check_ent:
    airbnb_NY = airbnb_NY[~(airbnb_NY["Room Type"] == "Entire home/apt")]

# Zdefiniowanie pierwszej zakładki
with tab1:
    # Expander z wykresami średnich cen w poszczególnych dzielnicach
    with st.expander("Średnie ceny w poszczególnych dzielnicach", expanded=True):
        # Średnie ceny kupna
        st.markdown(
            ":red[Średnia cena stopy kwadratowej w Nowym Jorku wynosi **"
            + str(sales_NY.describe()["Price Per Square Ft"]["mean"].round(2))
            + "**.]"
        )

        st.plotly_chart(sales_figure(sales_NY), use_container_width=True)

        # Średnie ceny wynajmu
        st.markdown(
            ":red[Średnia cena wynajmu na Airbnb w Nowym Jorku wynosi **"
            + str(airbnb_NY.describe()["Price"]["mean"].round(2))
            + "**.]"
        )
        st.plotly_chart(mean_rent_func(airbnb_NY)[0], use_container_width=True)

    # Expander z wykresem średnich cen w poszczególnych osiedlach
    for i in boroughs_checkbox:
        if boroughs_checkbox[i]:
            with st.expander(
                "Średnie ceny dla poszczególnych osiedli w dzielnicy " + i,
                expanded=True,
            ):
                st.plotly_chart(
                    average_price(
                        sales_NY,
                        airbnb_NY,
                        i,
                    ),
                    use_container_width=True,
                )

    # Expander z ramką danych do porównania osiedli
    with st.expander(
        "Tutaj możesz porównać średnie ceny dla wybranych osiedli:", expanded=True
    ):

        areas_df = pd.DataFrame(
            columns=[
                "Borough",
                "Land Square Feet",
                "Gross Square Feet",
                "Year Built",
                "Sale Price",
                "Price Per Square Ft",
                "Price Per Rental",
                "Price Per Square Ft/Price Per Rental",
                "Availability 365",
                "Price Per Rental*Availability 365",
            ]
        )

        for i in range(0, len(chosen_areas)):
            areas_df = areas_df.append(chosen_areas, ignore_index=True)
            col_list = [
                "Land Square Feet",
                "Gross Square Feet",
                "Sale Price",
                "Price Per Square Ft",
            ]
            describe_df = sales_NY[
                sales_NY["Neighborhood"] == chosen_areas[i]
            ].describe()[
                [
                    "Land Square Feet",
                    "Gross Square Feet",
                    "Sale Price",
                    "Price Per Square Ft",
                ]
            ]
            for j in col_list:
                areas_df.loc[areas_df[0] == chosen_areas[i], j] = float(
                    describe_df[describe_df.index == "mean"][j].round(2)
                )
        if len(areas_df) > 0:
            areas_df = areas_df.rename(columns={0: "Neighborhood"})
            dict_b = borough_neigh_dict
            areas_df = areas_df.drop_duplicates(subset="Neighborhood")
            for i in range(0, len(areas_df["Neighborhood"])):
                areas_df["Borough"].iloc[i] = dict_b[areas_df["Neighborhood"][i]]
            for i in range(0, len(areas_df["Neighborhood"])):
                areas_df["Price Per Rental"].iloc[i] = (
                    airbnb_NY[
                        airbnb_NY["Neighborhood"] == areas_df["Neighborhood"].iloc[i]
                    ]
                    .describe()["Price"]["mean"]
                    .round(2)
                )
            for i in range(0, len(areas_df["Neighborhood"])):
                areas_df["Year Built"].iloc[i] = (
                    sales_NY[
                        sales_NY["Neighborhood"] == areas_df["Neighborhood"].iloc[i]
                    ]
                    .describe()["Year Built"]["mean"]
                    .round()
                )
            areas_df["Price Per Square Ft/Price Per Rental"] = (
                areas_df["Price Per Square Ft"] / areas_df["Price Per Rental"]
            )
            areas_df["Price Per Square Ft/Price Per Rental"] = areas_df[
                "Price Per Square Ft/Price Per Rental"
            ]
            for i in range(0, len(areas_df["Neighborhood"])):
                areas_df["Availability 365"].iloc[i] = (
                    airbnb_NY[
                        airbnb_NY["Neighborhood"] == areas_df["Neighborhood"].iloc[i]
                    ]
                    .describe()["Availability 365"]["mean"]
                    .round()
                )
            areas_df["Price Per Rental*Availability 365"] = (
                areas_df["Price Per Rental"] * areas_df["Availability 365"]
            )

            # Zmiana ukladu kolumn
            areas_df = areas_df[
                [
                    "Borough",
                    "Neighborhood",
                    "Land Square Feet",
                    "Gross Square Feet",
                    "Year Built",
                    "Sale Price",
                    "Price Per Square Ft",
                    "Price Per Rental",
                    "Price Per Square Ft/Price Per Rental",
                    "Availability 365",
                    "Price Per Rental*Availability 365",
                ]
            ]

            # Przetlumaczenie nazw kolumn na polski
            areas_df = areas_df.rename(
                columns={
                    "Neighborhood": "Osiedle",
                    "Borough": "Dzielnica",
                    "Land Square Feet": "Pow. działki [ft2]",
                    "Gross Square Feet": "Całkowita pow. [ft2]",
                    "Year Built": "Rok budowy",
                    "Sale Price": "Cena sprzedaży",
                    "Price Per Square Ft": "Cena stopy kwadratowej",
                    "Price Per Rental": "Cena wynajmu",
                    "Price Per Square Ft/Price Per Rental": "Cena stopy kwadratowej/Cena wynajmu",
                    "Availability 365": "Dostępność wynajmu w roku [dni]",
                    "Price Per Rental*Availability 365": "Cena wynajmu*Dostępność",
                }
            )
        with st.container():
            if len(chosen_areas) == 0:
                st.write("Wybierz osiedla do porównania z menu bocznego.")
            else:
                areas_df = areas_df.sort_index()
                st.dataframe(
                    areas_df, use_container_width=True, hide_index=True, height=500
                )

# Zdefiniowanie trzeciej zakładki
with tab2:
    st.plotly_chart(map_airbnb(airbnb_NY), use_container_width=True)
