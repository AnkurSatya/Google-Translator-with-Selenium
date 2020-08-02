from glob import glob
import pickle
import pandas as pd
import numpy as np

# Extracting data frames from pickle files.
for file in glob("./data/translated/pickle/*"):
    with open(file, 'rb') as f:
        # Loaded as dataframe
        data = pickle.load(f)
    output_filename = file.replace("pickle","csvs").replace(".pkl",".csv")
    data.to_csv(output_filename)

# Creating a list of files where column 'original_index' is absent
files_without_index_col = []
for file in glob("./data/translated/csvs/*"):
    data = pd.read_csv(file)
    
    #Making a list of columns in the df
    cols = list(data.columns)
    
    if "original_index" not in cols:
        files_without_index_col.append(file)


# Adding 'original_index' column to those files
for file in files_without_index_col:
    # Extracting start index and the end index from the filename.
    tmp = file.split("/")[-1].split("_")
    start_idx = int(tmp[-2])
    end_idx = int(tmp[-1].replace(".csv",""))
    print(file)
    print(start_idx, end_idx)
    
    original_index_col_vals = np.arange(start_idx, end_idx, 1)
    
    #Appending this column to the translated dataframe
    data = pd.read_csv(file)
    data["original_index"] = original_index_col_vals
    data.to_csv(file)
    

# Creating a set of failure indices by combining failures.txt for all the batches
failure_indices = set()
for file in glob("./data/failures/10000+/*"):
    with open(file) as f:
        for row in f.readlines():
            failure_indices.add(int(row))
print(len(failure_indices))
print(failure_indices)
    

original_data = pd.read_csv("./Dataset.csv")

# Creating a new dataframe consisting of rows corresponding to failure indices
failure_rows = []
for i, val in original_data.iterrows():
    if i in failure_indices:
        failure_rows.append(val)
        
        
failure_df = pd.DataFrame(failure_rows, columns=["context","question","text"])

# Appending a new column, 'original_index' to the dataframe. Need to do this because this dataframe will be translated
# separately. So, we must know the original indices so that we can merge this dataframe with all other dataframes.
# If you have a doubt anywhere in the code, just try printing things one by one. You will understand everything.
failure_df["original_index"] = list(failure_df.index)
failure_df


failure_df.to_csv("failure_data_10000+.csv", index=False)