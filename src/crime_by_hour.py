# File: src/crime_by_hour.py
import pandas as pd

def analyze_crime_by_hour(df: pd.DataFrame, offence_type: str = None) -> pd.Series:
    """
    [GREEN STAGE] Implement core filtering and groupby aggregation 
    to satisfy basic test requirements.
    """
    # 1. Filter the dataset by the specified CSI_CATEGORY if provided
    if offence_type:
        df = df[df['CSI_CATEGORY'] == offence_type]
        
    # 2. Perform baseline hourly aggregation across the OCC_HOUR series
    hourly_counts = df.groupby('OCC_HOUR').size()
    
    # 3. Quick fix for the 24-element structural requirement (Green baseline)
    full_24_hours = list(range(0, 24))
    hourly_counts_validated = hourly_counts.reindex(full_24_hours, fill_value=0)
    
    return hourly_counts_validated