"""
this script combines the frequency distribution data and finds the average and standard deviations
"""

extension = ".csv"
file_root_name = ["fibroblasts_cultured_in_serum_", "_frequency_distribution_"]
files_in_folder =["n=1", "n=2", "n=3"]
attributes = ["Circ.", "Area"]

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

for attribute in attributes:
    combined_matrix = []
    header = []
    index = []

    for file in files_in_folder:
        file_name = file_root_name[0] + file + file_root_name[1] + attribute
        file = open(file_name + extension)

        file_matrix = []
        row_delimiter = "\n"
        column_delimiter = ","

        for row in file:
            file_matrix.append(row.strip(row_delimiter).split(column_delimiter))
        combined_matrix.append(file_matrix)

        file_matrix = np.array(file_matrix)
        header = file_matrix[0, :]
        index = file_matrix[1:, 0]
        #top_left = file_matrix[0,0]

    combined_matrix = np.array(combined_matrix)
    values = combined_matrix[:, 1:, 1:].astype(float)

    number_of_matrices = len(values)
    number_of_rows = len(values[0])
    number_of_columns = len(values[0][0])

    averages = np.zeros((number_of_rows, number_of_columns), dtype=float)
    standard_deviation = averages.copy()

    for row in range(number_of_rows):
        for column in range(number_of_columns):
            averages[row,column] = np.round(np.mean(values[:, row, column]), 2)
            standard_deviation[row,column] = np.round(np.std(values[:, row, column]), 2)

    number_of_index_columns = 1
    
    index  = index.reshape(number_of_rows, number_of_index_columns)
    averages = np.hstack((index, averages))
    averages = np.vstack((header, averages))
    averages = pd.DataFrame(averages)
    averages.to_csv(f"{file_root_name[0]}combined{file_root_name[1]}{attribute}.csv", header=False, index=False)
