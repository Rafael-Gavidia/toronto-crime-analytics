# File: tests/test_crime_by_hour.py
import pytest
import pandas as pd
from src.crime_by_hour import analyze_crime_by_hour

@pytest.fixture
def mock_crime_data():
    """Generates a mock Toronto crime dataset with missing hours to test zero-fill logic."""
    data = {
        'OCC_HOUR': [0, 1, 2, 3, 4, 6, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23], # 5 and 17 are missing
        'MCI_CATEGORY': ['Assault']*10 + ['Break and Enter']*10 + ['Robbery']*3
    }
    return pd.DataFrame(data)

def test_crime_by_hour_returns_exactly_24_rows(mock_crime_data):
    """[AC-Completeness] Output must contain exactly 24 rows (0-23)."""
    result = analyze_crime_by_hour(mock_crime_data)
    assert len(result) == 24
    assert list(result.index) == list(range(24))

def test_crime_by_hour_fills_missing_with_zero(mock_crime_data):
    """[AC-Zero-Fill] Missing hour intervals must systematically resolve to 0."""
    result = analyze_crime_by_hour(mock_crime_data)
    assert result.loc[5] == 0
    assert result.loc[17] == 0

def test_crime_by_hour_with_optional_filter(mock_crime_data):
    """[AC-Filter] Dynamically filters data if offence_type is provided."""
    result = analyze_crime_by_hour(mock_crime_data, offence_type='Robbery')
    assert len(result) == 24
    assert result.sum() == 3