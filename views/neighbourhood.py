import streamlit as st
import pandas as pd
import plotly.express as px
from src.neighbourhood import get_neighbourhood_rankings

def show_neighbourhood(df: pd.DataFrame):
    st.header("Neighbourhood Analysis")
    top_n = st.slider("Top N Neighbourhoods", 5, 25, 10)
    result = get_neighbourhood_rankings(df, top_n=top_n)
    fig = px.bar(result, x="incident_count", y="NEIGHBOURHOOD_158",
                 orientation="h", title=f"Top {top_n} Neighbourhoods by Incidents")
    st.plotly_chart(fig, use_container_width=True)