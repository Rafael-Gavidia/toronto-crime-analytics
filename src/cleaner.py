import pandas as pd

# ====================== CONSTANTS ======================
TORONTO_LAT_BOUNDS = (43.58, 43.85)
TORONTO_LON_BOUNDS = (-79.65, -79.10)
NSA_PLACEHOLDER = "NSA"
UNKNOWN_TOKEN = "Unknown"


def clean_crime_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Toronto Crime Indicators dataset according to US-02 requirements.
    
    Acceptance Criteria:
        - Drop rows with invalid/out-of-bound coordinates (including 0.0)
        - Replace all 'NSA' placeholders with 'Unknown'
        - Convert OCC_DATE to datetime and drop invalid dates
    
    This version includes refactoring improvements:
        - Constants extracted
        - More readable and maintainable code
        - Better handling of data types
    """
    if df.empty:
        return df.copy()

    cleaned = df.copy()

    # ==================== SPATIAL FILTER ====================
    lat_min, lat_max = TORONTO_LAT_BOUNDS
    lon_min, lon_max = TORONTO_LON_BOUNDS

    valid_coords = (
        cleaned["LAT_WGS84"].between(lat_min, lat_max, inclusive="both")
        & cleaned["LONG_WGS84"].between(lon_min, lon_max, inclusive="both")
        & (cleaned["LAT_WGS84"] != 0.0)
        & (cleaned["LONG_WGS84"] != 0.0)
    )

    cleaned = cleaned.loc[valid_coords].copy()

    # ==================== NSA REPLACEMENT ====================
    # Fixed Pandas warning + more robust
    object_cols = cleaned.select_dtypes(include=["object", "string"]).columns
    for col in object_cols:
        cleaned[col] = cleaned[col].replace(NSA_PLACEHOLDER, UNKNOWN_TOKEN)

    # ==================== DATE PARSING ====================
    if "OCC_DATE" in cleaned.columns:
        cleaned["OCC_DATE"] = pd.to_datetime(
            cleaned["OCC_DATE"], 
            errors="coerce"
        )
        # Drop rows with invalid dates
        cleaned = cleaned.dropna(subset=["OCC_DATE"])

    return cleaned