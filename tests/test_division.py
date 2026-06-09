# tests/test_division.py
# [US-07] Pytest tests for police division crime activity

import pandas as pd
import pytest
from src.division import get_division_crime_counts, get_division_percentage


def make_df(divisions):
    """Helper to build a minimal DataFrame for testing."""
    return pd.DataFrame({"DIVISION": divisions})


# --- get_division_crime_counts tests ---

def test_division_counts_sorted_descending():
    """Output must be sorted in descending order by incident count."""
    df = make_df(["D11", "D14", "D14", "D11", "D11", "D22"])
    result = get_division_crime_counts(df)
    counts = result["incident_count"].tolist()
    assert counts == sorted(counts, reverse=True)


def test_division_invalid_strings_mapped_to_unknown():
    """Invalid or unrecognized division strings must be mapped to Unknown."""
    df = make_df(["D11", "NSA", "INVALID", "", "D22"])
    result = get_division_crime_counts(df)
    divisions = result["DIVISION"].tolist()
    assert "NSA" not in divisions
    assert "INVALID" not in divisions
    assert "Unknown" in divisions


def test_division_valid_divisions_counted_correctly():
    """Valid division strings must be counted accurately."""
    df = make_df(["D11", "D11", "D11", "D14", "D14"])
    result = get_division_crime_counts(df)
    d11 = result[result["DIVISION"] == "D11"]["incident_count"].values[0]
    d14 = result[result["DIVISION"] == "D14"]["incident_count"].values[0]
    assert d11 == 3
    assert d14 == 2


def test_division_empty_dataframe():
    """Empty input must return empty DataFrame without crashing."""
    df = pd.DataFrame(columns=["DIVISION"])
    result = get_division_crime_counts(df)
    assert result.empty
    assert "incident_count" in result.columns


def test_division_all_invalid_goes_to_unknown():
    """If all entries are invalid, everything maps to Unknown."""
    df = make_df(["NSA", "NSA", "BADVAL"])
    result = get_division_crime_counts(df)
    assert len(result) == 1
    assert result["DIVISION"].values[0] == "Unknown"


# --- get_division_percentage tests ---

def test_division_percentage_sums_to_100():
    """Percentage shares across all divisions must sum to exactly 100."""
    df = make_df(["D11", "D11", "D14", "D22", "D22", "D22"])
    result = get_division_percentage(df)
    total = result["percentage"].sum()
    assert abs(total - 100.0) < 0.01


def test_division_percentage_has_correct_columns():
    """Result must contain DIVISION, incident_count, and percentage columns."""
    df = make_df(["D11", "D14"])
    result = get_division_percentage(df)
    assert "DIVISION" in result.columns
    assert "incident_count" in result.columns
    assert "percentage" in result.columns


def test_division_percentage_empty():
    """Empty input returns empty DataFrame without crashing."""
    df = pd.DataFrame(columns=["DIVISION"])
    result = get_division_percentage(df)
    assert result.empty