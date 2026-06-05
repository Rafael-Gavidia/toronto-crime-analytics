# File: main.py
import argparse
import os
import pandas as pd
from src.cleaner import clean_crime_data
# [US-04] Import the TDD-validated core engine function
from src.crime_by_hour import analyze_crime_by_hour


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
    # Read the cleaned data generated from the previous stage
    df = pd.read_csv("data/data_cleaned.csv", low_memory=False)
    
    # Placeholder for feature engineering logic from US-03
    # df_features = engineering_logic(df)
    
    df.to_csv("data/data_features.csv", index=False)
    print("Features saved to 'data/data_features.csv'")


def run_crime_hourly_analysis():
    """US-04: Pipeline for hourly crime distribution matrix."""
    print("\nExecuting 24-hour crime distribution analysis engine...")
    
    # Defensive path check: prioritize features or cleaned data over raw data
    if os.path.exists("data/data_features.csv"):
        data_path = "data/data_features.csv"
    elif os.path.exists("data/data_cleaned.csv"):
        data_path = "data/data_cleaned.csv"
    else:
        data_path = "data/Toronto_Crime_Indicators.csv"
        
    print(f"Loading operational dataset from: {data_path}")
    df = pd.read_csv(data_path, low_memory=False)
    
    # Execute your robust TDD analytics engine for 'Assault' as a default use-case
    hourly_distribution = analyze_crime_by_hour(df, offence_type="Assault")
    
    print("\n[Metrics Output] Chronological 24-Hour Verified Array (Assault):")
    print("-" * 45)
    print(hourly_distribution)
    print("-" * 45)


def main():
    parser = argparse.ArgumentParser(description="Toronto Crime Analytics Pipeline")

    # Added "analysis" to choices array to support US-04 execution
    parser.add_argument(
        "--stage",
        type=str,
        required=True,
        choices=["clean", "features", "analysis", "all"],
        help="Specify which stage of the project to run"
    )

    args = parser.parse_args()

    if args.stage == "clean":
        run_data_cleaning()
    elif args.stage == "features":
        run_feature_engineering()
    elif args.stage == "analysis":
        run_crime_hourly_analysis()
    elif args.stage == "all":
        run_data_cleaning()
        run_feature_engineering()
        run_crime_hourly_analysis()  # Includes your analysis in the master end-to-end execution


if __name__ == "__main__":
    main()