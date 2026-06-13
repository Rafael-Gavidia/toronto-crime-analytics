# src/data_cache.py
import streamlit as st
from pathlib import Path
from src.pipeline import CrimeDataPipeline

DATA_PATH = Path("data/Toronto_Crime_Indicators.csv")

@st.cache_data
def get_cached_dataframe(path: str = str(DATA_PATH)):
    """
    [US-14] Single cached entry point for pipeline execution.
    Prevents redundant file I/O on dashboard reloads.
    """
    pipeline = CrimeDataPipeline(path)
    return pipeline.run()