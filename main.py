import argparse
import os
import pandas as pd
from src.cleaner import clean_crime_data


def run_data_cleaning():
    """US-02: Pipeline for data cleaning."""
    print("Running data cleaning...")
    df = pd.read_csv("data/Toronto_Crime_Indicators.csv", low_memory=False)
    df_cleaned = clean_crime_data(df)
    df_cleaned.to_csv("data/data_cleaned.csv", index=False)
    print("Cleaned data saved to 'data_cleaned.csv'")

def run_feature_engineering():
    """US-03: Pipeline for feature engineering."""
    print("Extracting features...")
    df = pd.read_csv("data_cleaned.csv")
    print("Features saved to 'data_features.csv'")

def main():
    parser = argparse.ArgumentParser(description="Toronto Crime Analytics Pipeline")
    
    parser.add_argument(
        "--stage", 
        type=str, 
        required=True,
        choices=["clean", "features", "train", "all"],
        help="Specify which stage of the project to run"
    )
    
    args = parser.parse_args()

    if args.stage == "clean":
        run_data_cleaning()
    elif args.stage == "features":
        run_feature_engineering()
    elif args.stage == "all":
        run_data_cleaning()
        run_feature_engineering()

if __name__ == "__main__":
    main()