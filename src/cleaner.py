import pandas as pd
from pathlib import Path

# Constants
TORONTO_LAT_BOUNDS = (43.58, 43.85)
TORONTO_LON_BOUNDS = (-79.65, -79.10)
NSA_PLACEHOLDER = "NSA"
UNKNOWN_TOKEN = "Unknown"

def clean_crime_data(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean data with improved missing values handling"""
    if df.empty:
        return df.copy()

    cleaned = df.copy()

    if "OCC_DATE" in cleaned.columns:
        cleaned["OCC_DATE"] = pd.to_datetime(cleaned["OCC_DATE"], errors="coerce")
        
        cleaned["OCC_YEAR"] = cleaned["OCC_YEAR"].fillna(
            cleaned["OCC_DATE"].dt.year
        )
        cleaned["OCC_MONTH"] = cleaned["OCC_MONTH"].fillna(
            cleaned["OCC_DATE"].dt.month_name()
        )
        cleaned["OCC_DAY"] = cleaned["OCC_DAY"].fillna(
            cleaned["OCC_DATE"].dt.day
        )
        cleaned["OCC_DOY"] = cleaned["OCC_DOY"].fillna(
            cleaned["OCC_DATE"].dt.dayofyear
        )
        cleaned["OCC_DOW"] = cleaned["OCC_DOW"].fillna(
            cleaned["OCC_DATE"].dt.day_name()
        )

    # Drop rows where OCC_DATE is still invalid after parsing
    cleaned = cleaned.dropna(subset=["OCC_DATE"])

    # ==================== SPATIAL FILTER ====================
    lat_min, lat_max = self.TORONTO_LAT_BOUNDS
    lon_min, lon_max = self.TORONTO_LON_BOUNDS

    valid_coords = (
        cleaned["LAT_WGS84"].between(lat_min, lat_max, inclusive="both") &
        cleaned["LONG_WGS84"].between(lon_min, lon_max, inclusive="both") &
        (cleaned["LAT_WGS84"] != 0.0) &
        (cleaned["LONG_WGS84"] != 0.0)
    )

    cleaned = cleaned.loc[valid_coords].copy()

    # ==================== FILL MISSING CATEGORICAL ====================
    fill_values = {
        "NEIGHBOURHOOD_158": "Unknown",
        "NEIGHBOURHOOD_140": "Unknown",
        "DIVISION": "Unknown",
        "LOCATION_TYPE": "Unknown",           # ← добавили
        "PREMISES_TYPE": "Unknown",           # ← добавили
        "OFFENCE": "Unknown Offence",
    }
    cleaned = cleaned.fillna(value=fill_values)

    # ==================== NSA REPLACEMENT ====================
    object_cols = cleaned.select_dtypes(include=["object", "string"]).columns
    for col in object_cols:
        cleaned[col] = cleaned[col].replace("NSA", "Unknown")

    return cleaned