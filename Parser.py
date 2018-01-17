import re
import os
import csv

import PopupCreator
import PropertiesDictionaries

class Parser(object):
    def __init__(self):
        self.popup_creator = PopupCreator.PopupCreator()

    def check_file_extension(self, path_to_file):
        extension = os.path.split(path_to_file)[1].split(".")[1]
        if (extension == "csv" or extension == "txt"):
            return True
        return False

    def parse_file(self, path_to_file):
        if (not self.check_file_extension(path_to_file)):
            self.popup_creator.messagebox_popup("Wrong file format. Only .csv and .txt files can be loaded.")
            return False
        list_of_value_lines = []
        with open(path_to_file, "r") as file:
            csv_reader = csv.reader(file, delimiter=";")
            try:
                for line in csv_reader:
                    list_of_value_lines.append(line)
            except UnicodeDecodeError:
                self.popup_creator.messagebox_popup("File not properly converted to the .csv format.")
                return False
        if (not list_of_value_lines):
            self.popup_creator.messagebox_popup("File must not be empty.")
            return False
        temp_series_properties_dict = PropertiesDictionaries.create_series_properties_dict()
        proper_file_format = True
        value_line = ""
        for value_line in list_of_value_lines:
            for item in value_line:
                item = item.replace(",", ".")
                if (re.search("[^-0-9.]", item) or re.search(".+[-]|[-]\..*", item) or item == "." or item == "-" or 
                    item.count(".") > 1 or item.count("-") > 1):
                    proper_file_format = False
                    break
            if (not proper_file_format):
                break
            if (not value_line[0]):
                proper_file_format = False
                break
            if (len(value_line) == 1):
                proper_file_format = False
                break
            temp_series_properties_dict["x"].append(value_line[0])
            if (len(value_line) == 2):
                if (not value_line[1]):
                    proper_file_format = False
                    break
                temp_series_properties_dict["y"].append(value_line[1])
            elif (len(value_line) == 3):
                if (not value_line[1] or not value_line[2]):
                    proper_file_format = False
                    break
                temp_series_properties_dict["y"].append(value_line[1])
                temp_series_properties_dict["z"].append(value_line[2])
            elif (len(value_line) > 3):
                proper_file_format = False
                break
        if (proper_file_format):
            return temp_series_properties_dict
        self.popup_creator.messagebox_popup("Wrong file structure.\n"
                                            "Provide file that contains max of 3 numbers in one row (x,y,z) "
                                            "each in a separate column, number of columns in each row must be the same.\n"
                                            "x, y, z are floats/ints and use \".\" or \",\" for decimal part.\n"
                                            "In case of .txt file, columns should be separated with \";\"\n"
                                            "Line to check: {0}".format(value_line))
        return False

    def check_inserted_data_format(self, temp_series_properties_dict):
        dict_length = len(temp_series_properties_dict["x"])
        if (not dict_length):
            return False
        z_present = False
        if (temp_series_properties_dict["z"].count("") != len(temp_series_properties_dict["z"])):
            z_present = True
        for element_index in range(0, dict_length):
            if (not temp_series_properties_dict["x"][element_index] and
                (temp_series_properties_dict["y"][element_index] or z_present)):
                # x empty, y or z is not
                return False
            elif(temp_series_properties_dict["x"][element_index] and not temp_series_properties_dict["y"][element_index]):
                # x not empty, y empty
                return False
            elif(temp_series_properties_dict["x"][element_index] and temp_series_properties_dict["y"][element_index] and
                not temp_series_properties_dict["z"][element_index] and z_present): # x not empty, y not empty, z empty but should be present
                return False
        if (not z_present):
            temp_series_properties_dict["z"] = []
        return True
