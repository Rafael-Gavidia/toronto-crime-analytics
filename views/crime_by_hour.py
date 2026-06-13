import streamlit as st
import pandas as pd
import plotly.express as px
from src.crime_by_hour import get_crimes_by_hour

def show_crime_by_hour(df: pd.DataFrame):
    st.header("Crimes by Hour of Day")
    result = get_crimes_by_hour(df)
    fig = px.bar(result, x="OCC_HOUR", y="incident_count",
                 title="Incident Count by Hour of Day",
                 labels={"OCC_HOUR": "Hour", "incident_count": "Incidents"})
    st.plotly_chart(fig, use_container_width=True)