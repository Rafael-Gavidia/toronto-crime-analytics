# tests/test_trends.py
# [US-05] Pytest tests for crime trends over time

import pandas as pd
import pytest
from src.trends import get_crime_trends, get_yearly_summary


def make_df(rows):
    """Helper to build a minimal DataFrame for testing."""
    return pd.DataFrame(rows, columns=["OCC_YEAR", "OCC_MONTH"])


# --- get_crime_trends tests ---

def test_trends_sorted_chronologically():
    """Output must be strictly sorted by year then month."""
    df = make_df([
        (2015, "March"),
        (2015, "January"),
        (2014, "December"),
        (2014, "January"),
    ])
    result = get_crime_trends(df)
    years = result["OCC_YEAR"].tolist()
    months = result["MONTH_NUM"].tolist()
    # Check each row is >= previous row in (year, month) order
    for i in range(1, len(result)):
        assert (years[i], months[i]) >= (years[i - 1], months[i - 1])


def test_trends_fills_missing_months_with_zero():
    """Missing months between min and max year must be filled with 0."""
    df = make_df([
        (2020, "January"),
        (2020, "December"),  # gap: Feb-Nov should be filled
    ])
    result = get_crime_trends(df)
    # 2020 should have all 12 months
    year_2020 = result[result["OCC_YEAR"] == 2020]
    assert len(year_2020) == 12
    # Months other than Jan and Dec should have 0 incidents
    middle = year_2020[~year_2020["OCC_MONTH"].isin(["January", "December"])]
    assert (middle["incident_count"] == 0).all()


def test_trends_correct_counts():
    """Incident counts must reflect actual data grouping."""
    df = make_df([
        (2021, "March"),
        (2021, "March"),
        (2021, "March"),
        (2021, "June"),
    ])
    result = get_crime_trends(df)
    march_count = result[(result["OCC_YEAR"] == 2021) & (result["OCC_MONTH"] == "March")]["incident_count"].values[0]
    june_count = result[(result["OCC_YEAR"] == 2021) & (result["OCC_MONTH"] == "June")]["incident_count"].values[0]
    assert march_count == 3
    assert june_count == 1


def test_trends_empty_dataframe():
    """Empty input must return empty DataFrame without crashing."""
    df = pd.DataFrame(columns=["OCC_YEAR", "OCC_MONTH"])
    result = get_crime_trends(df)
    assert result.empty
    assert "incident_count" in result.columns


def test_trends_invalid_month_dropped():
    """Rows with unrecognized month strings must be silently dropped."""
    df = make_df([
        (2019, "March"),
        (2019, "BADMONTH"),
    ])
    result = get_crime_trends(df)
    months_in_result = result["OCC_MONTH"].tolist()
    assert "BADMONTH" not in months_in_result


# --- get_yearly_summary tests ---

def test_yearly_summary_sorted():
    """Yearly summary must be sorted ascending by year."""
    df = make_df([
        (2018, "May"),
        (2016, "January"),
        (2017, "August"),
    ])
    result = get_yearly_summary(df)
    assert result["OCC_YEAR"].tolist() == sorted(result["OCC_YEAR"].tolist())


def test_yearly_summary_correct_counts():
    """Yearly totals must match actual row counts per year."""
    df = make_df([
        (2020, "January"),
        (2020, "February"),
        (2021, "March"),
    ])
    result = get_yearly_summary(df)
    assert result[result["OCC_YEAR"] == 2020]["incident_count"].values[0] == 2
    assert result[result["OCC_YEAR"] == 2021]["incident_count"].values[0] == 1


def test_yearly_summary_empty():
    """Empty input returns empty DataFrame without crashing."""
    df = pd.DataFrame(columns=["OCC_YEAR", "OCC_MONTH"])
    result = get_yearly_summary(df)
    assert result.empty