import pandas as pd
import os

dfs = []

for folder in ["", "raw"]:
    for file in os.listdir(folder if folder else "."):
        
        if file.endswith(".csv") and "listing" in file.lower():
            
            path = os.path.join(folder, file) if folder else file
            df = pd.read_csv(path)
            dfs.append(df)

combined = pd.concat(dfs)

combined.to_csv("listed.csv", index=False)

print('Listed files successfuly combined.')

