import argparse
import os
import pandas as pd
from src.cleaner import clean_crime_data
from src.trends import get_crime_trends, get_yearly_summary


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


def run_crime_trends():
    """US-05: Pipeline for crime trends over time."""
    print("Running crime trends analysis...")
    df = pd.read_csv("data/data_cleaned.csv", low_memory=False)

    print("\n--- Monthly Crime Trends ---")
    trends = get_crime_trends(df)
    print(trends.head(24))

    print("\n--- Yearly Crime Summary ---")
    yearly = get_yearly_summary(df)
    print(yearly)


def main():
    parser = argparse.ArgumentParser(description="Toronto Crime Analytics Pipeline")

    parser.add_argument(
        "--stage",
        type=str,
        required=True,
        choices=["clean", "features", "trends", "train", "all"],
        help="Specify which stage of the project to run"
    )

    args = parser.parse_args()

    if args.stage == "clean":
        run_data_cleaning()
    elif args.stage == "features":
        run_feature_engineering()
    elif args.stage == "trends":
        run_crime_trends()
    elif args.stage == "all":
        run_data_cleaning()
        run_feature_engineering()
        run_crime_trends()


if __name__ == "__main__":
    main()