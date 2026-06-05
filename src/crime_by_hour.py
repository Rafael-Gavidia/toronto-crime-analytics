# File: src/crime_by_hour.py
import pandas as pd

def analyze_crime_by_hour(df: pd.DataFrame, offence_type: str = None) -> pd.Series:
    """
    Calculates crime distribution grouped by OCC_HOUR.
    Guarantees a complete 24-hour indexed array with zero-fill handling.
    """
    # 1. Handle optional filter constraint (e.g., 'Assault', 'Robbery')
    if offence_type:
        df = df[df['MCI_CATEGORY'] == offence_type]
        
    # 2. Perform baseline hourly aggregation
    hourly_counts = df.groupby('OCC_HOUR').size()
    
    # 3. Defensive Reindexing: Map to complete chronological 24-hour range (0-23)
    full_24_hours = range(0, 24)
    hourly_counts_validated = hourly_counts.reindex(full_24_hours, fill_value=0)
    
    return hourly_counts_validated