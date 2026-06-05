# File: src/crime_by_hour.py
import pandas as pd

def analyze_crime_by_hour(df: pd.DataFrame, offence_type: str = None) -> pd.Series:
    """
    Calculates crime distribution grouped by OCC_HOUR.
    Guarantees a complete 24-hour indexed array with defensive zero-fill handling.
    """
    # Defensive Copy to prevent SettingWithCopyWarning
    working_df = df.copy()
    
    # [FIX] Changed from 'MCI_CATEGORY' to 'CSI_CATEGORY' based on actual schema
    if offence_type:
        working_df = working_df[working_df['CSI_CATEGORY'] == offence_type]
        
    # Perform baseline hourly aggregation
    hourly_counts = working_df.groupby('OCC_HOUR').size()
    
    # Defensive Reindexing: Map to complete chronological 24-hour range
    full_24_hours = range(0, 24)
    hourly_counts_validated = hourly_counts.reindex(full_24_hours, fill_value=0).astype('int64')
    
    # Ensure the series index name aligns with reporting standards
    hourly_counts_validated.index.name = 'OCC_HOUR'
    
    return hourly_counts_validated