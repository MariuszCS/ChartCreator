from PopupCreator import *

import re
import os


class Parser(object):
    def __init__(self):
        self.popup_creator = PopupCreator()

    def check_file_extension(self, path_to_file):
        extension = os.path.split(path_to_file)[1].split(".")[1]
        if (extension == "csv" or extension == "txt"):
            return True
        return False

    def parse_file(self, path_to_file):
        proper_file_format = True
        first_run = True
        temp_value_line = []
        if (not self.check_file_extension(path_to_file)):
            self.popup_creator.messagebox_popup("Wrong file format. Only .csv and .txt files can be loaded.")
            return False
        with open(path_to_file, "r") as f:
            file = f.read()
        list_of_value_lines = file.split("\n")
        if (not list_of_value_lines[-1]):
            list_of_value_lines.pop()
        temp_series_properties_dict = create_series_properties_dict()
        value_line = ""
        for value_line in list_of_value_lines:
            if (first_run):
                first_run = False
                if (value_line[0] >= bytes.decode(b'\xc2\x80') and value_line[0] <= bytes.decode(b'\xd1\xbf') and
                        not re.search("[a-zA-Z]", value_line[0])):
                    value_line = value_line[
                                 3:]  # 3 first characters can be some trash left from conversion from xlsx to csv file
            if (re.search("[^-;0-9,.]", value_line)):
                proper_file_format = False
                break
            value_line = value_line.replace(",", ".")
            split_value_line = value_line.split(";")
            for item in split_value_line:
                if (item == "." or item == "-"):
                    proper_file_format = False
                    break
                if (item.count(".") > 1 or item.count("-") > 1):
                    proper_file_format = False
                    break
                if (re.match(".+[-]", item)):
                    proper_file_format = False
                    break
            if (not proper_file_format):
                break
            if (not split_value_line[0]):
                proper_file_format = False
                break
            if (len(split_value_line) == 1):
                proper_file_format = False
                break
            temp_series_properties_dict["x"].append(split_value_line[0])
            if (len(split_value_line) == 2):
                if (not split_value_line[1]):
                    proper_file_format = False
                    break
                temp_series_properties_dict["y"].append(split_value_line[1])
            elif (len(split_value_line) == 3):
                if (not split_value_line[1] or not split_value_line[2]):
                    proper_file_format = False
                    break
                temp_series_properties_dict["y"].append(split_value_line[1])
                temp_series_properties_dict["z"].append(split_value_line[2])
            elif (len(split_value_line) > 3):
                proper_file_format = False
                break
        if (proper_file_format):
            return temp_series_properties_dict
        self.popup_creator.messagebox_popup("Wrong file structure.\n"
                                            "Provide file that contains max of 3 numbers in one row (x,y,z) "
                                            "each in a separate column, number of columns in each row must be the same.\n"
                                            "x, y, z are floats/ints and use \",\" or \".\" for decimal part.\n"
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
