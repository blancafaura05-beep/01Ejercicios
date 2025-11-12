import os
import pandas as pd

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")

# Create processed folder if it doesn't exist
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Get all CSV files in downloads
csv_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".csv")]

if not csv_files:
    print("No CSV files found in the 'downloads' folder.")
    exit()

results = []

# Loop through each CSV
for file in csv_files:
    path = os.path.join(DOWNLOAD_DIR, file)
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"Error reading {file}: {e}")
        continue

    # Find the duration column (name changes between years)
    duration_col = None
    for col in df.columns:
        if "duration" in col.lower():
            duration_col = col
            break

    if duration_col is None:
        print(f"No duration column found in {file}. Skipping.")
        continue

    # Convert to numeric and calculate mean
    df[duration_col] = pd.to_numeric(df[duration_col], errors="coerce")
    mean_duration = df[duration_col].mean()

    results.append({
        "file": file,
        "mean_trip_time_seconds": round(mean_duration, 2)
    })

    print(f"{file}: mean trip time = {mean_duration:.2f} seconds")

# Save summary
results_df = pd.DataFrame(results)
output_path = os.path.join(PROCESSED_DIR, "mean_trip_time_per_quarter.csv")
results_df.to_csv(output_path, index=False)

print(f"\nSummary saved to: {output_path}")