# See how usage evolves by user type (Member vs Casual)
import os
import pandas as pd
import matplotlib.pyplot as plt

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")

# Get CSV files
csv_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".csv")]

if not csv_files:
    print("No CSV files found in the 'downloads' folder.")
    exit()

# Prepare results
user_counts = []

for file in csv_files:
    path = os.path.join(DOWNLOAD_DIR, file)
    df = pd.read_csv(path)

    # Try to find user type column (can vary by year)
    user_col = None
    for col in df.columns:
        if "user" in col.lower() or "member" in col.lower():
            user_col = col
            break

    if user_col is None:
        print(f"No user type column found in {file}. Skipping.")
        continue

    counts = df[user_col].value_counts(dropna=False)
    total = counts.sum()
    member = counts.get("Subscriber", 0) + counts.get("member", 0)
    casual = counts.get("Customer", 0) + counts.get("casual", 0)

    user_counts.append({
        "file": file,
        "member": member,
        "casual": casual,
        "total": total
    })

# Create a DataFrame
result_df = pd.DataFrame(user_counts)

# Plot a simple bar chart
plt.figure(figsize=(8, 5))
plt.bar(result_df["file"], result_df["member"], label="Member")
plt.bar(result_df["file"], result_df["casual"], bottom=result_df["member"], label="Casual")
plt.title("Bike Usage by User Type per Quarter")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Number of Trips")
plt.legend()
plt.tight_layout()
plt.show()
