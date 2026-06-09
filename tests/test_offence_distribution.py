# File: tests/test_offence_distribution.py
import pandas as pd
import pytest
from src.offence_distribution import calculate_offence_distribution

def test_calculate_offence_distribution_sorting_and_math():
    """
    [US-06] Verifies descending sorting and precise 100.0% percentage total 
    even under highly skewed mock data distributions using CSI_CATEGORY.
    """
    # Prepared highly skewed mock data using the updated 'CSI_CATEGORY' column
    mock_data = pd.DataFrame({
        'CSI_CATEGORY': ['Assault', 'Robbery', 'Assault', 'Auto Theft', 'Assault']
    })
    
    result = calculate_offence_distribution(mock_data)
    
    # 1. Validation: Highest volume category ('Assault') must be the first row (Descending Sort)
    assert result.iloc[0]['CSI_CATEGORY'] == 'Assault'
    assert result.iloc[0]['VOLUME'] == 3
    
    # 2. Validation: Ratios must sum up to exactly 100.0%
    assert result['PERCENTAGE'].sum() == 100.0
    
    # 3. Validation: Structural integrity of the output dataframe
    assert list(result.columns) == ['CSI_CATEGORY', 'VOLUME', 'PERCENTAGE']