import pandas as pd
import pytest
from src.pipeline import CrimeDataPipeline


@pytest.fixture
def mock_raw_data():
    return pd.DataFrame({
        "LAT_WGS84": [43.70, 0.0, 55.0, 43.65],
        "LONG_WGS84": [-79.40, 0.0, -120.0, -79.35],
        "LOCATION_TYPE": ["Convenience Store", "Commercial", "NSA", "NSA"],
        "OCC_DATE": ["2024-01-01", "2024-01-02", "2024-01-03", "invalid-date-xyz"]
    })


def test_tdd_red_phase_violations(mock_raw_data):

    assert (mock_raw_data["LAT_WGS84"] == 0.0).any()
    assert ((mock_raw_data["LAT_WGS84"] > 43.85) | (mock_raw_data["LAT_WGS84"] < 43.58)).any()
    
    assert (mock_raw_data["LOCATION_TYPE"] == "NSA").any()
    
    assert not pd.api.types.is_datetime64_any_dtype(mock_raw_data["OCC_DATE"])


def test_tdd_green_phase_cleanup(mock_raw_data):
    """
    [TDD GREEN EVIDENCE] 
    """
    result = CrimeDataPipeline().clean_data(mock_raw_data)

    assert len(result) == 1

    assert result["LAT_WGS84"].iloc[0] == 43.70
    assert result["LONG_WGS84"].iloc[0] == -79.40

    assert pd.api.types.is_datetime64_any_dtype(result["OCC_DATE"])

    df_nsa = pd.DataFrame({
        "LAT_WGS84": [43.7], "LONG_WGS84": [-79.4],
        "LOCATION_TYPE": ["NSA"], "OCC_DATE": ["2024-01-01"]
    })
    cleaned_nsa = CrimeDataPipeline().clean_data(df_nsa)
    assert cleaned_nsa["LOCATION_TYPE"].iloc[0] == "Unknown"