##### DELTA change for SWAT+ (Uses SWAT+ files .TMP) and generates again SWAT+ file (not input files)
##### Also you must change the directory. This is only for .TMP files.
##### You must use monthly abs change for MAX and MIN tmp.
##### Developed by MR.Eini mohammad_eini@sggw.edu.pl



import numpy as np
from calendar import monthrange
import os


def file_name_finder(folder_dir='tmp_pcp'):    #directory
    files_name_list = os.listdir(folder_dir)
    list_of_file_number = []
    for item in files_name_list:
        if item[:3] == 'tmp':
            list_of_file_number.append(item[3:-4])
    return list_of_file_number


class Tmp_File:
    def __init__(self, file_number):
        self.file_number = file_number
        self.file_address = 'tmp_pcp/tmp' + self.file_number + '.tmp'    #only TMP
        self.data_table = self.get_data()
        self.header = self.get_header()

    def get_data(self):
        f = open(self.file_address, "r")
        data = f.read().splitlines()[3:]
        for _ in range(len(data)):
            data[_] = data[_].split()
        return data

    def get_header(self):
        f = open(self.file_address, "r").read()
        return f.splitlines()[:3]


class Tmp_Table:
    def __init__(self, input_table):
        self.first_year = 1990
        self.last_year = 2019
        self.number_of_days = 10957
        self.table = self.table_creator(input_table)

    def table_creator(self, input_table):
        table = []
        counter = 0
        for year_number in range(self.first_year, self.last_year + 1):
            day_counter = 1
            for month_number in range(1, 13):
                for day_in_month in range(1, monthrange(year_number, month_number)[1] + 1):
                    table.append([year_number, day_counter, month_number, float(input_table[counter][2]),
                                  float(input_table[counter][3])])
                    counter += 1
                    day_counter += 1
        return table


class Tmp_Scenario:
    def __init__(self, file_number, input_table, header):
        self.change_parameters = [[4.33, 4.47, 4.37, 4.02, 3.83, 4.11, 4.91, 5.74, 5.92, 5.42, 4.79, 4.38], #monthly changes for MAX Jan to Dec
                                  [4.56, 4.80, 4.53, 4.00, 3.61, 3.57, 4.04, 4.66, 4.87, 4.59, 4.25, 4.24]] #monthly changes for MIN Jan to Dec
        self.table = self.scenario(input_table)
        self.save_results(file_number, header)

    def scenario(self, input_table):
        table = input_table
        for _ in range(len(table)):
            month_number = table[_][2]

            first_parameter = self.change_parameters[0][month_number - 1]
            table[_][3] = round(table[_][3] + first_parameter, 2)

            second_parameter = self.change_parameters[1][month_number - 1]
            table[_][4] = round(table[_][4] + second_parameter, 2)

        return table

    def save_results(self, file_number, header):
        output_table = ''
        for item in header:
            output_table += item + '\n'
        for line in self.table:
            output_table += line[0].__str__() + '\t' + line[1].__str__() + '\t' + line[3].__str__() + '\t' + \
                            line[4].__str__() + '\n'
        with open('result-tmp_pcp/tmp' + file_number + '.tmp', "w") as output:   #format
            output.write(output_table)


try:
    os.makedirs('result-tmp_pcp')   #directory
except:
    print('The "result-tmp_pcp" directory is already exist!')

list_of_file_numbers = file_name_finder()
for f_number in list_of_file_numbers:
    tmp_file = Tmp_File(f_number)
    input_table = tmp_file.data_table
    new_table = Tmp_Table(input_table).table
    Tmp_Scenario(f_number, new_table, header=tmp_file.header)
