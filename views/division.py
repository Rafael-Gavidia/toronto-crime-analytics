import streamlit as st
import pandas as pd
import plotly.express as px
from src.division_performance import calculate_division_performance

def show_division(df: pd.DataFrame):
    st.header("Division Performance")
    result = calculate_division_performance(df)
    fig = px.bar(result, x="DIVISION", y="VOLUME",
                 title="Crime Volume by Police Division",
                 labels={"VOLUME": "Incidents"})
    st.plotly_chart(fig, use_container_width=True)