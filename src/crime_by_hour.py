# File: src/crime_by_hour.py
import pandas as pd

def analyze_crime_by_hour(df: pd.DataFrame, offence_type: str = None) -> pd.Series:
    """
    [REFACTOR STAGE] Safely processes hourly crime distributions.
    Enforces zero-filled 24-hour index mapping while protecting raw input dataframe.
    """
    # Defensive programming: Prevent side-effects by creating a shallow copy
    working_df = df.copy()
    
    # Apply category filter if requested
    if offence_type:
        working_df = working_df[working_df['CSI_CATEGORY'] == offence_type]
        
    # Standard hourly aggregation
    hourly_counts = working_df.groupby('OCC_HOUR').size()
    
    # Guarantee full 24-hour continuous sequence (0-23) with strict zero-fill constraints
    full_day_hours = list(range(0, 24))
    validated_hourly_series = hourly_counts.reindex(full_day_hours, fill_value=0)
    
    return validated_hourly_series