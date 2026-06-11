import streamlit as st

from pages.overview import show_overview
from pages.crime_by_hour import show_crime_by_hour
from pages.neighbourhood import show_neighbourhood
from pages.division import show_division
from pages.premises import show_premises


st.set_page_config(
    page_title="Toronto Crime Analytics",
    layout="wide"
)

st.title("Toronto Crime Analytics Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Crime by Hour",
        "Neighbourhood",
        "Division",
        "Premises"
    ]
)

if page == "Overview":
    show_overview()

elif page == "Crime by Hour":
    show_crime_by_hour()

elif page == "Neighbourhood":
    show_neighbourhood()

elif page == "Division":
    show_division()

elif page == "Premises":
    show_premises()