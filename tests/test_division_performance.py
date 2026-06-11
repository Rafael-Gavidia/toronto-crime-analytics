import pytest
import pandas as pd
from src.division_performance import calculate_division_performance

def test_division_performance_mathematical_equivalence():
    """
    [Evidence] Pytest confirms mathematical equivalence between 
    cumulative divisional sums and full data baselines.
    """
    # Prepare dummy operational dataset using the verified 'DIVISION' column name
    mock_data = {
        'DIVISION': ['D11', 'D12', 'D11', 'D14', 'D12', 'D11', 'D14', 'D11']
    }
    df = pd.DataFrame(mock_data)
    
    # Execute the core division performance analysis engine
    result_df = calculate_division_performance(df)
    
    # Assertions to verify that the complex metrics layout has been flattened properly
    assert 'DIVISION' in result_df.columns
    assert 'VOLUME' in result_df.columns
    assert 'SHARE' in result_df.columns

    # [Evidence] Validate that cumulative divisional volumes match the full data baseline count exactly
    cumulative_divisional_sum = result_df['VOLUME'].sum()
    full_data_baseline = len(df)
    assert cumulative_divisional_sum == full_data_baseline, \
        f"Mathematical gap found! Divisional sum: {cumulative_divisional_sum}, Baseline: {full_data_baseline}"

    # Verify sorting utility puts the highest volume division at the top (D11 has 4 cases)
    assert result_df.iloc[0]['DIVISION'] == 'D11'
    assert result_df.iloc[0]['VOLUME'] == 4
    
    # Validate that total percentage metrics accumulate correctly to approximately 100%
    total_share = result_df['SHARE'].sum()
    assert pytest.approx(total_share, abs=0.5) == 100.0

def test_division_performance_empty_dataframe():
    """
    Verify edge-case handling for empty datasets to ensure robustness.
    """
    empty_df = pd.DataFrame(columns=['DIVISION'])
    result = calculate_division_performance(empty_df)
    assert len(result) == 0
    assert list(result.columns) == ['DIVISION', 'VOLUME', 'SHARE']