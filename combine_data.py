import pandas as pd
import os

csv_folder = "annotated_data"

dataframes = []

for filename in os.listdir(csv_folder):
    if filename.endswith(".csv"):
        filepath = os.path.join(csv_folder, filename)
        df = pd.read_csv(filepath)
        
        #add a "Video ID" column to identify which video the data comes from
        df["Video ID"] = os.path.splitext(filename)[0]
        dataframes.append(df)

#combine all CSVs into one dataframe
combined_df = pd.concat(dataframes, ignore_index=True)

#save the combined dataframe for future use
combined_df.to_csv("combined_data.csv", index=False)
print("Combined dataset saved as combined_data.csv.")

print(combined_df.head())
print(combined_df.info())
print(combined_df["Action"].value_counts())  
