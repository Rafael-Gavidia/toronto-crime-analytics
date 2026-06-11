# tests/test_premises.py
# [US-11] Pytest tests for premises type analysis

import pandas as pd
import pytest
from src.premises import get_premises_distribution, get_premises_percentage


def make_df(premises):
    """Helper to build a minimal DataFrame for testing."""
    return pd.DataFrame({"PREMISES_TYPE": premises})


# --- get_premises_distribution tests ---

def test_premises_sorted_descending():
    """Output must be sorted in descending order by incident count."""
    df = make_df(["Apartment", "House", "House", "House", "Apartment", "Commercial"])
    result = get_premises_distribution(df)
    counts = result["incident_count"].tolist()
    assert counts == sorted(counts, reverse=True)


def test_premises_empty_mapped_to_other():
    """Empty or blank premises entries must be mapped to Other."""
    df = make_df(["Apartment", "", "House", "nan"])
    result = get_premises_distribution(df)
    premises = result["PREMISES_TYPE"].tolist()
    assert "Other" in premises
    assert "" not in premises


def test_premises_nsa_mapped_to_other():
    """NSA premises entries must be mapped to Other."""
    df = make_df(["Apartment", "NSA", "NSA", "House"])
    result = get_premises_distribution(df)
    premises = result["PREMISES_TYPE"].tolist()
    assert "NSA" not in premises
    assert "Other" in premises


def test_premises_correct_counts():
    """Incident counts must reflect actual data grouping."""
    df = make_df(["Apartment", "Apartment", "Apartment", "House", "House"])
    result = get_premises_distribution(df)
    apt = result[result["PREMISES_TYPE"] == "Apartment"]["incident_count"].values[0]
    house = result[result["PREMISES_TYPE"] == "House"]["incident_count"].values[0]
    assert apt == 3
    assert house == 2


def test_premises_empty_dataframe():
    """Empty input must return empty DataFrame without crashing."""
    df = pd.DataFrame(columns=["PREMISES_TYPE"])
    result = get_premises_distribution(df)
    assert result.empty
    assert "incident_count" in result.columns


# --- get_premises_percentage tests ---

def test_premises_percentage_sums_to_100():
    """Percentage shares must sum to exactly 100."""
    df = make_df(["Apartment", "House", "Commercial", "Apartment", "House"])
    result = get_premises_percentage(df)
    total = result["percentage"].sum()
    assert abs(total - 100.0) < 0.01


def test_premises_percentage_has_correct_columns():
    """Result must contain PREMISES_TYPE, incident_count, and percentage."""
    df = make_df(["Apartment", "House"])
    result = get_premises_percentage(df)
    assert "PREMISES_TYPE" in result.columns
    assert "incident_count" in result.columns
    assert "percentage" in result.columns


def test_premises_percentage_empty():
    """Empty input returns empty DataFrame without crashing."""
    df = pd.DataFrame(columns=["PREMISES_TYPE"])
    result = get_premises_percentage(df)
    assert result.empty