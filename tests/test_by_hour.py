# File: tests/test_by_hour.py
import pandas as pd
import pytest
from src.crime_by_hour import analyze_crime_by_hour

def test_analyze_crime_by_hour_returns_24_elements():
    """
    [REFACTOR] Requirement 1: Verify that the function returns exactly 24 rows 
    representing every hour of a day (0 to 23), even with sparse input data.
    """
    df = pd.DataFrame({
        'CSI_CATEGORY': ['Assault', 'Robbery'],
        'OCC_HOUR': [0, 5]
    })
    result = analyze_crime_by_hour(df)
    
    assert len(result) == 24
    assert list(result.index) == list(range(0, 24))


def test_analyze_crime_by_hour_filters_by_offence_type():
    """
    [REFACTOR] Requirement 2: Verify that the function correctly filters the dataset 
    by the specified offence category (CSI_CATEGORY).
    """
    df = pd.DataFrame({
        'CSI_CATEGORY': ['Assault', 'Robbery', 'Assault'],
        'OCC_HOUR': [0, 5, 0]
    })
    result = analyze_crime_by_hour(df, offence_type='Assault')
    
    assert result.loc[0] == 2
    assert result.loc[5] == 0 


def test_analyze_crime_by_hour_fills_missing_hours_with_zero():
    """
    [REFACTOR] Requirement 3: Ensure that hours with zero crime events are defensively 
    filled with 0 instead of being dropped or returning NaN.
    """
    df = pd.DataFrame({
        'CSI_CATEGORY': ['Assault'],
        'OCC_HOUR': [3]  # Only 3 AM has data
    })
    result = analyze_crime_by_hour(df)
    
    # 3 AM must be 1, while unrepresented hours like 0 and 23 must be safely 0
    assert result.loc[3] == 1
    assert result.loc[0] == 0
    assert result.loc[23] == 0