import pandas as pd

def create_sample():
    print("Loading raw dataset...")
    # Read just the first 500 rows of the massive dataset
    df = pd.read_csv('data/Toronto_Crime_Indicators.csv', nrows=500)
    
    print("Saving sample dataset...")
    # Save it as a new, lightweight file
    df.to_csv('data/sample_crime_data.csv', index=False)
    print("Success! sample_crime_data.csv created in the data folder.")

if __name__ == "__main__":
    create_sample()