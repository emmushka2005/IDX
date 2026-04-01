import pandas as pd
import glob
import os

dfs = []

for folder in ["", "raw"]:
    for file in os.listdir(folder if folder else "."):
        
        if file.endswith(".csv") and "sold" in file.lower():
            
            path = os.path.join(folder, file) if folder else file
            df = pd.read_csv(path, low_memory=False)
            dfs.append(df)

combined = pd.concat(dfs)

combined.to_csv("sold.csv", index=False)

print('Sold files successfuly combined.')


