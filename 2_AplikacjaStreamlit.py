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

StreamlitPatcher().jupyter()

# Wczytaj przekształcone dane
sales_NY = pd.read_json("dane_przeksztalcone/sales_NY.json")
airbnb_NY = pd.read_json("dane_przeksztalcone/airbnb_NY.json")

# Utworzenie trzech zakładek
tab1, tab2, tab3 = st.tabs(
    ["Wykresy", "Porównanie osiedli", "Mapa z mieszkaniami na wynajem"]
)

boroughs = sales_NY["Borough"].unique()

# Zdafiniowanie paska bocznego
with st.sidebar:
    st.write(
        """ ### Analiza rynku nieruchomości w Nowym Jorku: kupno i wynajem mieszkań """
    )
    add_radio = st.radio("Dzielnica:", (boroughs))

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
        "Ilość nocny wnajmu obiektu:",
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

    all_neighborhoods = sales_NY["Neighborhood"].unique()
    all_neighborhoods.sort()
    chosen_areas = st.multiselect(
        "Wybrane osiedla do porównania:",
        all_neighborhoods,
        placeholder="Wybierz osiedla",
    )


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

# Zdefiniowanie pierwszej zakładki
with tab1:
    with st.expander("Średnie ceny w poszczególnych dzielnicach", expanded=True):
        st.markdown(
            ":red[Średnia cena stopy kwadratowej w Nowym Jorku wynosi **"
            + str(sales_NY.describe()["Price Per Square Ft"]["mean"].round(2))
            + "**.]"
        )

        st.plotly_chart(sales_figure(sales_NY), use_container_width=True)
        st.markdown(
            ":red[Średnia cena wynajmu na Airbnb w Nowym Jorku wynosi **"
            + str(airbnb_NY.describe()["Price"]["mean"].round(2))
            + "**.]"
        )
        st.plotly_chart(mean_rent_func(airbnb_NY)[0], use_container_width=True)

    with st.expander(
        "Średnie ceny dla poszczególnych osiedli w dzielnicy " + str(add_radio),
        expanded=True,
    ):
        for i in boroughs:
            with st.container():
                if add_radio == i:
                    if check_sr:
                        if check_pr:
                            if check_ent:
                                st.plotly_chart(
                                    average_price(
                                        sales_NY,
                                        airbnb_NY,
                                        i,
                                        "Shared room",
                                        "Private room",
                                        "Entire home/apt",
                                    ),
                                    use_container_width=True,
                                )
                            else:
                                st.plotly_chart(
                                    average_price(
                                        sales_NY,
                                        airbnb_NY,
                                        i,
                                        "Shared room",
                                        "Private room",
                                        "",
                                    ),
                                    use_container_width=True,
                                )
                        else:
                            st.plotly_chart(
                                average_price(
                                    sales_NY, airbnb_NY, i, "Shared room", "", ""
                                ),
                                use_container_width=True,
                            )
                    elif check_pr:
                        if check_ent:
                            st.plotly_chart(
                                average_price(
                                    sales_NY,
                                    airbnb_NY,
                                    i,
                                    "",
                                    "Private room",
                                    "Entire home/apt",
                                ),
                                use_container_width=True,
                            )
                        else:
                            st.plotly_chart(
                                average_price(
                                    sales_NY, airbnb_NY, i, "", "Private room", ""
                                ),
                                use_container_width=True,
                            )
                    elif check_ent:
                        st.plotly_chart(
                            average_price(
                                sales_NY, airbnb_NY, i, "", "", "Entire home/apt"
                            ),
                            use_container_width=True,
                        )
                    else:
                        st.plotly_chart(
                            average_price(sales_NY, airbnb_NY, i, "", "", ""),
                            use_container_width=True,
                        )

# Zdefiniowanie drugiej zakładki
with tab2:
    st.write("""**Tutaj możesz porównać średnie ceny dla wybranych osiedli:**""")

    # Stworzenie ramki danych z porównaniem
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
        ]
    )

    for i in range(0, len(chosen_areas)):
        areas_df = areas_df.append(chosen_areas, ignore_index=True)
        col_list = [
            "Land Square Feet",
            "Gross Square Feet",
            "Year Built",
            "Sale Price",
            "Price Per Square Ft",
        ]
        describe_df = sales_NY[sales_NY["Neighborhood"] == chosen_areas[i]].describe()[
            [
                "Land Square Feet",
                "Gross Square Feet",
                "Year Built",
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
        dict_b = {}
        for i in set(sales_NY["Neighborhood"]):
            dict_b[i] = sales_NY["Borough"][sales_NY["Neighborhood"] == i].unique()[0]
        areas_df = areas_df.drop_duplicates(subset="Neighborhood")
        for i in range(0, len(areas_df["Neighborhood"])):
            areas_df["Borough"].iloc[i] = dict_b[areas_df["Neighborhood"][i]]
        areas_df["Year Built"] = areas_df["Year Built"].astype(int)
        areas_df["Year Built"] = areas_df["Year Built"].astype(str)
        for i in range(0, len(areas_df["Neighborhood"])):
            areas_df["Price Per Rental"].iloc[i] = (
                airbnb_NY[airbnb_NY["Neighborhood"] == areas_df["Neighborhood"].iloc[i]]
                .describe()["Price"]["mean"]
                .round(2)
            )
        areas_df["Price Per Square Ft/Price Per Rental"] = (
            areas_df["Price Per Square Ft"] / areas_df["Price Per Rental"]
        )
        areas_df["Price Per Square Ft/Price Per Rental"] = areas_df[
            "Price Per Square Ft/Price Per Rental"
        ]
        for i in range(0, len(areas_df["Neighborhood"])):
            areas_df["Availability 365"].iloc[i] = (
                airbnb_NY[airbnb_NY["Neighborhood"] == areas_df["Neighborhood"].iloc[i]]
                .describe()["Availability 365"]["mean"]
                .astype(int)
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
            ]
        ]

        # Przetlumaczenie nazw kolumn na polski
        areas_df = areas_df.rename(
            columns={
                "Neighborhood": "Osiedle",
                "Borough": "Dzielnica",
                "Land Square Feet": "Powierzchnia działki [ft2]",
                "Gross Square Feet": "Całkowita powierzchnia [ft2]",
                "Year Built": "Rok budowy",
                "Sale Price": "Cena sprzedaży",
                "Price Per Square Ft": "Cena stopy kwadratowej",
                "Price Per Rental": "Cena wynajmu",
                "Price Per Square Ft/Price Per Rental": "Cena stopy kwadratowej/Cena wynajmu",
                "Availability 365": "Dostępność dni wynajmu w roku",
            }
        )
    with st.container():
        if len(chosen_areas) == 0:
            st.write("Wybierz osiedla do porównania z menu bocznego.")
        else:
            areas_df = areas_df.sort_index()
            st.dataframe(areas_df, use_container_width=True)

# Zdefiniowanie trzeciej zakładki
with tab3:
    st.write(map_airbnb(airbnb_NY))
