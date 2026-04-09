import pandas as pd
import os

dfs = []
file_row_counts = {}

# Load Files
for folder in ["", "raw"]:
    for file in os.listdir(folder if folder else "."):
        
        if file.endswith(".csv") and "listing" in file.lower():
            
            path = os.path.join(folder, file) if folder else file
            df = pd.read_csv(path)
            
            dfs.append(df)
            file_row_counts[path] = len(df)

# Row Counts
print("\nRow count per file BEFORE append:")
for path, count in file_row_counts.items():
    print(f"{path}: {count}")

# Concatenate
combined = pd.concat(dfs)

# Check
print(f"\nRow count AFTER concatenation: {len(combined)}")

# PropertyType distribution before filter 
if "PropertyType" in combined.columns:
    print("\nPropertyType distribution BEFORE filter:")
    print(combined["PropertyType"].value_counts(dropna=False))

    # Residential filter 
    filtered = combined[combined["PropertyType"] == "Residential"]

    # Row count after filter 
    print(f"\nRow count AFTER Residential filter: {len(filtered)}")

    # PropertyType distribution after filter 
    print("\nPropertyType distribution AFTER filter:")
    print(filtered["PropertyType"].value_counts(dropna=False))

else:
    print("\nWARNING: 'PropertyType' column not found. Skipping filter.")
    filtered = combined

# Save
filtered.to_csv("listed.csv", index=False)

print('\nListed files successfully combined.')