# tests/test_neighbourhood.py
# [US-08] Pytest tests for neighbourhood ranking - TDD

import pandas as pd
import pytest
from src.neighbourhood import filter_valid_coordinates, get_neighbourhood_rankings


def make_df(rows):
    """Helper to build a minimal DataFrame for testing."""
    return pd.DataFrame(rows, columns=["LAT_WGS84", "LONG_WGS84", "NEIGHBOURHOOD_158"])


# --- filter_valid_coordinates tests ---

def test_filter_drops_zero_coordinates():
    """Rows with 0.0 lat or lon must be dropped."""
    df = make_df([
        (43.7, -79.4, "Moss Park"),
        (0.0, -79.4, "Downtown"),
        (43.7, 0.0, "Midtown"),
    ])
    result = filter_valid_coordinates(df)
    assert len(result) == 1
    assert result["NEIGHBOURHOOD_158"].values[0] == "Moss Park"


def test_filter_drops_out_of_bounds_coordinates():
    """Rows with coordinates outside Toronto bounding box must be dropped."""
    df = make_df([
        (43.7, -79.4, "Valid"),
        (10.0, -79.4, "Too Far South"),
        (43.7, 10.0, "Too Far East"),
    ])
    result = filter_valid_coordinates(df)
    assert len(result) == 1
    assert result["NEIGHBOURHOOD_158"].values[0] == "Valid"


def test_filter_keeps_boundary_coordinates():
    """Coordinates exactly on the boundary edges must be kept."""
    df = make_df([
        (43.5810, -79.6393, "Edge Case Min"),
        (43.8555, -79.1168, "Edge Case Max"),
    ])
    result = filter_valid_coordinates(df)
    assert len(result) == 2


def test_filter_empty_dataframe():
    """Empty input must return empty DataFrame without crashing."""
    df = pd.DataFrame(columns=["LAT_WGS84", "LONG_WGS84", "NEIGHBOURHOOD_158"])
    result = filter_valid_coordinates(df)
    assert result.empty


# --- get_neighbourhood_rankings tests ---

def test_rankings_sorted_descending():
    """Neighbourhoods must be sorted by incident count descending."""
    df = pd.DataFrame({
        "LAT_WGS84": [43.7] * 6,
        "LONG_WGS84": [-79.4] * 6,
        "NEIGHBOURHOOD_158": ["Alpha", "Beta", "Beta", "Beta", "Alpha", "Gamma"]
    })
    result = get_neighbourhood_rankings(df)
    counts = result["incident_count"].tolist()
    assert counts == sorted(counts, reverse=True)


def test_rankings_excludes_unknown_and_nsa():
    """Unknown and NSA placeholder neighbourhoods must be excluded."""
    df = pd.DataFrame({
        "LAT_WGS84": [43.7] * 4,
        "LONG_WGS84": [-79.4] * 4,
        "NEIGHBOURHOOD_158": ["Unknown", "NSA", "Moss Park", "Moss Park"]
    })
    result = get_neighbourhood_rankings(df)
    neighbourhoods = result["NEIGHBOURHOOD_158"].tolist()
    assert "Unknown" not in neighbourhoods
    assert "NSA" not in neighbourhoods


def test_rankings_top_n_limit():
    """Result must respect the top_n limit."""
    neighbourhoods = [f"Area_{i}" for i in range(20)]
    df = pd.DataFrame({
        "LAT_WGS84": [43.7] * 20,
        "LONG_WGS84": [-79.4] * 20,
        "NEIGHBOURHOOD_158": neighbourhoods
    })
    result = get_neighbourhood_rankings(df, top_n=5)
    assert len(result) <= 5


def test_rankings_empty_dataframe():
    """Empty input must return empty DataFrame without crashing."""
    df = pd.DataFrame(columns=["LAT_WGS84", "LONG_WGS84", "NEIGHBOURHOOD_158"])
    result = get_neighbourhood_rankings(df)
    assert result.empty
    assert "incident_count" in result.columns


def test_rankings_all_placeholders_returns_empty():
    """If all neighbourhoods are Unknown or NSA, return empty DataFrame."""
    df = pd.DataFrame({
        "LAT_WGS84": [43.7] * 3,
        "LONG_WGS84": [-79.4] * 3,
        "NEIGHBOURHOOD_158": ["Unknown", "NSA", "Unknown"]
    })
    result = get_neighbourhood_rankings(df)
    assert result.empty