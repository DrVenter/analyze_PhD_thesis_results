"""
this function combines all data points from experimental repeats into one data file
"""

extension = ".csv"
file_root_name = "fibroblasts_cultured_in_serum_"
files_in_folder =["n=1", "n=2", "n=3"]

import numpy as np
import pandas as pd

def combine_experimental_repeats(files_in_folder, file_root_name, extension):
    matrix = []
    for file in files_in_folder:
        file_name = file_root_name + file
        file = open(file_name + extension)

        row_delimiter = "\n"
        column_delimiter = ","

        #first line of first file is the header we want
        header = file.readline().strip(row_delimiter).split(column_delimiter) 
        matrix = [header]

        for line in file:
            row = line.strip(row_delimiter).split(column_delimiter)
            if row == header:
                continue
            else: 
                matrix.append(row)

    matrix = np.array(matrix)
    data = pd.DataFrame(matrix)

    #set first row as header
    data.columns = data.iloc[0]
    data = data[1:]

    data.to_csv(f"{file_root_name}combined.csv", index=False)

combine_experimental_repeats(files_in_folder, file_root_name, extension)