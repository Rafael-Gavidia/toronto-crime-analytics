# src/premises.py
# [US-11] Premises Type Analysis

import pandas as pd

PLACEHOLDER_VALUES = {"", "nan", "NSA"}


def _clean_premises(df: pd.DataFrame) -> pd.DataFrame:
    """Impute blank, nan, or NSA premises entries to 'Other'."""
    df = df.copy()
    df["PREMISES_TYPE"] = df["PREMISES_TYPE"].astype(str).str.strip()
    df["PREMISES_TYPE"] = df["PREMISES_TYPE"].replace(
        {v: "Other" for v in PLACEHOLDER_VALUES}
    )
    return df


def get_premises_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates crime incident counts by premises type.

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

    df = _clean_premises(df)

    return (
        df.groupby("PREMISES_TYPE")
        .size()
        .reset_index(name="incident_count")
        .sort_values("incident_count", ascending=False)
        .reset_index(drop=True)
    )


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


def get_premises_offence_breakdown(df: pd.DataFrame, top_offences: int = 6) -> pd.DataFrame:
    """
    Computes the percentage share of each offence type within each premises type.
    Used for a 100% stacked bar chart.

    - Cleans premises placeholders to 'Other'.
    - Groups minor offence types beyond top_offences into 'Other Offences'.
    - Returns row-wise percentages (each premises row sums to 100%).

    Args:
        df: Cleaned DataFrame containing PREMISES_TYPE and OFFENCE columns.
        top_offences: Number of most frequent offence types to keep individually.

    Returns:
        pd.DataFrame with columns: PREMISES_TYPE, OFFENCE, incident_count, percentage
        where percentage is the share of that offence within that premises type.
    """
    offence_col = "OFFENCE" if "OFFENCE" in df.columns else "CSI_CATEGORY" if "CSI_CATEGORY" in df.columns else None
    required = {"PREMISES_TYPE"} | ({offence_col} if offence_col else set())

    if df.empty or not required.issubset(df.columns) or offence_col is None:
        return pd.DataFrame(columns=["PREMISES_TYPE", "OFFENCE", "incident_count", "percentage"])

    df = _clean_premises(df)
    df = df.copy()
    df = df.rename(columns={offence_col: "OFFENCE"})

    # Determine top offences globally by total volume
    top_offence_names = (
        df["OFFENCE"].value_counts()
        .head(top_offences)
        .index.tolist()
    )

    # Group minor offences
    df["OFFENCE"] = df["OFFENCE"].where(
        df["OFFENCE"].isin(top_offence_names), other="Other Offences"
    )

    # Count per premises + offence
    counts = (
        df.groupby(["PREMISES_TYPE", "OFFENCE"])
        .size()
        .reset_index(name="incident_count")
    )

    # Calculate within-premises percentage
    premises_totals = counts.groupby("PREMISES_TYPE")["incident_count"].transform("sum")
    counts["percentage"] = (counts["incident_count"] / premises_totals * 100).round(1)

    return counts.sort_values(["PREMISES_TYPE", "incident_count"], ascending=[True, False]).reset_index(drop=True)