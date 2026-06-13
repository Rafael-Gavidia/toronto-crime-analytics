# src/neighbourhood.py
# [US-08] Neighbourhood Ranking - TDD

import pandas as pd

# Toronto bounding box constants
LAT_MIN = 43.5810
LAT_MAX = 43.8555
LON_MIN = -79.6393
LON_MAX = -79.1168


def filter_valid_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters out rows with invalid or out-of-bounds coordinates.

    - Drops rows where LAT_WGS84 or LONG_WGS84 is 0.0
    - Drops rows outside Toronto bounding box

    Args:
        df: Cleaned DataFrame with LAT_WGS84, LONG_WGS84 columns.

    Returns:
        pd.DataFrame with only valid Toronto coordinate rows.
    """
    if df.empty:
        return df.copy()

    df = df.copy()

    df = df[(df["LAT_WGS84"] != 0.0) & (df["LONG_WGS84"] != 0.0)]

    df = df[
        (df["LAT_WGS84"] >= LAT_MIN) & (df["LAT_WGS84"] <= LAT_MAX) &
        (df["LONG_WGS84"] >= LON_MIN) & (df["LONG_WGS84"] <= LON_MAX)
    ]

    return df.reset_index(drop=True)


def get_neighbourhood_rankings(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Ranks neighbourhoods by crime incident count in descending order.

    - Excludes 'Unknown' and 'NSA' placeholder neighbourhoods.
    - Returns top_n neighbourhoods by default.

    Args:
        df: Cleaned DataFrame containing NEIGHBOURHOOD_158 column.
        top_n: Number of top neighbourhoods to return.

    Returns:
        pd.DataFrame with columns: NEIGHBOURHOOD_158, incident_count
        sorted descending by incident_count.
    """
    if df.empty:
        return pd.DataFrame(columns=["NEIGHBOURHOOD_158", "incident_count"])

    df = df.copy()

    df = df[~df["NEIGHBOURHOOD_158"].isin(["Unknown", "NSA"])]

    if df.empty:
        return pd.DataFrame(columns=["NEIGHBOURHOOD_158", "incident_count"])

    result = (
        df.groupby("NEIGHBOURHOOD_158")
        .size()
        .reset_index(name="incident_count")
        .sort_values("incident_count", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    return result


def get_neighbourhood_trends(df: pd.DataFrame, top_n: int = 5, years: int = 5) -> pd.DataFrame:
    """
    Returns year-over-year crime trends for the top N neighbourhoods.

    - Derives top_n from get_neighbourhood_rankings on the full df.
    - Filters to the last `years` years of available data.
    - Excludes 'Unknown' and 'NSA' placeholder neighbourhoods.

    Args:
        df: Cleaned DataFrame containing NEIGHBOURHOOD_158 and OCC_YEAR columns.
        top_n: Number of top neighbourhoods to include in the trend.
        years: How many most-recent years to include.

    Returns:
        pd.DataFrame with columns: OCC_YEAR, NEIGHBOURHOOD_158, incident_count
        sorted by OCC_YEAR ascending.
    """
    required = {"NEIGHBOURHOOD_158", "OCC_YEAR"}
    if df.empty or not required.issubset(df.columns):
        return pd.DataFrame(columns=["OCC_YEAR", "NEIGHBOURHOOD_158", "incident_count"])

    df = df.copy()
    df = df[~df["NEIGHBOURHOOD_158"].isin(["Unknown", "NSA"])]

    if df.empty:
        return pd.DataFrame(columns=["OCC_YEAR", "NEIGHBOURHOOD_158", "incident_count"])

    # Determine top N neighbourhoods by total incidents
    top_neighbourhoods = (
        get_neighbourhood_rankings(df, top_n=top_n)["NEIGHBOURHOOD_158"].tolist()
    )

    # Filter to last `years` years
    max_year = int(df["OCC_YEAR"].max())
    min_year = max_year - years + 1

    trend_df = df[
        df["NEIGHBOURHOOD_158"].isin(top_neighbourhoods) &
        (df["OCC_YEAR"] >= min_year)
    ]

    result = (
        trend_df.groupby(["OCC_YEAR", "NEIGHBOURHOOD_158"])
        .size()
        .reset_index(name="incident_count")
        .sort_values("OCC_YEAR", ascending=True)
        .reset_index(drop=True)
    )

    return result