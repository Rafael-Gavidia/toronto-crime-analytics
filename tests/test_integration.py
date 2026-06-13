# tests/test_integration.py
# [US-14] Integration tests — TDD RED

import pandas as pd
import pytest
from src.pipeline import CrimeDataPipeline
from src.crime_by_hour import get_crimes_by_hour
from src.neighbourhood import get_neighbourhood_rankings
from src.division_performance import get_division_performance
from src.premises import get_premises_breakdown
from src.offence_distribution import get_offence_distribution


@pytest.fixture(scope="module")
def clean_df():
    """Load and clean real dataset through the pipeline."""
    pipeline = CrimeDataPipeline("data/Toronto_Crime_Indicators.csv")
    return pipeline.run()


# --- E2E Pipeline: pipeline output feeds view functions ---

def test_pipeline_output_feeds_crime_by_hour(clean_df):
    """get_crimes_by_hour must accept pipeline output and return non-empty result."""
    result = get_crimes_by_hour(clean_df)
    assert result is not None
    assert not result.empty


def test_pipeline_output_feeds_neighbourhood(clean_df):
    """get_neighbourhood_rankings must accept pipeline output and return non-empty result."""
    result = get_neighbourhood_rankings(clean_df)
    assert result is not None
    assert not result.empty


def test_pipeline_output_feeds_division(clean_df):
    """get_division_performance must accept pipeline output and return non-empty result."""
    result = get_division_performance(clean_df)
    assert result is not None
    assert not result.empty


def test_pipeline_output_feeds_premises(clean_df):
    """get_premises_breakdown must accept pipeline output and return non-empty result."""
    result = get_premises_breakdown(clean_df)
    assert result is not None
    assert not result.empty


# --- Consistency: metric values match chart data vectors ---

def test_crime_by_hour_totals_match_raw_count(clean_df):
    """Sum of hourly counts must equal total records in the filtered DataFrame."""
    result = get_crimes_by_hour(clean_df)
    # result must have a numeric count column
    count_col = [c for c in result.columns if c != "OCC_HOUR"][0]
    assert result[count_col].sum() == len(clean_df)


def test_neighbourhood_rankings_no_unknown(clean_df):
    """Rankings returned to the view must never contain Unknown or NSA."""
    result = get_neighbourhood_rankings(clean_df)
    assert "Unknown" not in result["NEIGHBOURHOOD_158"].values
    assert "NSA" not in result["NEIGHBOURHOOD_158"].values


def test_offence_distribution_totals_match(clean_df):
    """Offence distribution counts must sum to total records."""
    result = get_offence_distribution(clean_df)
    count_col = [c for c in result.columns if c != "OFFENCE"][0]
    assert result[count_col].sum() == len(clean_df)


# --- Filter consistency: filtered df matches what view receives ---

def test_year_filter_consistency(clean_df):
    """Filtering by year must reduce row count and match explicit calculation."""
    filtered = clean_df[clean_df["OCC_YEAR"] == 2023]
    result = get_crimes_by_hour(filtered)
    count_col = [c for c in result.columns if c != "OCC_HOUR"][0]
    assert result[count_col].sum() == len(filtered)