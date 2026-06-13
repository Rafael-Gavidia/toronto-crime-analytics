import streamlit as st
import pandas as pd
from src.offence_distribution import calculate_offence_distribution

def show_overview(df: pd.DataFrame):
    st.header("Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Incidents", f"{len(df):,}")
    col2.metric("Neighbourhoods", df["NEIGHBOURHOOD_158"].nunique())
    col3.metric("Offence Types", df["OFFENCE"].nunique())

    st.subheader("Offence Distribution")
    result = calculate_offence_distribution(df)
    st.dataframe(result, use_container_width=True)