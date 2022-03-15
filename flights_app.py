#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:41:01 2022

@author: larsheemskerk
"""

import pandas as pd
import streamlit as st


@st.cache()
def load_data():
    df = pd.read_csv(
        'https://github.com/l-heemskerk/streamlit/blob/main/flights.csv'
    )
    return df


#sidebar
st.sidebar.header("please filter here:")

#create filter options
origin = st.sidebar.multiselect(
    "select origin:",
    options=df["origin"].unique(),
    default=df["origin"].unique()
)

carrier = st.sidebar.multiselect(
    "select carrier:",
    options=df["carrier"].unique(),
    default=df["carrier"].unique()
)

#store fitered data in df_seelction
df_selection = df.query(
    "origin == @origin & carrier == @carrier"
    )

#mainpage

st.title(":bar_chart: Flights Dashboard")
st.markdown("An overview of all flights departed from New York airports in 2013 ")

#check filtering

st.markdown("""---""")


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.dataframe(df_selection) 
    
st.markdown("""---""")

#Displayed data based on calculations
total_delay = int(df_selection["dep_delay"].sum())
average_delay = round(df_selection["dep_delay"].mean(), 1)
average_dist = round(df_selection["distance"].mean())


#three columns to dispaly calculations
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total delay:")
    st.subheader(f"{total_delay:,} hour")
with middle_column:
    st.subheader("Average delay:")
    st.subheader(f"{average_delay}")
with right_column:
    st.subheader("Average Distance:")
    st.subheader(f"{average_dist} Miles")
    
st.markdown("""---""")

#barchart 1
dep_delay_per_carrier = (
    df_selection.groupby(by=["carrier"]).sum()[["dep_delay"]].sort_values(by="dep_delay")
    )

fig_dep_delay = pt.bar(
    dep_delay_per_carrier,
    y="dep_delay",
    x=dep_delay_per_carrier.index,
    title="<b>Departure delay per carrier</b>",
)

st.plotly_chart(fig_dep_delay, use_container_width=False)

#barchart 2
dep_delay_per_origin = (
    df_selection.groupby(by=["dest"]).sum()[["dep_delay"]].sort_values(by="dep_delay")
    )

fig_dep_delay2 = pt.bar(
    dep_delay_per_origin,
    y="dep_delay",
    x=dep_delay_per_origin.index,
    title="<b>Arrival delay per destination</b>",
)

st.plotly_chart(fig_dep_delay2, use_container_width=False)
