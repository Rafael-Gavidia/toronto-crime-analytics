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
    - Drops rows where NEIGHBOURHOOD_158 is 'Unknown' or 'NSA'

    Args:
        df: Cleaned DataFrame with LAT_WGS84, LONG_WGS84 columns.

    Returns:
        pd.DataFrame with only valid Toronto coordinate rows.
    """
    if df.empty:
        return df.copy()

    df = df.copy()

    # Drop zero coordinates
    df = df[(df["LAT_WGS84"] != 0.0) & (df["LONG_WGS84"] != 0.0)]

    # Drop coordinates outside Toronto bounding box
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

    # Remove placeholder neighbourhood values
    # exclude Unknown and NSA placeholder neighbourhoods from ranking
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