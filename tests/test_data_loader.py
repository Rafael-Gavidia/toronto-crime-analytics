import pytest
import pandas as pd
# 1. THE NEW IMPORT
from src.pipeline import CrimeDataPipeline

def test_load_dataset_success():
    """Validates that a correct file loads properly into a DataFrame."""
    # We use the sample data you just created for fast testing
    file_path = "data/sample_crime_data.csv"
    
    # 2. THE NEW CLASS CALL
    df = CrimeDataPipeline().load_data(file_path)
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'OCC_HOUR' in df.columns

def test_load_dataset_file_not_found():
    """Validates that a missing file throws a FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        # 3. THE NEW CLASS CALL
        CrimeDataPipeline().load_data("data/fake_ghost_file.csv")

def test_load_dataset_invalid_schema(tmp_path):
    """Validates that a corrupted schema throws a ValueError."""
    # Create a temporary bad dataset using pytest's tmp_path fixture
    bad_data = pd.DataFrame({
        "WRONG_COLUMN_1": [1, 2],
        "WRONG_COLUMN_2": ["A", "B"]
    })
    
    bad_file = tmp_path / "bad_schema.csv"
    bad_data.to_csv(bad_file, index=False)

    # The test passes if the specific ValueError is triggered
    with pytest.raises(ValueError, match="Corrupted schema"):
        # 4. THE NEW CLASS CALL
        CrimeDataPipeline().load_data(str(bad_file))