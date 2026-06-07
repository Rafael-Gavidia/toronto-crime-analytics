# src/trends.py
# [US-05] Crime Trends Over Time

import pandas as pd

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


def get_crime_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates crime incidents by year (OCC_YEAR) and month (OCC_MONTH).

    Returns a DataFrame with columns:
        OCC_YEAR, OCC_MONTH, MONTH_NUM, incident_count
    Sorted strictly in chronological order.
    Missing months with zero incidents are preserved.

    Args:
        df: Cleaned DataFrame containing OCC_YEAR and OCC_MONTH columns.

    Returns:
        pd.DataFrame sorted chronologically with no gaps.
    """
    if df.empty:
        return pd.DataFrame(columns=["OCC_YEAR", "OCC_MONTH", "MONTH_NUM", "incident_count"])

    # Map month names to numbers for sorting
    month_map = {month: i + 1 for i, month in enumerate(MONTH_ORDER)}

    df = df.copy()
    df["MONTH_NUM"] = df["OCC_MONTH"].map(month_map)

    # Drop rows where month couldn't be mapped
    df = df.dropna(subset=["MONTH_NUM"])
    df["MONTH_NUM"] = df["MONTH_NUM"].astype(int)

    # Group by year and month
    grouped = (
        df.groupby(["OCC_YEAR", "OCC_MONTH", "MONTH_NUM"])
        .size()
        .reset_index(name="incident_count")
    )

    # Build a complete year-month grid to fill missing periods with 0
    # zero-fill verified by test_trends_fills_missing_months_with_zero
    if not grouped.empty:
        years = range(int(grouped["OCC_YEAR"].min()), int(grouped["OCC_YEAR"].max()) + 1)
        all_periods = pd.DataFrame(
            [(y, m, i + 1) for y in years for i, m in enumerate(MONTH_ORDER)],
            columns=["OCC_YEAR", "OCC_MONTH", "MONTH_NUM"]
        )
        result = all_periods.merge(grouped, on=["OCC_YEAR", "OCC_MONTH", "MONTH_NUM"], how="left")
        result["incident_count"] = result["incident_count"].fillna(0).astype(int)
    else:
        result = grouped

    # Sort strictly chronologically
    # enforce chronological sorting by year then month number
    result = result.sort_values(["OCC_YEAR", "MONTH_NUM"]).reset_index(drop=True)

    return result


def get_yearly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates total crime incidents per year.

    Args:
        df: Cleaned DataFrame containing OCC_YEAR column.

    Returns:
        pd.DataFrame with OCC_YEAR and incident_count, sorted ascending.
    """
    if df.empty:
        return pd.DataFrame(columns=["OCC_YEAR", "incident_count"])

    result = (
        df.groupby("OCC_YEAR")
        .size()
        .reset_index(name="incident_count")
        .sort_values("OCC_YEAR")
        .reset_index(drop=True)
    )
    return result