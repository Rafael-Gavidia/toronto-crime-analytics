# File: src/pipeline.py

import pandas as pd
from pathlib import Path

class CrimeDataPipeline:
    """
    [SR-01] Object-Oriented Data Pipeline for Toronto Crime Analytics.
    Encapsulates data ingestion, validation, and cleaning workflows.
    """
    TORONTO_LAT_BOUNDS = (43.58, 43.85)
    TORONTO_LON_BOUNDS = (-79.65, -79.10)
    NSA_PLACEHOLDER = "NSA"
    UNKNOWN_TOKEN = "Unknown"

    def __init__(self, file_path: str | Path = None):
        self.file_path = Path(file_path) if file_path else None

    # DATA INGESTION
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

    # DATA CLEANING

    def filter_by_geometry(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        [US-09] Filters the dataset to include only valid Toronto coordinates.
        Returns a strictly filtered copy to prevent memory mutations.
        """
        if df.empty or not {"LAT_WGS84", "LONG_WGS84"}.issubset(df.columns):
            return df.copy()

        lat_min, lat_max = self.TORONTO_LAT_BOUNDS
        lon_min, lon_max = self.TORONTO_LON_BOUNDS

        valid_coords = (
            df["LAT_WGS84"].between(lat_min, lat_max, inclusive="both")
            & df["LONG_WGS84"].between(lon_min, lon_max, inclusive="both")
            & (df["LAT_WGS84"] != 0.0)
            & (df["LONG_WGS84"] != 0.0)
        )

        return df.loc[valid_coords].copy()
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        [US-02] Clean raw Toronto crime data.
        """

        if df.empty:
            return df.copy()
        cleaned = df.copy()

        # Date parsing
        if "OCC_DATE" in cleaned.columns:

            cleaned["OCC_DATE"] = pd.to_datetime(
                cleaned["OCC_DATE"],
                errors="coerce"
            )

            if "OCC_YEAR" in cleaned.columns:
                cleaned["OCC_YEAR"] = cleaned["OCC_YEAR"].fillna(
                    cleaned["OCC_DATE"].dt.year
                )

            if "OCC_MONTH" in cleaned.columns:
                cleaned["OCC_MONTH"] = cleaned["OCC_MONTH"].fillna(
                    cleaned["OCC_DATE"].dt.month_name()
                )

            if "OCC_DAY" in cleaned.columns:
                cleaned["OCC_DAY"] = cleaned["OCC_DAY"].fillna(
                    cleaned["OCC_DATE"].dt.day
                )

            if "OCC_DOY" in cleaned.columns:
                cleaned["OCC_DOY"] = cleaned["OCC_DOY"].fillna(
                    cleaned["OCC_DATE"].dt.dayofyear
                )

            if "OCC_DOW" in cleaned.columns:
                cleaned["OCC_DOW"] = cleaned["OCC_DOW"].fillna(
                    cleaned["OCC_DATE"].dt.day_name()
                )

            cleaned = cleaned.dropna(subset=["OCC_DATE"])

        # Spatial filtering
        cleaned = self.filter_by_geometry(cleaned)

        # Missing categorical values
        fill_values = {
            "NEIGHBOURHOOD_158": self.UNKNOWN_TOKEN,
            "NEIGHBOURHOOD_140": self.UNKNOWN_TOKEN,
            "DIVISION": self.UNKNOWN_TOKEN,
            "LOCATION_TYPE": self.UNKNOWN_TOKEN,
            "PREMISES_TYPE": self.UNKNOWN_TOKEN,
            "OFFENCE": "Unknown Offence",
        }

        existing_fill_values = {
            col: value
            for col, value in fill_values.items()
            if col in cleaned.columns
        }

        cleaned = cleaned.fillna(existing_fill_values)

        # Replace NSA placeholders
        object_cols = cleaned.select_dtypes(
            include=["object", "string"]
        ).columns

        for col in object_cols:
            cleaned[col] = cleaned[col].replace(
                self.NSA_PLACEHOLDER,
                self.UNKNOWN_TOKEN
            )

        return cleaned

    # PIPELINE EXECUTION
    def run(self) -> pd.DataFrame:
        """
        Execute complete ETL workflow.
        """

        if self.file_path is None:
            raise ValueError(
                "Pipeline requires a file path for execution."
            )

        raw_df = self.load_data()
        return self.clean_data(raw_df)