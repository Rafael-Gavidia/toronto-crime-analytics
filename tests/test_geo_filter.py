import pytest
import pandas as pd
from src.pipeline import CrimeDataPipeline

@pytest.fixture
def geo_mock_data():
    """Creates a dataset with points inside, outside, and exactly on Toronto's borders."""
    return pd.DataFrame({
        "LAT_WGS84": [43.70, 43.00, 44.00, 43.85, 0.0],
        "LONG_WGS84": [-79.40, -80.00, -79.00, -79.65, 0.0],
        "EVENT": ["Inside", "Too Far South", "Too Far North", "Exact Border", "Zero/Null"]
    })

def test_geographic_boundary_filter(geo_mock_data):
    """
    [US-09] Validates that the spatial filter strictly enforces Toronto's geographic bounding box.
    Expected: Only 'Inside' and 'Exact Border' should survive (2 rows).
    """
    pipeline = CrimeDataPipeline()
    
    # Execution: This will fail in the RED phase because the method does not exist yet!
    filtered_df = pipeline.filter_by_geometry(geo_mock_data)
    
    # Verification: Only 2 out of the 5 rows should remain
    assert len(filtered_df) == 2
    assert "Too Far South" not in filtered_df["EVENT"].values
    assert "Zero/Null" not in filtered_df["EVENT"].values