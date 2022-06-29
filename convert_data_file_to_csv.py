import numpy as np
import pandas as pd

class Data_to_CSV:
    experimental_conditions = []
    bins = []
    matrix = []

    def __init__(self, file_name, extension):
        self.file_name = file_name
        self.extension = extension

        file = open(self.file_name + self.extension)

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

    def save_matrix_to_csv(self):
        data = pd.DataFrame(self.matrix)

        data.columns = data.iloc[0]
        data = data[1:]

        for row in data.index:
            if data.loc[row, "Label"] not in self.experimental_conditions:
                data.drop(row, inplace = True)

        data.to_csv(f"{file_name}.csv", index=False)

    def create_bin_intervals(self, start, end, number_of_bins):
        bin_intervals = []
        interval = (end - start)/number_of_bins

        for bin in range(number_of_bins):
            bin_intervals.append([round(start, 3), round(start + interval, 3)])
            start+=interval

        return bin_intervals

    def determine_frequency_distribution(self, label, attribute, number_of_bins, bins):
        header_row = 0
        column = np.where(self.matrix[header_row] == attribute)[0]
        label = np.where(self.matrix[: , 0] == label)
        x_axis = np.zeros((number_of_bins, 1), dtype=float)

        inner_element = 0
        lower_limit = 0
        upper_limit = 1
        for row in label[inner_element]: 
            for bin in range(len(bins)):
                if bins[bin][lower_limit] <= float(self.matrix[row, column][inner_element]) < bins[bin][upper_limit]:
                    x_axis[bin]+=1

        count = len(label[inner_element])
        for frequency_count in range(len(x_axis)): x_axis[frequency_count] = x_axis[frequency_count]/count * 100
        x_axis_percentage = np.around(x_axis, 2)

        return x_axis_percentage

    def create_frequency_distribution_matrix(self, attribute, start, end, number_of_bins):
        bins = self.create_bin_intervals(start, end, number_of_bins)

        x_axis_label = []
        lower_limit = 0
        upper_limit = 1
        for bin in range(len(bins)):
            lower_limit_label = str(bins[bin][lower_limit])
            upper_limit_label = str(bins[bin][upper_limit])
            x_axis_label.append([lower_limit_label + " - " + "<" + upper_limit_label])
        x_axis_label = np.array(x_axis_label)

        frequency_matrix = x_axis_label.copy()
        for label in self.experimental_conditions:
            temp = self.determine_frequency_distribution(label, attribute, number_of_bins, bins)
            frequency_matrix = np.concatenate((frequency_matrix, temp), axis=1)

        legend = ["Bins"] + self.experimental_conditions
        frequency_matrix = np.concatenate((np.array([legend]), frequency_matrix), axis=0)

        frequency_matrix = pd.DataFrame(frequency_matrix)
        frequency_matrix.columns = frequency_matrix.iloc[0]
        frequency_matrix = frequency_matrix[1:]
        frequency_matrix.to_csv(f"{file_name}_frequency_distribution_{attribute}.csv", index=False)

file_name = "fibroblasts_cultured_in_serum_n=1"
extension = ".xls"
data = Data_to_CSV(file_name, extension)
data.experimental_conditions = ['(1) LMTK 0%', '(2) LMTK 1%', '(3) LMTK 2%', '(4) LMTK 5%', '(5) LMTK 10%']
data.save_matrix_to_csv()

data.create_frequency_distribution_matrix(attribute="Circ.", start=0, end=1, number_of_bins=10)
data.create_frequency_distribution_matrix(attribute="Area", start=100, end=200, number_of_bins=10)
