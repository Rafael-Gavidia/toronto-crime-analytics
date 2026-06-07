# File: src/offence_distribution.py
import pandas as pd

def calculate_offence_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    [US-06] Computes total volume and percentage shares of crime categories using CSI_CATEGORY,
    sorted in descending order. Ensures the total percentage sums up to exactly 100.0%.
    """
    # Defensive check: Ensure the correct column exists
    if 'CSI_CATEGORY' not in df.columns:
        raise KeyError("The operational dataset is missing the required 'CSI_CATEGORY' column.")

    # 1. Group by CSI_CATEGORY and calculate volume
    grouped = df.groupby('CSI_CATEGORY').size().reset_index(name='VOLUME')
    
    # 2. Sort in descending order based on crime volume
    grouped = grouped.sort_values(by='VOLUME', ascending=False).reset_index(drop=True)
    
    # 3. Calculate percentage shares strictly rounded to 1 decimal place
    total_volume = grouped['VOLUME'].sum()
    if total_volume > 0:
        grouped['PERCENTAGE'] = (grouped['VOLUME'] / total_volume * 100).round(1)
    else:
        grouped['PERCENTAGE'] = 0.0
    
    # 4. Return the finalized structural dataframe
    return grouped[['CSI_CATEGORY', 'VOLUME', 'PERCENTAGE']]