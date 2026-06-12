import streamlit as st

from views.overview import show_overview
from views.crime_by_hour import show_crime_by_hour
from views.neighbourhood import show_neighbourhood
from views.division import show_division
from views.premises import show_premises

st.set_page_config(
    page_title="Toronto Crime Analytics",
    layout="wide"
)

st.title("Toronto Crime Analytics Dashboard")

# --- NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select View:",
    [
        "Overview",
        "Crime by Hour",
        "Neighbourhood",
        "Division",
        "Premises"
    ]
)

# --- INTERACTIVE FILTERS (US-13) ---
st.sidebar.markdown("---")
st.sidebar.header("Data Filters")

# Standard lists (to be dynamically fed by the dataframe in US-14)
years_list = [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014]
crimes_list = ["Assault", "Auto Theft", "Break and Enter", "Robbery", "Theft Over"]

selected_years = st.sidebar.multiselect(
    "Select Year(s):", 
    options=years_list, 
    default=years_list
)

selected_crimes = st.sidebar.multiselect(
    "Select Offence Type(s):", 
    options=crimes_list, 
    default=crimes_list
)

# --- DEFENSIVE ZERO-STATE CATCH (US-13) ---
if not selected_years or not selected_crimes:
    st.info("⚠️ **Action Required:** All filters have been cleared. Please select at least one Year and one Offence Type from the sidebar to render analytics.")
    st.stop() # Gracefully halts the execution of the page below to prevent errors

# --- PAGE ROUTING ---
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