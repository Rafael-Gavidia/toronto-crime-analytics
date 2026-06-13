import streamlit as st
import pandas as pd
import plotly.express as px
from src.premises import get_premises_distribution

def show_premises(df: pd.DataFrame):
    st.header("Premises Analysis")
    result = get_premises_distribution(df)
    fig = px.pie(result, names="PREMISES_TYPE", values="incident_count",
                 title="Crime Distribution by Premises Type")
    st.plotly_chart(fig, use_container_width=True)