import numpy as np
import pandas as pd

file_name = "fibroblasts_cultured_in_serum_n=1"
extension = ".csv"

data = pd.read_csv(file_name + extension)

print(data.head())
print(data.groupby("Label")["Circ."].describe())