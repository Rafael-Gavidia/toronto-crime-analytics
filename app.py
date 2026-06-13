import streamlit as st
from src.pipeline import CrimeDataPipeline
# [SR-02] Import the newly established modular plotting utility package into the central application
from src.visualization.plots import create_filtered_crime_trend_plot, create_filtered_premises_plot
from views.overview import show_overview
from views.crime_by_hour import show_crime_by_hour
from views.neighbourhood import show_neighbourhood
from views.division import show_division
from views.premises import show_premises

st.set_page_config(page_title="Toronto Crime Analytics", layout="wide")
#st.title("Toronto Crime Analytics Dashboard")
st.markdown("""
<style>
:root {
    --primary-color: #4a4a4a !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #f5f5f5;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #2c2c2c;
}

/* ==================== RADIO BUTTONS ==================== */
div[data-baseweb="radio"] [role="radio"][aria-checked="true"] > div:first-child {
    border-color: #4a4a4a !important;
    background-color: #4a4a4a !important;
}

div[data-baseweb="radio"] [role="radio"][aria-checked="true"] > div:first-child > div {
    background-color: #ffffff !important;
}

div[data-baseweb="radio"] label[aria-checked="true"] {
    color: #2c2c2c !important;
    font-weight: 600 !important;
}

div[data-baseweb="slider"] div[role="slider"] {
    background-color: #4a4a4a !important;
    border-color: #4a4a4a !important;
}

div[data-baseweb="slider"] div[role="progressbar"] > div {
    background-color: #4a4a4a !important;
}

div[data-baseweb="slider"] div[style*="background-color: rgb"] {
    background-color: #4a4a4a !important;
}

[data-testid="stSlider"] div[style*="color"] {
    color: #4a4a4a !important;
}

/* Min / Max */
div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"] {
    color: #4a4a4a !important;
}

span[data-baseweb="tag"] {
    background-color: #4a4a4a !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


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