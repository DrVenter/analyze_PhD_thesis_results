import numpy as np
import pandas as pd

class Data_to_CSV:
    experimental_conditions = []
    
    def __init__(self, file_name, extension):
        self.file_name = file_name
        self.extension = extension

        file = open(self.file_name + self.extension)
        self.matrix = []

        row_delimiter = "\n"
        column_delimiter = "\t"
        for line in file:
            self.matrix.append(line.strip(row_delimiter).split(column_delimiter))

        self.matrix = np.array(self.matrix)

        index_column = 0
        self.matrix = np.delete(self.matrix, index_column, axis=1) 

        length_of_text_to_remove = 7
        header_row = 0
        label_column = 0
        for row in range(len(self.matrix[header_row+1:, label_column])):
            self.matrix[row, label_column] = self.matrix[row, label_column][0:-length_of_text_to_remove]
        self.matrix[0,0] = "Label" #not quite sure why this gets removed

file_name = "fibroblasts_cultured_in_serum_n=1"
extension = ".xls"
data = Data_to_CSV(file_name, extension)

data.experimental_conditions = ['(1) LMTK 0%', '(2) LMTK 1%', '(3) LMTK 2%', '(4) LMTK 5%', '(5) LMTK 10%']

def distribution(start, end, number_of_bins):
    distribution = []
    interval = (end - start)/number_of_bins

    for x in range(number_of_bins):
        distribution.append([round(start, 3), round(start + interval, 3)])
        start+=interval

    return distribution

bins = distribution(0, 1, 10)

def frequency_distribution(label, characteristic, bins):
    col = np.where(matrix[0] == characteristic)[0]
    label = np.where(matrix[: , 0] == label)
    x_axis = np.zeros((len(bins), 1), dtype=float)

    for x in label[0]: 
        for y in range(len(bins)):
            if bins[y][0] <= float(matrix[x, col][0]) < bins[y][1]:
                x_axis[y]+=1

    count = len(label[0])
    for x in range(len(x_axis)): x_axis[x] = x_axis[x]/count * 100
    x_axis = np.around(x_axis, 2)
    #x_axis = x_axis.astype(str)

    return x_axis

#print(frequency_distribution(experimental_conditions[2], "Circ.", bins))

x_axis_label = []
for x in range(len(bins)):
    x_axis_label.append([str(bins[x][0]) + " - " + "<" + str(bins[x][1])])
x_axis_label = np.array(x_axis_label)

frequency_matrix = x_axis_label.copy()
for x in experimental_conditions:
    temp = frequency_distribution(x, "Circ.", bins)
    frequency_matrix = np.concatenate((frequency_matrix, temp), axis=1)

#print(frequency_matrix)

legend = ["bins"] + experimental_conditions
frequency_matrix = np.concatenate((np.array([legend]), frequency_matrix), axis=0)
print(frequency_matrix)


data = pd.DataFrame(matrix)
data.columns = data.iloc[0]
data = data[1:]

for x in data.index:
    if data.loc[x, "Label"] not in experimental_conditions:
        data.drop(x, inplace = True)

#data.to_csv(f"{file_name}.csv", index=False)

