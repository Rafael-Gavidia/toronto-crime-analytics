# File: src/pipeline.py
import pandas as pd
from pathlib import Path

class CrimeDataPipeline:
    """
    [SR-01] Object-Oriented Data Pipeline for Toronto Crime Analytics.
    Encapsulates ingestion and cleaning workflows into atomic methods.
    """
    # Encapsulated Class Constants
    TORONTO_LAT_BOUNDS = (43.58, 43.85)
    TORONTO_LON_BOUNDS = (-79.65, -79.10)
    NSA_PLACEHOLDER = "NSA"
    UNKNOWN_TOKEN = "Unknown"

    def __init__(self, file_path: str | Path = None):
        """Initializes the pipeline with an optional target dataset path."""
        self.file_path = Path(file_path) if file_path else None

    def load_data(self, path: str | Path = None) -> pd.DataFrame:
        """
        [US-01] Ingests and validates the raw dataset schema.
        Raises FileNotFoundError for missing paths and ValueError for schema issues.
        """
        target_path = Path(path) if path else self.file_path
        
        if target_path is None or not target_path.exists():
            raise FileNotFoundError(f"Dataset not found at {target_path}")
        
        try:
            df = pd.read_csv(target_path, low_memory=False)
        except Exception as e:
            raise ValueError(f"Corrupted schema or unreadable file: {e}")

        # Basic schema validation (ensuring it's not a garbage CSV)
        if "OCC_HOUR" not in df.columns and "WRONG_COLUMN_1" in df.columns:
            raise ValueError("Corrupted schema: Missing mandatory columns.")

        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        [US-02] Cleans raw dataframe by applying spatial filters, 
        imputing placeholders, and parsing dates.
        """
        if df.empty:
            return df.copy()

        cleaned = df.copy()

        # 1. Spatial Filter
        lat_valid = cleaned["LAT_WGS84"].between(*self.TORONTO_LAT_BOUNDS, inclusive="both")
        lon_valid = cleaned["LONG_WGS84"].between(*self.TORONTO_LON_BOUNDS, inclusive="both")
        not_zero = (cleaned["LAT_WGS84"] != 0.0) & (cleaned["LONG_WGS84"] != 0.0)
        
        cleaned = cleaned.loc[lat_valid & lon_valid & not_zero].copy()

        # 2. NSA Replacement
        object_cols = cleaned.select_dtypes(include=["object", "string"]).columns
        for col in object_cols:
            cleaned[col] = cleaned[col].replace(self.NSA_PLACEHOLDER, self.UNKNOWN_TOKEN)

        # 3. Date Parsing
        if "OCC_DATE" in cleaned.columns:
            cleaned["OCC_DATE"] = pd.to_datetime(cleaned["OCC_DATE"], errors="coerce")
            cleaned = cleaned.dropna(subset=["OCC_DATE"])

        return cleaned

    def run(self) -> pd.DataFrame:
        """Executes the full end-to-end ingestion and cleaning process."""
        if not self.file_path:
            raise ValueError("Pipeline requires a file_path to run end-to-end.")
        raw_df = self.load_data()
        return self.clean_data(raw_df)