# tests/test_integration.py
# [US-14] End-to-end integration tests — TDD

import pandas as pd
import pytest
from src.pipeline import CrimeDataPipeline
from src.crime_by_hour import get_crimes_by_hour
from src.neighbourhood import get_neighbourhood_rankings
from src.division_performance import calculate_division_performance
from src.premises import get_premises_distribution
from src.offence_distribution import calculate_offence_distribution


@pytest.fixture(scope="module")
def clean_df():
    pipeline = CrimeDataPipeline("data/Toronto_Crime_Indicators.csv")
    return pipeline.run()


# --- E2E Pipeline: pipeline output feeds each view function ---

def test_pipeline_output_feeds_crime_by_hour(clean_df):
    result = get_crimes_by_hour(clean_df)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert list(result.columns) == ["OCC_HOUR", "incident_count"]


def test_pipeline_output_feeds_neighbourhood(clean_df):
    result = get_neighbourhood_rankings(clean_df)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "NEIGHBOURHOOD_158" in result.columns


def test_pipeline_output_feeds_division(clean_df):
    result = calculate_division_performance(clean_df)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "DIVISION" in result.columns


def test_pipeline_output_feeds_premises(clean_df):
    result = get_premises_distribution(clean_df)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "PREMISES_TYPE" in result.columns


def test_pipeline_output_feeds_offence_distribution(clean_df):
    result = calculate_offence_distribution(clean_df)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "CSI_CATEGORY" in result.columns


# --- Consistency: chart data matches raw calculations ---

def test_crime_by_hour_totals_match_raw_count(clean_df):
    """Sum of hourly counts must equal total records in the DataFrame."""
    result = get_crimes_by_hour(clean_df)
    assert result["incident_count"].sum() == len(clean_df)


def test_offence_distribution_totals_match(clean_df):
    """VOLUME sum must equal total records."""
    result = calculate_offence_distribution(clean_df)
    assert result["VOLUME"].sum() == len(clean_df)


def test_offence_percentage_sums_to_100(clean_df):
    """PERCENTAGE column must sum to 100.0 (within rounding tolerance)."""
    result = calculate_offence_distribution(clean_df)
    assert abs(result["PERCENTAGE"].sum() - 100.0) <= 0.5


def test_division_share_sums_to_100(clean_df):
    """SHARE column must sum to 100.0 (within rounding tolerance)."""
    result = calculate_division_performance(clean_df)
    assert abs(result["SHARE"].sum() - 100.0) <= 0.5


def test_neighbourhood_rankings_no_placeholders(clean_df):
    """Rankings must never contain Unknown or NSA."""
    result = get_neighbourhood_rankings(clean_df)
    assert "Unknown" not in result["NEIGHBOURHOOD_158"].values
    assert "NSA" not in result["NEIGHBOURHOOD_158"].values


# --- Filter consistency: filtered df matches view output ---

def test_year_filter_consistency(clean_df):
    """Filtering by year must propagate correctly to hourly counts."""
    filtered = clean_df[clean_df["OCC_YEAR"] == 2023]
    if filtered.empty:
        pytest.skip("No 2023 data in dataset")
    result = get_crimes_by_hour(filtered)
    assert result["incident_count"].sum() == len(filtered)


def test_premises_sorted_descending(clean_df):
    """Premises results must be sorted descending by incident_count."""
    result = get_premises_distribution(clean_df)
    counts = result["incident_count"].tolist()
    assert counts == sorted(counts, reverse=True)