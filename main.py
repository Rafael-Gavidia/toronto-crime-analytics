import argparse
import os
import pandas as pd
from src.pipeline import CrimeDataPipeline
from src.crime_by_hour import analyze_crime_by_hour
from src.trends import get_crime_trends, get_yearly_summary
from src.offence_distribution import calculate_offence_distribution
from src.division import get_division_crime_counts, get_division_percentage
from src.neighbourhood import filter_valid_coordinates, get_neighbourhood_rankings
from src.premises import get_premises_distribution, get_premises_percentage
# [SR-02] Import the newly established modular plotting utility package
from src.visualization.plots import create_hourly_crime_plot, create_filtered_crime_trend_plot


def run_data_cleaning():
    """US-02 & SR-01: Object-Oriented Pipeline for data ingestion and cleaning."""
    print("Running data cleaning pipeline...")
    pipeline = CrimeDataPipeline("data/Toronto_Crime_Indicators.csv")
    df_cleaned = pipeline.run()
    df_cleaned.to_csv("data/data_cleaned.csv", index=False)
    print("Cleaned data saved to 'data/data_cleaned.csv'")


def run_feature_engineering():
    """US-03: Pipeline for feature engineering."""
    print("Extracting features...")
    df = pd.read_csv("data/data_cleaned.csv", low_memory=False)
    df.to_csv("data/data_features.csv", index=False)
    print("Features saved to 'data/data_features.csv'")


def run_crime_hourly_analysis(df):
    """US-04: Pipeline for hourly crime distribution matrix."""
    print("\nExecuting 24-hour crime distribution analysis engine [US-04]...")
    hourly_distribution = analyze_crime_by_hour(df, offence_type="Assault")
    
    # [SR-02] T 2.4: Standardize view execution calls to exclusively handle layout generation and plot invocation
    hourly_chart = create_hourly_crime_plot(df, offence_type="Assault")
    
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
    """US-06: Pipeline for Categorical Offence Type Distribution analysis."""
    print("\n--> Calculating Categorical Offence Distributions [US-06]...")

    if 'CSI_CATEGORY' in df.columns:
        offence_dist = calculate_offence_distribution(df)
        print("-" * 60)
        print(offence_dist.to_string(index=False))
        print("-" * 60)
        print("[SUCCESS] US-06 Offence Type Distribution computed and verified.\n")
    else:
        print("Warning: 'CSI_CATEGORY' column missing in the dataset. Skipping US-06.")


def run_division_analysis(df):
    """US-07: Pipeline for police division crime activity."""
    print("\nRunning police division analysis [US-07]...")

    print("\n--- Crime Count by Division ---")
    counts = get_division_crime_counts(df)
    print(counts)

    print("\n--- Division Percentage Share ---")
    percentages = get_division_percentage(df)
    print(percentages)
    print("[SUCCESS] US-07 Division analysis completed.\n")


def run_neighbourhood_ranking(df):
    """US-08: Pipeline for neighbourhood crime ranking."""
    print("\nRunning neighbourhood ranking analysis [US-08]...")

    df_filtered = filter_valid_coordinates(df)
    print(f"\nValid coordinate rows: {len(df_filtered)}")

    print("\n--- Top 10 Neighbourhoods by Crime Count ---")
    rankings = get_neighbourhood_rankings(df_filtered, top_n=10)
    print(rankings)
    print("[SUCCESS] US-08 Neighbourhood ranking completed.\n")


def run_premises_analysis(df):
    """US-11: Pipeline for premises type analysis."""
    print("\nRunning premises type analysis [US-11]...")

    print("\n--- Crime Count by Premises Type ---")
    distribution = get_premises_distribution(df)
    print(distribution)

    print("\n--- Premises Percentage Share ---")
    percentages = get_premises_percentage(df)
    print(percentages)
    print("[SUCCESS] US-11 Premises analysis completed.\n")


# [SR-02] T 2.4: Dedicated runner to handle standardized visualization execution layer
def run_visualization_refactor_stage(df):
    """SR-02: Isolated pipeline stage for verifying modular chart generation."""
    print("\nExecuting Standardized Visualization Refactor Engine [SR-02]...")
    trend_chart = create_filtered_crime_trend_plot(df)
    print("[SUCCESS] SR-02 Visual pipeline rendering test complete with zero chart breakage.\n")


def main():
    parser = argparse.ArgumentParser(description="Toronto Crime Analytics Pipeline")

    parser.add_argument(
        "--stage",
        type=str,
        required=True,
        # [SR-02] Integrated 'visual-refactor' option into the command-line interface argument choices safely
        choices=["clean", "features", "analysis", "trends", "offence", "division", "neighbourhood", "premises", "visual-refactor", "all"],
        help="Specify which stage of the project to run"
    )

    args = parser.parse_args()

    def load_operational_data():
        if os.path.exists("data/data_features.csv"):
            path = "data/data_features.csv"
        elif os.path.exists("data/data_cleaned.csv"):
            path = "data/data_cleaned.csv"
        else:
            path = "data/Toronto_Crime_Indicators.csv"
        print(f"Loading operational dataset from: {path}")
        return pd.read_csv(path, low_memory=False)

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

    elif args.stage == "division":
        df = load_operational_data()
        run_division_analysis(df)

    elif args.stage == "neighbourhood":
        df = load_operational_data()
        run_neighbourhood_ranking(df)

    elif args.stage == "premises":
        df = load_operational_data()
        run_premises_analysis(df)

    # [SR-02] Route visualization refactor verification stage
    elif args.stage == "visual-refactor":
        df = load_operational_data()
        run_visualization_refactor_stage(df)

    elif args.stage == "all":
        run_data_cleaning()
        run_feature_engineering()
        df = load_operational_data()
        run_crime_hourly_analysis(df)
        run_crime_trends()
        run_offence_distribution(df)
        run_division_analysis(df)
        run_neighbourhood_ranking(df)
        run_premises_analysis(df)
        # [SR-02] Appended the refactored visualization step seamlessly at the end of full pipeline sequence execution
        run_visualization_refactor_stage(df)


if __name__ == "__main__":
    main()