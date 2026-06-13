import pytest
import pandas as pd
from src.filters import DataFilters

@pytest.fixture
def mock_dashboard_data():
    """Mock dataset for interactive filtering."""
    return pd.DataFrame({
        "OCC_YEAR": [2023, 2023, 2024, 2024],
        "OFFENCE": ["Assault", "Robbery", "Assault", "Theft"],
        "INCIDENT_ID": [1, 2, 3, 4]
    })

def test_multiselect_dataframe_filtering(mock_dashboard_data):
    """
    [US-13] Validates that dataframe queries correctly intersect 
    multiple selected years and offence types.
    """
    # Execution: Filter for '2023' and 'Assault'
    selected_years = [2023]
    selected_crimes = ["Assault"]
    
    # This will fail in the RED phase because DataFilters does not exist
    filtered_df = DataFilters.apply_multiselect_filter(
        df=mock_dashboard_data, 
        years=selected_years, 
        crimes=selected_crimes
    )
    
    # Verification: Only Incident 1 should survive the intersection
    assert len(filtered_df) == 1
    assert filtered_df.iloc[0]["INCIDENT_ID"] == 1
    
def test_empty_filter_graceful_catch(mock_dashboard_data):
    """
    [US-13] Validates that passing empty filter selections returns an empty dataframe 
    to trigger the UI st.info zero-state alert cleanly.
    """
    empty_df = DataFilters.apply_multiselect_filter(
        df=mock_dashboard_data, 
        years=[], 
        crimes=[]
    )
    
    assert empty_df.empty