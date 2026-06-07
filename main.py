# File: main.py
import argparse
import os
import pandas as pd
from src.cleaner import clean_crime_data
from src.crime_by_hour import analyze_crime_by_hour
from src.trends import get_crime_trends, get_yearly_summary
# [US-06] Import the core engine function for offence type distribution analysis
from src.offence_distribution import calculate_offence_distribution


def run_data_cleaning():
    """US-02: Pipeline for data cleaning."""
    print("Running data cleaning...")
    df = pd.read_csv("data/Toronto_Crime_Indicators.csv", low_memory=False)
    df_cleaned = clean_crime_data(df)
    df_cleaned.to_csv("data/data_cleaned.csv", index=False)
    print("Cleaned data saved to 'data/data_cleaned.csv'")


def run_feature_engineering():
    """US-03: Pipeline for feature engineering."""
    print("Extracting features...")
    df = pd.read_csv("data/data_cleaned.csv", low_memory=False)
    # Placeholder for feature engineering logic from US-03
    df.to_csv("data/data_features.csv", index=False)
    print("Features saved to 'data/data_features.csv'")


def run_crime_hourly_analysis(df):
    """US-04: Pipeline for hourly crime distribution matrix."""
    print("\nExecuting 24-hour crime distribution analysis engine [US-04]...")
    hourly_distribution = analyze_crime_by_hour(df, offence_type="Assault")
    print("\n=== [Metrics Output] Chronological 24-Hour Verified Array (Assault) ===")
    print("-" * 55)
    print(hourly_distribution)
    print("-" * 55)
    print("[SUCCESS] Hourly analysis stage completed with side-effect protections.\n")


def run_crime_trends():
    """US-05: Pipeline for crime trends over time."""
    print("Running crime trends analysis [US-05]...")
    df = pd.read_csv("data/data_cleaned.csv", low_memory=False)

    print("\n--- Monthly Crime Trends ---")
    trends = get_crime_trends(df)
    print(trends.head(24))

    print("\n--- Yearly Crime Summary ---")
    yearly = get_yearly_summary(df)
    print(yearly)


def run_offence_distribution(df):
    """[US-06] Pipeline for Categorical Offence Type Distribution analysis."""
    print("\n--> Calculating Categorical Offence Distributions [US-06]...")
    
    # Verify the existence of CSI_CATEGORY column before running the core engine
    if 'CSI_CATEGORY' in df.columns:
        offence_dist = calculate_offence_distribution(df)
        print("-" * 60)
        print(offence_dist.to_string(index=False))
        print("-" * 60)
        print("[SUCCESS] US-06 Offence Type Distribution computed and verified.\n")
    else:
        print("Warning: 'CSI_CATEGORY' column missing in the dataset. Skipping US-06.")


0def main():
    parser = argparse.ArgumentParser(description="Toronto Crime Analytics Pipeline")

    # Single integrated choices array supporting all team stages
    parser.add_argument(
        "--stage",
        type=str,
        required=True,
        choices=["clean", "features", "analysis", "trends", "offence", "all"],
        help="Specify which stage of the project to run (clean, features, analysis, trends, offence, all)"
    )

    args = parser.parse_args()

    # Shared data loading logic optimized for different pipeline stages
    def load_operational_data():
        if os.path.exists("data/data_features.csv"):
            path = "data/data_features.csv"
        elif os.path.exists("data/data_cleaned.csv"):
            path = "data/data_cleaned.csv"
        else:
            path = "data/Toronto_Crime_Indicators.csv"
        print(f"Loading operational dataset from: {path}")
        return pd.read_csv(path, low_memory=False)

    # Pipeline execution routing based on the selected stage
    if args.stage == "clean":
        run_data_cleaning()
        
    elif args.stage == "features":
        run_feature_engineering()
        
    elif args.stage == "analysis":
        df = load_operational_data()
        run_crime_hourly_analysis(df)
        
    elif args.stage == "trends":
        run_crime_trends()
        
    elif args.stage == "offence":
        df = load_operational_data()
        run_offence_distribution(df)
        
    elif args.stage == "all":
        # Master end-to-end pipeline execution flow
        run_data_cleaning()
        run_feature_engineering()
        df = load_operational_data()
        run_crime_hourly_analysis(df)
        run_crime_trends()
        run_offence_distribution(df)  # US-06 integrated as the final analytical stage


if __name__ == "__main__":
    main()