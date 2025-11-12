import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")

# Check if the folder exists
if not os.path.exists(DOWNLOAD_DIR):
    print("The 'downloads' folder does not exist. Run the download script first.")
    exit()

# List all CSV files in the folder
csv_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".csv")]

if not csv_files:
    print("No CSV files found in the 'downloads' folder.")
    exit()

# Loop through each CSV file and show basic information
for file in csv_files:
    path = os.path.join(DOWNLOAD_DIR, file)
    print(f"\nAnalyzing {file}")
    
    # Read the CSV file
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"Error reading file: {e}")
        continue

    # General info
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Show column names
    print("Columns:")
    print(list(df.columns))

    # Count missing values
    nulls = df.isna().sum()
    total_nulls = nulls.sum()
    print(f"Total missing values: {total_nulls}")

    # Show columns with missing values
    if total_nulls > 0:
        print("Columns with missing values:")
        print(nulls[nulls > 0])

    # Show data types
    print("Data types:")
    print(df.dtypes.head())

    # Show first few rows as an example
    print("First rows:")
    print(df.head(3))