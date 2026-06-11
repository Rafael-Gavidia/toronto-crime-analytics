import pandas as pd

def calculate_division_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes cross-divisional statistics and percentage share metrics.
    Formats complex multi-index metrics into a clean, flat summary dataframe.
    """
    if df.empty:
        return pd.DataFrame(columns=['DIVISION', 'VOLUME', 'SHARE'])

    # 1. [Comparison] Aggregate crime volumes side-by-side grouped by DIVISION.
    # Structured to remain scalable if additional multi-variable metrics are integrated later.
    summary = df.groupby('DIVISION').size().to_frame(name='VOLUME')

    # 2. [Market Share] Calculate localized contribution percentage relative to city-wide total crime volume.
    total_city_crime = summary['VOLUME'].sum()
    if total_city_crime > 0:
        summary['SHARE'] = (summary['VOLUME'] / total_city_crime) * 100
    else:
        summary['SHARE'] = 0.0

    # Apply formatting rule to round the percentage share metrics to 1 decimal place.
    summary['SHARE'] = summary['SHARE'].round(1)

    # 3. [Formatting] Reset index to flatten the multi-index layout into an analysis-ready structure.
    # [T 10.4] Sort by VOLUME in descending order to evaluate inter-division baseline deviations.
    flat_summary = summary.sort_values(by='VOLUME', ascending=False).reset_index()

    return flat_summary