# src/crime_by_hour.py

import pandas as pd

DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
WEEKEND = ["Saturday", "Sunday"]


def analyze_crime_by_hour(df: pd.DataFrame, offence_type: str = None) -> pd.Series:
    """
    [REFACTOR STAGE] Safely processes hourly crime distributions.
    Enforces zero-filled 24-hour index mapping while protecting raw input dataframe.
    """
    working_df = df.copy()

    if offence_type:
        working_df = working_df[working_df["CSI_CATEGORY"] == offence_type]

    hourly_counts = working_df.groupby("OCC_HOUR").size()
    full_day_hours = list(range(0, 24))
    validated_hourly_series = hourly_counts.reindex(full_day_hours, fill_value=0)

    return validated_hourly_series


def get_crimes_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    """
    [US-14] Integration wrapper — returns DataFrame for dashboard views.
    """
    series = analyze_crime_by_hour(df)
    result = series.reset_index()
    result.columns = ["OCC_HOUR", "incident_count"]
    return result


def get_crimes_polar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns hourly crime counts formatted for a polar/radar chart.
    Hours 0-23 mapped to degree angles (0-345, step 15).
    Includes hour label for display.

    Returns:
        pd.DataFrame with columns: OCC_HOUR, incident_count, angle, hour_label
    """
    result = get_crimes_by_hour(df)
    result["angle"] = result["OCC_HOUR"] * 15  # 360 / 24 = 15 degrees per hour
    result["hour_label"] = result["OCC_HOUR"].apply(lambda h: f"{h:02d}:00")
    return result


def get_crimes_by_hour_and_dow(df: pd.DataFrame, offence: str = None) -> pd.DataFrame:
    """
    Returns incident counts grouped by OCC_HOUR and OCC_DOW.
    Optionally filtered by a specific OFFENCE type.
    Used for Hour x Day-of-Week heatmap with offence filter.

    Returns:
        pd.DataFrame pivot: index=OCC_DOW (ordered), columns=OCC_HOUR (0-23), values=incident_count
    """
    required = {"OCC_HOUR", "OCC_DOW"}
    if df.empty or not required.issubset(df.columns):
        return pd.DataFrame()

    working = df.copy()
    working["OCC_DOW"] = working["OCC_DOW"].astype(str).str.strip()

    if offence and "OFFENCE" in working.columns:
        working = working[working["OFFENCE"] == offence]

    if working.empty:
        return pd.DataFrame()

    counts = (
        working.groupby(["OCC_DOW", "OCC_HOUR"])
        .size()
        .reset_index(name="incident_count")
    )

    pivot = (
        counts.pivot(index="OCC_DOW", columns="OCC_HOUR", values="incident_count")
        .reindex([d for d in DAY_ORDER if d in counts["OCC_DOW"].unique()])
        .reindex(columns=range(24), fill_value=0)
        .fillna(0)
        .astype(int)
    )

    return pivot


def get_crimes_weekday_vs_weekend(df: pd.DataFrame) -> dict:
    """
    Splits hourly crime counts into weekday (Mon-Fri) vs weekend (Sat-Sun).
    Returns averaged per-day counts so the comparison is fair.

    Returns:
        dict with keys 'weekday' and 'weekend', each a pd.DataFrame
        with columns: OCC_HOUR, avg_incidents
    """
    required = {"OCC_HOUR", "OCC_DOW"}
    if df.empty or not required.issubset(df.columns):
        empty = pd.DataFrame(columns=["OCC_HOUR", "avg_incidents"])
        return {"weekday": empty, "weekend": empty}

    working = df.copy()
    working["OCC_DOW"] = working["OCC_DOW"].astype(str).str.strip()

    full_hours = pd.DataFrame({"OCC_HOUR": range(24)})

    def _avg_hourly(subset: pd.DataFrame, n_days: int) -> pd.DataFrame:
        if subset.empty:
            return full_hours.assign(avg_incidents=0)
        counts = (
            subset.groupby("OCC_HOUR")
            .size()
            .reset_index(name="total")
        )
        merged = full_hours.merge(counts, on="OCC_HOUR", how="left").fillna(0)
        merged["avg_incidents"] = (merged["total"] / n_days).round(1)
        return merged[["OCC_HOUR", "avg_incidents"]]

    weekday_df = working[working["OCC_DOW"].isin(WEEKDAYS)]
    weekend_df = working[working["OCC_DOW"].isin(WEEKEND)]

    return {
        "weekday": _avg_hourly(weekday_df, n_days=5),
        "weekend": _avg_hourly(weekend_df, n_days=2),
    }