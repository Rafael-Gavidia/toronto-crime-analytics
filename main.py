import os
import pandas as pd
from src.cleaner import clean_crime_data

def main():
    input_file = "data/Toronto_Crime_Indicators.csv"
    output_file = "data/Toronto_Crime_Indicators_Cleaned.csv"
    
    # Check if the source dataset exists
    if not os.path.exists(input_file):
        print(f"Error: Source file '{input_file}' not found in the current directory.")
        print("Please ensure the CSV file is placed in the root of the project.")
        return

    print("Loading raw dataset...")
    df_raw = pd.read_csv(input_file, low_memory=False)
    
    initial_rows = len(df_raw)
    print(f"Initial dataset size: {initial_rows:,} rows")
    print("-" * 50)

    print("Running data cleaning pipeline (clean_crime_data)...")
    df_cleaned = clean_crime_data(df_raw)
    final_rows = len(df_cleaned)
    print("Data cleaning completed successfully!")
    print("-" * 50)

    # ==================== CLEANING METRICS REPORT ====================
    dropped_rows = initial_rows - final_rows
    drop_percentage = (dropped_rows / initial_rows) * 100

    print("DATA CLEANING METRICS REPORT:")
    print(f"• Dropped rows (invalid coordinates / unparsable dates): {dropped_rows:,} ({drop_percentage:.2f}%)")
    print(f"• Final valid rows remaining: {final_rows:,}")
    
    # Calculate NSA placeholders before and after for validation
    raw_nsa_count = (df_raw.select_dtypes(include=['object']) == "NSA").sum().sum()
    cleaned_nsa_count = (df_cleaned.select_dtypes(include=['object']) == "NSA").sum().sum()
    print(f"• Total 'NSA' placeholders detected before cleaning: {raw_nsa_count:,}")
    print(f"• Total 'NSA' placeholders remaining after cleaning: {cleaned_nsa_count}")
    
    # Verify the target column datatype
    print(f"• New data type for 'OCC_DATE' column: {df_cleaned['OCC_DATE'].dtype}")
    print("-" * 50)

    # ==================== SAVING THE OUTPUT ====================
    print(f"Saving cleaned dataset to '{output_file}'...")
    df_cleaned.to_csv(output_file, index=False)
    print("Done! The processed dataset is now fully ready for precise analysis.")

if __name__ == "__main__":
    main()