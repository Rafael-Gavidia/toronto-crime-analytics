# src/premises.py
# [US-11] Premises Type Analysis

import pandas as pd


def get_premises_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates crime incident counts by premises type.

    - Valid premises types are counted normally.
    - Missing, blank, or unmapped premises entries are mapped to 'Other'.
    - Results are sorted in descending order by incident count.

    Args:
        df: Cleaned DataFrame containing a PREMISES_TYPE column.

    Returns:
        pd.DataFrame with columns: PREMISES_TYPE, incident_count
        sorted descending by incident_count.
    """
    if df.empty:
        return pd.DataFrame(columns=["PREMISES_TYPE", "incident_count"])

    df = df.copy()

    # Impute blank or missing premises entries to Other
    df["PREMISES_TYPE"] = df["PREMISES_TYPE"].astype(str).str.strip()
    # handle empty and unmapped premises entries
    df["PREMISES_TYPE"] = df["PREMISES_TYPE"].replace({"": "Other", "nan": "Other", "NSA": "Other"})

    # Group and count
    result = (
        df.groupby("PREMISES_TYPE")
        .size()
        .reset_index(name="incident_count")
        .sort_values("incident_count", ascending=False)
        .reset_index(drop=True)
    )

    return result


def get_premises_percentage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes each premises type's percentage share of total incidents.

    Args:
        df: Cleaned DataFrame containing a PREMISES_TYPE column.

    Returns:
        pd.DataFrame with columns: PREMISES_TYPE, incident_count, percentage
        sorted descending by incident_count.
    """
    if df.empty:
        return pd.DataFrame(columns=["PREMISES_TYPE", "incident_count", "percentage"])

    counts = get_premises_distribution(df)
    total = counts["incident_count"].sum()
    counts["percentage"] = (counts["incident_count"] / total * 100).round(2)

    return counts