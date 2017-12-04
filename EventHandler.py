from Parser import *
from PopupCreator import *
from PropertiesDictionaries import *

import matplotlib.artist as mat_art
from matplotlib.lines import Line2D

import time

class EventHandler(object):
    def __init__(self):
        self.parser = Parser()
        self.popup_creator = PopupCreator()
        self.data_series_name = ""
        self.data_series_dict = {}  # data series dict with key = "data_series_name" value = self.create_coordinates_dict()
        self.proper_name = True
        self.color = "#000000"

    def event_for_load_button(self, data_series_combobox):
        path_to_file = self.popup_creator.popup_for_openfile()
        if (path_to_file):
            temp_series_properties_dict = self.parser.parse_file(path_to_file)
            if (temp_series_properties_dict):
                file_name = os.path.split(path_to_file)[1].split(".")[0]
                self.popup_creator.popup_for_provide_name(file_name, lambda: self.event_for_submit_name_button(temp_series_properties_dict, data_series_combobox),
                                                          lambda: self.event_for_close_popup_button(
                                                              self.popup_creator.provide_name_popup))

    def rewrite_values_to_data_series_dict(self, temp_series_properties_dict):
        self.data_series_dict[self.data_series_name] = create_series_properties_dict()
        self.data_series_dict[self.data_series_name]["x"] = [float(element) for element in temp_series_properties_dict["x"]]
        self.data_series_dict[self.data_series_name]["y"] = [float(element) for element in temp_series_properties_dict["y"]]
        self.data_series_dict[self.data_series_name]["z"] = [float(element) for element in temp_series_properties_dict["z"]]

    def event_for_submit_name_button(self, temp_series_properties_dict, data_series_combobox):
        if (self.check_name()):
            self.rewrite_values_to_data_series_dict(temp_series_properties_dict)
            self.event_for_update_data_series_combobox(data_series_combobox)
            data_series_combobox.current(len(data_series_combobox["values"]) - 1)
            self.event_for_close_popup_button(self.popup_creator.provide_name_popup)
            data_series_combobox.event_generate("<<ComboboxSelected>>")
        else:
            self.popup_creator.provide_name_popup.lift()

    def check_name(self):
        # checks if the name is not empty or if it already exists
        self.data_series_name = self.popup_creator.name_entry.get()
        if (not self.data_series_name):
            self.popup_creator.messagebox_popup("Name must not be empty.")
            return False
        for data_series_name in self.data_series_dict:
            if (self.data_series_name == data_series_name):
                self.popup_creator.messagebox_popup("Name: \"{0}\" already exists!".format(self.data_series_name))
                return False
        return True

    def event_for_close_popup_button(self, popup):
        if (self.popup_creator.excel_sheet_popup == popup):
            #clear entries list if the popup was excel_sheet_popup
            self.popup_creator.entry_list = []
        popup.grab_release() # release focus
        popup.quit() # escape the mainloop()
        popup.destroy() # destroy the popup

    def event_for_update_data_series_combobox(self, data_series_combobox):
        # command run every time user clicks on the arrow of the combobox
        data_series_combobox.config(values=[data_series_name for data_series_name in self.data_series_dict.keys()])

    def event_for_color_chooser_button(self, chosen_color_label, chosen_color_preview_label, data_series_name, canvas, plot):
        new_color = colorchooser.askcolor(initialcolor="#000000")[1]
        if (new_color and new_color != self.color):
            #if the color has been chosen and is different than previous one
            self.color = new_color
            self.update_color_labels(chosen_color_label, chosen_color_preview_label, self.color)
            if (self.data_series_dict and self.data_series_dict[data_series_name]["artist"]):
                # if the data series is plotted, change its color
                mat_art.setp(self.data_series_dict[data_series_name]["artist"], color=self.color)
                self.data_series_dict[data_series_name]["color"] = self.color
                self.update_legend(plot)
                canvas.show()

    def data_series_combobox_callback(self, data_series_name, chosen_color_label, chosen_color_preview_label, chart_type,
                                      name_entry):
        if (self.data_series_dict.keys()):
            if (self.data_series_dict[data_series_name]["artist"]):
                # update color in hex and preview in the color label to the color of the plot of this data series
                self.color = self.data_series_dict[data_series_name]["color"]
                self.update_color_labels(chosen_color_label, chosen_color_preview_label, self.color)
            else:
                # update color in hex and preview in the color label to the default color (black)
                self.color = "#000000"
                self.update_color_labels(chosen_color_label, chosen_color_preview_label, self.color)
            # set radiobutton to the chart_type of the data series (if plotted data series is line, line radiobutton will be set,
            # if the data series is not plotted, all radio buttons will be cleared etc.)
            chart_type.set(self.data_series_dict[data_series_name]["chart_type"])
            # remove anything that is present in name_entry, but only in case if it is different than the plot_name of current data series,
            # and set it to the plot_name of current data series
            if (name_entry.get() != self.data_series_dict[data_series_name]["plot_name"]):
                name_entry.delete(0, len(name_entry.get()))
                name_entry.insert(0, self.data_series_dict[data_series_name]["plot_name"])
        else:
            name_entry.delete(0, len(name_entry.get()))
            chart_type.set("")
            self.update_color_labels(chosen_color_label, chosen_color_preview_label, "")

    def update_color_labels(self, chosen_color_label, chosen_color_preview_label, color):
        # update text and color in preview label
        chosen_color_label.config(text="Chosen color (hex): {0}".format(color))
        chosen_color_preview_label.config(background=color)

    def event_for_delete_button(self, data_series_combobox, canvas, plot):
        data_series_name = data_series_combobox.get()
        if (data_series_name):
            if (self.data_series_dict[data_series_name]["artist"]):
                self.data_series_dict[data_series_name]["artist"].remove()
                self.data_series_dict[data_series_name]["artist"] = None
                self.update_legend(plot)
                canvas.show()
            del self.data_series_dict[data_series_name]
            if (data_series_combobox.current()):
                data_series_combobox.current(data_series_combobox.current() - 1)
            elif (not data_series_combobox.current() and len(data_series_combobox["values"]) > 1):
                data_series_combobox.current(data_series_combobox.current() + 1)
            else:
                data_series_combobox.set("")
            self.event_for_update_data_series_combobox(data_series_combobox)
            data_series_combobox.event_generate("<<ComboboxSelected>>")
        else:
            self.popup_creator.messagebox_popup("Choose data series.")

    def event_for_insert_button(self, data_series_combobox):
        self.popup_creator.popup_for_excel_sheet(
            "Insert data series...",
            lambda: self.event_for_close_popup_button(self.popup_creator.excel_sheet_popup),
            lambda: self.event_for_submit_insert_button(data_series_combobox),
            lambda: self.event_for_add_row_button())
        self.popup_creator.excel_sheet_popup.mainloop()

    def event_for_submit_insert_button(self, data_series_combobox):
        if (self.check_name()):
            self.check_format_and_rewrite_to_dict(data_series_combobox)
        else:
            self.popup_creator.excel_sheet_popup.lift()

    def check_format_and_rewrite_to_dict(self, data_series_combobox):
        temp_series_properties_dict = create_series_properties_dict()
        for entry_number in range(0, len(self.popup_creator.entry_list), 3):
            x_entry_content = self.popup_creator.entry_list[entry_number].get()
            y_entry_content = self.popup_creator.entry_list[entry_number + 1].get()
            z_entry_content = self.popup_creator.entry_list[entry_number + 2].get()
            if (not x_entry_content and not y_entry_content and not z_entry_content):
                pass
            else:
                temp_series_properties_dict["x"].append(x_entry_content)
                temp_series_properties_dict["y"].append(y_entry_content)
                temp_series_properties_dict["z"].append(z_entry_content)
        if (self.parser.check_inserted_data_format(temp_series_properties_dict)):
            self.rewrite_values_to_data_series_dict(temp_series_properties_dict)
            self.event_for_update_data_series_combobox(data_series_combobox)
            data_series_combobox.current(len(data_series_combobox["values"]) - 1)
            self.event_for_close_popup_button(self.popup_creator.excel_sheet_popup)
            data_series_combobox.event_generate("<<ComboboxSelected>>")
        else:
            temp_series_properties_dict = []
            self.popup_creator.messagebox_popup("Please check if the entered field are well aligned.")
            self.popup_creator.excel_sheet_popup.lift()

    def event_for_add_row_button(self):
        self.popup_creator.add_entry()
        self.popup_creator.update_scroll_region()

    def event_for_modify_button(self, data_series_combobox):
        self.data_series_name = data_series_combobox.get()
        if (self.data_series_name):
            self.popup_creator.popup_for_excel_sheet(
                "Modify data series...",
                lambda: self.event_for_close_popup_button(self.popup_creator.excel_sheet_popup),
                lambda: self.event_for_submit_modify_button(data_series_combobox),
                lambda: self.event_for_add_row_button())
            self.fill_excel_sheet_popup(data_series_combobox)
            self.popup_creator.excel_sheet_popup.mainloop() # needs to be here so self.fill_excel_sheet_popup(data_series_combobox)
                                                            # will be executed before the popup will show
        else:
            self.popup_creator.messagebox_popup("Choose data series.")
            return

    def fill_excel_sheet_popup(self, data_series_combobox):
        self.popup_creator.name_entry.insert(0, self.data_series_name)
        if (len(self.data_series_dict[self.data_series_name]["x"]) > int(len(self.popup_creator.entry_list) / 3)):
            for _ in range(0, len(self.data_series_dict[self.data_series_name]["x"]) - int(len(self.popup_creator.entry_list) / 3)):
                self.popup_creator.add_entry()
                self.popup_creator.update_scroll_region()
        for value_index in range(0, len(self.data_series_dict[self.data_series_name]["x"])): #every list is the same length (despite z which can be 0)
            self.popup_creator.entry_list[int(value_index * 3)].insert(0, #position
                                                                        self.data_series_dict[self.data_series_name]["x"][value_index]) #value
            self.popup_creator.entry_list[int(value_index * 3) + 1].insert(0,
                                                                            self.data_series_dict[self.data_series_name]["y"][value_index])
            if (self.data_series_dict[self.data_series_name]["z"]):
                self.popup_creator.entry_list[int(value_index * 3) + 2].insert(0,
                                                                                self.data_series_dict[self.data_series_name]["z"][value_index])

    def event_for_submit_modify_button(self, data_series_combobox):
        if (self.data_series_name != self.popup_creator.name_entry.get()):
            old_data_series_name = self.data_series_name
            if (self.check_name()):
                self.data_series_dict[self.data_series_name] = self.data_series_dict.pop(old_data_series_name)
                self.check_format_and_rewrite_to_dict(data_series_combobox)
            else:
                self.popup_creator.excel_sheet_popup.lift()
        else:
            self.check_format_and_rewrite_to_dict(data_series_combobox)

    def event_for_remove_plot_button(self, canvas, data_series_combobox, plot):
        if (not data_series_combobox.get()):
            self.popup_creator.messagebox_popup("Choose data series.")
            return
        if (not self.data_series_dict[data_series_combobox.get()]["artist"]):
            self.popup_creator.messagebox_popup(
                "Data series \"{0}\" not plotted, so cannot be removed".format(data_series_combobox.get()))
            return
        self.clear_series_properties(self.data_series_dict[data_series_combobox.get()])
        self.update_legend(plot)
        canvas.show()
        data_series_combobox.event_generate("<<ComboboxSelected>>")

    def event_for_plot_button(self, data_series_name, plot, canvas, chart_type, plot_name):
        self.data_series_name = data_series_name
        if (not self.data_series_name):
            self.popup_creator.messagebox_popup("Choose data series.")
            return
        if (self.data_series_dict[self.data_series_name]["artist"]):
            self.popup_creator.messagebox_popup(
                "Data series \"{0}\" already plotted".format(self.data_series_name))
            return
        if (not chart_type.get()):
            self.popup_creator.messagebox_popup(
                "Choose plot type.".format(self.data_series_name))
            return
        self.data_series_dict[self.data_series_name]["chart_type"] = chart_type.get()
        self.data_series_dict[self.data_series_name]["plot_name"] = plot_name
        self.draw_plot(plot)
        canvas.show()

    def draw_plot(self, plot):
        if (self.data_series_dict[self.data_series_name]["chart_type"] == "line"):
            if (not self.data_series_dict[self.data_series_name]["artist"]):
                self.data_series_dict[self.data_series_name]["artist"], = plot.plot(self.data_series_dict[self.data_series_name]["x"],
                                                                                    self.data_series_dict[self.data_series_name]["y"],
                                                                                    color=self.color,
                                                                                    picker=True,
                                                                                    label=self.data_series_dict[self.data_series_name]["plot_name"])
            else:
                plot.plot(self.data_series_dict[self.data_series_name]["x"], self.data_series_dict[self.data_series_name]["y"],
                          color=self.data_series_dict[self.data_series_name]["color"],
                          label=self.data_series_dict[self.data_series_name]["plot_name"])
                return
        elif (self.data_series_dict[self.data_series_name]["chart_type"] == "bar"):
            if (not self.data_series_dict[self.data_series_name]["artist"]):
                self.data_series_dict[self.data_series_name]["artist"] = plot.bar(self.data_series_dict[self.data_series_name]["x"],
                                                                                  self.data_series_dict[self.data_series_name]["y"],
                                                                                  color=self.color,
                                                                                  picker=True,
                                                                                  label=self.data_series_dict[self.data_series_name]["plot_name"])
            else:
                plot.bar(self.data_series_dict[self.data_series_name]["x"], self.data_series_dict[self.data_series_name]["y"],
                         color=self.data_series_dict[self.data_series_name]["color"],
                         label=self.data_series_dict[self.data_series_name]["plot_name"])
                return
        elif (self.data_series_dict[self.data_series_name]["chart_type"] == "point"):
            if (not self.data_series_dict[self.data_series_name]["artist"]):
                self.data_series_dict[self.data_series_name]["artist"] = plot.scatter(self.data_series_dict[self.data_series_name]["x"],
                                                                                      self.data_series_dict[self.data_series_name]["y"],
                                                                                      color=self.color,
                                                                                      picker=True,
                                                                                      label=self.data_series_dict[self.data_series_name]["plot_name"])
            else:
                plot.scatter(self.data_series_dict[self.data_series_name]["x"], self.data_series_dict[self.data_series_name]["y"],
                             color=self.data_series_dict[self.data_series_name]["color"],
                             label=self.data_series_dict[self.data_series_name]["plot_name"])
                return
        self.data_series_dict[self.data_series_name]["color"] = self.color
        self.update_legend(plot)

    def event_for_open_in_a_new_window_button(self):
        self.popup_creator.popup_for_plot(lambda: self.event_for_close_popup_button(self.popup_creator.plot_popup))
        for dict_name in self.data_series_dict.keys():
            if (self.data_series_dict[dict_name]["artist"]):
                self.data_series_name = dict_name
                self.draw_plot(self.popup_creator.plot)
                self.update_legend(self.popup_creator.plot)
        self.popup_creator.plot_popup.mainloop()

    def event_for_auto_scale_button(self, plot, canvas):
        plot.relim()
        plot.autoscale()
        canvas.show()

    def event_for_clear_button(self, canvas, plot):
        for dict in self.data_series_dict.values():
            if (dict["artist"]):
                self.clear_series_properties(dict)
        self.update_legend(plot)
        canvas.show()

    def event_for_radiobutton(self, chart_type, data_series_name, plot, canvas):
        # changes the drawn plot to the new type
        if (data_series_name and self.data_series_dict[data_series_name]["artist"]):
            if (chart_type != self.data_series_dict[data_series_name]["chart_type"]):
                self.data_series_dict[data_series_name]["chart_type"] = chart_type.get()
                self.data_series_dict[data_series_name]["artist"].remove()
                self.data_series_dict[data_series_name]["artist"] = None
                self.data_series_name = data_series_name
                self.draw_plot(plot)
                canvas.show()

    def name_entry_callback(self, data_series_name, plot_name, canvas, plot):
        if (data_series_name and self.data_series_dict[data_series_name]["artist"] and
            self.data_series_dict[data_series_name]["plot_name"] != plot_name):
            self.data_series_dict[data_series_name]["plot_name"] = plot_name
            self.update_legend(plot)
            canvas.show()

    def update_legend(self, plot):
        artist_list = []
        label_list = []
        for dict in self.data_series_dict.values():
            if (dict["artist"]):
                artist_list.append(dict["artist"])
                label_list.append(dict["plot_name"])
        if (artist_list):
            plot.legend(artist_list, label_list)
            #plot.get_legend().draggable()
            return
        if (plot.get_legend()):
            plot.get_legend().set_visible(False)

    def click_artist_callback(self, event):
        print(event.artist)

    def event_for_chart_configuration(self, plot, canvas):
        self.popup_creator.popup_for_chart_configuration(
            lambda: self.event_for_close_popup_button(self.popup_creator.chart_configuration_popup),
            lambda: self.event_for_submit_config_button(plot, canvas),
            lambda: self.event_for_apply_config_button(plot, canvas)
        )

    #remember about ticks
    def clear_series_properties(self, properties_dict):
        properties_dict["artist"].remove()
        properties_dict["artist"] = None
        properties_dict["chart_type"] = ""
        properties_dict["color"] = ""
        properties_dict["plot_name"] = ""

    def event_for_apply_config_button(self, plot, canvas):
        self.update_values_of_properties_dict(self.popup_creator.axes_frame.winfo_children(), axes_properties_dict,
                                              axes_properties_UI_dict, axes_properties_mapping_dict)
        self.update_values_of_properties_dict(self.popup_creator.grid_frame.winfo_children(), grid_properties_dict,
                                              grid_properties_UI_dict, gird_properties_mapping_dict)
        self.update_values_of_properties_dict(self.popup_creator.ticks_frame.winfo_children(), ticks_properties_dict,
                                              ticks_properties_UI_dict, ticks_properties_mapping_dict)
        mat_art.setp(plot, **axes_properties_dict)
        plot.grid(**grid_properties_dict)
        plot.tick_params(**ticks_properties_dict)
        canvas.show()

    def event_for_submit_config_button(self, plot, canvas):
        self.event_for_apply_config_button(plot, canvas)
        self.event_for_close_popup_button(self.popup_creator.chart_configuration_popup)

    def update_values_of_properties_dict(self, frame_elements, properties_dict, GUI_dict, mapping_dict):
        for index in range(0, len(frame_elements) - 1, 2):
            label_text = frame_elements[index].cget("text")[:-1]
            if (type(frame_elements[index + 1]) == tk.ttk.Combobox):
                for key, value in GUI_dict[label_text].items():
                    if (value == frame_elements[index + 1].get()):
                        break
            else:
                key = frame_elements[index + 1].get()
                GUI_dict[label_text] = key
            properties_dict[mapping_dict[label_text]] = key
