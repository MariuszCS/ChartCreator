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

    def write_dicts_to_file(self, path_to_file, data_series_dict):
        with open(path_to_file, "w") as file_to_write:
            writer = csv.writer(file_to_write)
            for data_series_name, properties_dict in data_series_dict.items():
                writer.writerow([data_series_name])
                for key, value in properties_dict.items():
                    if (value is None):
                        writer.writerow([key, "None"])
                    else:
                        writer.writerow([key, value])
            writer.writerow(["Axes",""])
            for key, value in PropertiesDictionaries.axes_properties_dict.items():
                writer.writerow([key, value])
            writer.writerow(["Grid",""])
            for key, value in PropertiesDictionaries.grid_properties_dict.items():
                writer.writerow([key, value])
            writer.writerow(["Ticks",""])
            for key, value in PropertiesDictionaries.ticks_properties_dict.items():
                writer.writerow([key, value])
            writer.writerow(["Legend",""])
            for key, value in PropertiesDictionaries.legend_properties_dict.items():
                writer.writerow([key, value])
    
    def read_dicts_from_file(self, path_to_file, data_series_dict):
        with open(path_to_file, "r") as file_to_read:
            reader = csv.reader(file_to_read)
            data_series_name = ""
            axes_config = False
            grid_config = False
            ticks_config = False
            legend_config = False
            for line in reader:
                if (len(line) == 1):
                    data_series_name = line[0]
                    while data_series_name in list(data_series_dict.keys()):
                        data_series_name += "1"
                    data_series_dict[data_series_name] = PropertiesDictionaries.create_series_properties_dict()
                elif (len(line) == 2 and line[0] != "Axes" and not axes_config and not grid_config and 
                        not ticks_config and not legend_config):
                    if (line[1] == "None"):
                        data_series_dict[data_series_name][line[0]] = None
                    elif (re.search("\[", line[1])):
                        line[1] = line[1].replace("[", "")
                        line[1] = line[1].replace("]", "")
                        line[1] = line[1].replace(" ", "")
                        line[1] = line[1].split(",")
                        if (line[1] != [""]):
                            data_series_dict[data_series_name][line[0]] = [float(value) for value in line[1]]
                        else:
                            data_series_dict[data_series_name][line[0]] = []
                    elif (re.search("\{", line[1])):
                        line[1] = line[1].replace("{", "")
                        line[1] = line[1].replace("}", "")
                        line[1] = line[1].replace(" ", "")
                        line[1] = line[1].replace("\'", "")
                        line[1] = line[1].split(",")
                        data_series_dict[data_series_name][line[0]] = PropertiesDictionaries.create_dict_for_open_button(data_series_dict[data_series_name]["chart_type"])
                        for dict_pair in line[1]:
                            dict_pair = dict_pair.split(":")
                            if (re.search("[0-9]", dict_pair[1]) and not re.search("[#]", dict_pair[1]) and
                                dict_pair[0] != "marker"):
                                data_series_dict[data_series_name][line[0]][dict_pair[0]] = float(dict_pair[1])
                            elif (dict_pair[1] == "None"):
                                data_series_dict[data_series_name][line[0]][dict_pair[0]] = None
                            elif (dict_pair[1] == "True"):
                                data_series_dict[data_series_name][line[0]][dict_pair[0]] = True
                            elif (dict_pair[1] == "False"):
                                data_series_dict[data_series_name][line[0]][dict_pair[0]] = False
                            else:
                                data_series_dict[data_series_name][line[0]][dict_pair[0]] = dict_pair[1]
                    elif (line[0] == "artist"):
                        data_series_dict[data_series_name][line[0]] = None
                    else:
                        data_series_dict[data_series_name][line[0]] = line[1]
                elif (line):
                    if (axes_config and line[0] != "Grid"):
                        self.assign_value_to_key(PropertiesDictionaries.axes_properties_dict, line[0], line[1])
                    elif (grid_config and line[0] != "Ticks"):
                        self.assign_value_to_key(PropertiesDictionaries.grid_properties_dict, line[0], line[1])
                    elif (ticks_config and line[0] != "Legend"):
                        self.assign_value_to_key(PropertiesDictionaries.ticks_properties_dict, line[0], line[1])
                    elif (legend_config):
                        self.assign_value_to_key(PropertiesDictionaries.legend_properties_dict, line[0], line[1])
                    if (line[0] == "Axes"):
                        axes_config = True
                    elif (line[0] == "Grid"):
                        axes_config = False
                        grid_config = True
                    elif (line[0] == "Ticks"):
                        grid_config = False
                        ticks_config = True
                    elif (line[0] == "Legend"):
                        ticks_config = False
                        legend_config = True

    def assign_value_to_key(self, properties_dict, key, value):
        if (key == "scatterpoints"):
            properties_dict[key] = int(value)
        elif (value == "True"):
            properties_dict[key] = True
        elif (value == "False"):
            properties_dict[key] = False
        elif (re.search("[0-9]", value) and not re.search("[#]", value)):
            properties_dict[key] = float(value)
        else:
            properties_dict[key] = value