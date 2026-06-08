# src/division.py
# [US-07] Police Division Crime Activity

import pandas as pd


def get_division_crime_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates crime incident counts by Toronto Police Service division.

    - Valid division strings (e.g. D11, D14) are counted normally.
    - Missing, blank, or unrecognized division strings are mapped to 'Unknown'.
    - Results are sorted in descending order by incident count.

    Args:
        df: Cleaned DataFrame containing a DIVISION column.

    Returns:
        pd.DataFrame with columns: DIVISION, incident_count
        sorted descending by incident_count.
    """
    if df.empty:
        return pd.DataFrame(columns=["DIVISION", "incident_count"])

    df = df.copy()

    # Flag invalid/missing division values as Unknown
    valid_pattern = r"^D\d{2}$"
    df["DIVISION"] = df["DIVISION"].astype(str).str.strip()
    df["DIVISION"] = df["DIVISION"].where(
        df["DIVISION"].str.match(valid_pattern), other="Unknown"
    )

    # Group and count
    result = (
        df.groupby("DIVISION")
        .size()
        .reset_index(name="incident_count")
        .sort_values("incident_count", ascending=False)
        .reset_index(drop=True)
    )

    return result


def get_division_percentage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes each division's percentage share of total city-wide crime.

    Args:
        df: Cleaned DataFrame containing a DIVISION column.

    Returns:
        pd.DataFrame with columns: DIVISION, incident_count, percentage
        sorted descending by incident_count.
    """
    if df.empty:
        return pd.DataFrame(columns=["DIVISION", "incident_count", "percentage"])

    counts = get_division_crime_counts(df)
    total = counts["incident_count"].sum()
    counts["percentage"] = (counts["incident_count"] / total * 100).round(2)

    return counts