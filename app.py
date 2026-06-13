import streamlit as st
from src.pipeline import CrimeDataPipeline
from views.overview import show_overview
from views.crime_by_hour import show_crime_by_hour
from views.neighbourhood import show_neighbourhood
from views.division import show_division
from views.premises import show_premises

st.set_page_config(page_title="Toronto Crime Analytics", layout="wide")
st.title("Toronto Crime Analytics Dashboard")

from src.data_cache import get_cached_dataframe
df = get_cached_dataframe()

# --- NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select View:",
    ["Overview", "Crime by Hour", "Neighbourhood", "Division", "Premises"]
)

# --- DYNAMIC FILTERS (fed by real data) ---
st.sidebar.markdown("---")
st.sidebar.header("Data Filters")

years_list = sorted(df["OCC_YEAR"].dropna().astype(int).unique().tolist(), reverse=True)
crimes_list = sorted(df["OFFENCE"].dropna().unique().tolist())

selected_years = st.sidebar.multiselect("Select Year(s):", options=years_list, default=years_list)
selected_crimes = st.sidebar.multiselect("Select Offence Type(s):", options=crimes_list, default=crimes_list)

# --- DEFENSIVE ZERO-STATE CATCH ---
if not selected_years or not selected_crimes:
    st.info("⚠️ Please select at least one Year and one Offence Type.")
    st.stop()

# --- APPLY FILTERS ---
filtered_df = df[
    df["OCC_YEAR"].isin(selected_years) &
    df["OFFENCE"].isin(selected_crimes)
]

# --- PAGE ROUTING ---
if page == "Overview":
    show_overview(filtered_df)
elif page == "Crime by Hour":
    show_crime_by_hour(filtered_df)
elif page == "Neighbourhood":
    show_neighbourhood(filtered_df)
elif page == "Division":
    show_division(filtered_df)
elif page == "Premises":
    show_premises(filtered_df)