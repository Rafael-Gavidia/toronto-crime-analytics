# File: tests/test_by_hour.py
import pandas as pd
import pytest
from src.crime_by_hour import analyze_crime_by_hour

def test_analyze_crime_by_hour_returns_24_elements():
    """
    [RED] Requirement 1: Verify that the function returns exactly 24 rows 
    representing every hour of a day (0 to 23), even with sparse input data.
    """
    df = pd.DataFrame({
        'CSI_CATEGORY': ['Assault', 'Robbery'],
        'OCC_HOUR': [0, 5]
    })
    result = analyze_crime_by_hour(df)
    
    # Assert that the output series length is strictly 24 and indexed chronologically
    assert len(result) == 24
    assert list(result.index) == list(range(0, 24))


def test_analyze_crime_by_hour_filters_by_offence_type():
    """
    [RED] Requirement 2: Verify that the function correctly filters the dataset 
    by the specified offence category (CSI_CATEGORY).
    """
    df = pd.DataFrame({
        'CSI_CATEGORY': ['Assault', 'Robbery', 'Assault'],
        'OCC_HOUR': [0, 5, 0]
    })
    result = analyze_crime_by_hour(df, offence_type='Assault')
    
    # Hour 0 should aggregate exactly 2 counts of 'Assault'
    assert result.loc[0] == 2
    # Hour 5 should be 0 because 'Robbery' must be filtered out
    assert result.loc[5] == 0