##### DELTA change for SWAT+ (Uses SWAT+ files) and generates again SWAT+ file (not input files)
##### Also you must change the directory. Also, be careful about extension (PCP, SLR, HMD, WND)
##### You must use percentage change not abs change 
##### Developed by MR.Eini:  mohammad_eini@sggw.edu.pl

import numpy as np
from calendar import monthrange
import os


def file_name_finder(folder_dir='tmp_pcp'):    ###directory
    files_name_list = os.listdir(folder_dir)
    list_of_file_number = []
    for item in files_name_list:
        if item[:3] == 'pcp':
            list_of_file_number.append(item[3:-4])
    return list_of_file_number


class Pcp_File:
    def __init__(self, file_number):
        self.file_number = file_number
        self.file_address = 'tmp_pcp/pcp' + self.file_number + '.pcp'   #format
        self.data_table = self.get_data()
        self.header = self.get_header()

    def get_data(self):
        f = open(self.file_address, "r").read()
        data = f.splitlines()[3:]
        for _ in range(len(data)):
            data[_] = data[_].split()
        return data

    def get_header(self):
        f = open(self.file_address, "r").read()
        return f.splitlines()[:3]

class Pcp_Table:
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
                    table.append([year_number, day_counter, month_number, float(input_table[counter][2])])
                    counter += 1
                    day_counter += 1
        return table


class Pcp_Scenario:
    def __init__(self, file_number, input_table, header):
        self.change_parameters = [.21, .23, .25, .24, .16, .05, -.05, -.14, -.14, -.04, .09, .18]  #### Monthly change
        self.table = self.scenario(input_table)
        self.save_results(file_number, header)

    def scenario(self, input_table):
        table = input_table
        for _ in range(len(table)):
            if not table[_][3] == 0:
                month_number = table[_][2]
                parameter = self.change_parameters[month_number - 1]
                table[_][3] = round(table[_][3] + parameter * table[_][3], 2)

        return table

    def save_results(self, file_number, header):
        output_table = ''
        for item in header:
            output_table += item + '\n'
        for line in self.table:
            output_table += line[0].__str__() + '\t' + line[1].__str__() + '\t' + line[3].__str__() + '\n'
        with open('result-tmp_pcp/pcp' + file_number + '.pcp', "w") as output:     #directory and format
            output.write(output_table)


try:
    os.makedirs('result-tmp_pcp')           #directory
except:
    print('The "result-tmp_pcp" directory is already exist!')

list_of_file_numbers = file_name_finder()
for f_number in list_of_file_numbers:
    pcp_file = Pcp_File(f_number)
    input_table = pcp_file.data_table
    new_table = Pcp_Table(input_table).table
    Pcp_Scenario(f_number, new_table, header=pcp_file.header)
