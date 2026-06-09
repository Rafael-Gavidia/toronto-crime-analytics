import pandas as pd
import os

def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Loads the Toronto Crime dataset and validates its schema.
    Raises errors if the file is missing or the schema is corrupted.
    """
    # 1. Validate the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at path: {file_path}")

    # 2. Load the dataset into Pandas
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read the CSV file: {e}")

    # 3. Validate mandatory columns (Schema Check)
    # Note: Assignment asks for MCI_CATEGORY, but raw data uses CSI_CATEGORY
    mandatory_columns = ['OCC_HOUR', 'CSI_CATEGORY', 'LAT_WGS84', 'LONG_WGS84']
    
    missing_columns = [col for col in mandatory_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Corrupted schema. Missing mandatory columns: {missing_columns}")

    return df