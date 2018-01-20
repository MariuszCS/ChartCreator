import Parser
import PopupCreator
import PropertiesDictionaries
import GUICreator

import os

import matplotlib.artist as mat_art
import matplotlib.patches
from matplotlib import ticker

class EventHandler(object):
    def __init__(self):
        self.parser = Parser.Parser()
        self.popup_creator = PopupCreator.PopupCreator()
        self.data_series_name = ""
        self.data_series_dict = {}
        self.proper_name = True
        self.color = "#000000"
        self.chosen_plot = ""
        self.plot_is_chosen = False

    def event_for_load_button(self, data_series_combobox):
        path_to_file = self.popup_creator.popup_for_openfile()
        if (path_to_file):
            temp_series_properties_dict = self.parser.parse_file(path_to_file)
            if (temp_series_properties_dict):
                file_name = os.path.split(path_to_file)[1].split(".")[0]
                self.popup_creator.popup_for_provide_name(file_name, 
                                                          lambda: self.event_for_submit_name_button(temp_series_properties_dict, 
                                                                                                    data_series_combobox),
                                                          lambda: self.event_for_close_popup_button(
                                                          self.popup_creator.provide_name_popup))

    def rewrite_values_to_data_series_dict(self, temp_series_properties_dict):
        if (not self.data_series_name in self.data_series_dict):
            self.data_series_dict[self.data_series_name] = PropertiesDictionaries.create_series_properties_dict()
        else:
            self.data_series_dict[self.data_series_name]["x"] = []
            self.data_series_dict[self.data_series_name]["y"] = []
        self.data_series_dict[self.data_series_name]["x"] = [
            float(element) for element in temp_series_properties_dict["x"]]
        self.data_series_dict[self.data_series_name]["y"] = [
            float(element) for element in temp_series_properties_dict["y"]]

    def event_for_submit_name_button(self, temp_series_properties_dict, data_series_combobox):
        if (self.check_name()):
            self.rewrite_values_to_data_series_dict(
                temp_series_properties_dict)
            self.event_for_update_data_series_combobox(data_series_combobox)
            data_series_combobox.current(
                len(data_series_combobox["values"]) - 1)
            self.event_for_close_popup_button(
                self.popup_creator.provide_name_popup)
            data_series_combobox.event_generate("<<ComboboxSelected>>")
        else:
            self.popup_creator.provide_name_popup.lift()

    def check_name(self):
        # checks if the name is not empty or if it already exists
        provided_name = self.popup_creator.name_entry.get()
        if (not provided_name):
            self.popup_creator.messagebox_popup("Name must not be empty.")
            return False
        if (provided_name in self.data_series_dict):
            self.popup_creator.messagebox_popup(
                "Name: \"{0}\" already exists!".format(provided_name))
            return False
        self.data_series_name = provided_name
        return True

    def event_for_close_popup_button(self, popup):
        if (self.popup_creator.excel_sheet_popup == popup):
            # clear entries list if the popup was excel_sheet_popup
            self.popup_creator.entry_list = []
        popup.grab_release()  # release focus
        popup.quit()  # escape the mainloop()
        popup.destroy()  # destroy the popup

    def event_for_update_data_series_combobox(self, data_series_combobox):
        # command run every time user clicks on the arrow of the combobox
        data_series_combobox.config(
            values=[data_series_name for data_series_name in self.data_series_dict.keys()])

    def event_for_color_chooser_button(self, chosen_color_label, chosen_color_preview_label, canvas, plot):
        new_color = colorchooser.askcolor(initialcolor="#000000")[1]
        if (new_color):
            # if the color has been chosen and is different than previous one
            self.color = new_color
            self.update_color_labels(
                chosen_color_label, chosen_color_preview_label, self.color)
            # if the data series is plotted, change its color
            if (self.data_series_dict and self.data_series_dict[self.data_series_name]["artist"]):
                if (self.data_series_dict[self.data_series_name]["chart_type"] == "Stem plot"):
                    mat_art.setp(
                        self.data_series_dict[self.data_series_name]["artist"][0], markerfacecolor=self.color, markeredgecolor=self.color)
                    mat_art.setp(
                        self.data_series_dict[self.data_series_name]["artist"][1], color=self.color)
                else:
                    mat_art.setp(
                        self.data_series_dict[self.data_series_name]["artist"], color=self.color)
                self.data_series_dict[self.data_series_name]["color"] = self.color
                self.update_legend(plot)
                canvas.show()

    def data_series_combobox_callback(self, data_series_name, chosen_color_label, chosen_color_preview_label, 
                                     name_entry, chosen_type_label):
        self.data_series_name = data_series_name
        if (self.data_series_dict.keys()):
            if (self.data_series_dict[self.data_series_name]["artist"]):
                # update color in hex and preview in the color label to the color of the plot of this data series
                self.color = self.data_series_dict[self.data_series_name]["color"]
                self.update_color_labels(
                    chosen_color_label, chosen_color_preview_label, self.color)
            else:
                # update color in hex and preview in the color label to the default color (black)
                self.color = "#000000"
                self.update_color_labels(
                    chosen_color_label, chosen_color_preview_label, self.color)
            # set radiobutton to the chart_type of the data series (if plotted data series is line, line radiobutton will be set,
            # if the data series is not plotted, all radio buttons will be cleared etc.)
            GUICreator.ChartCreator.chart_type.set(value=self.data_series_dict[self.data_series_name]["chart_type"])
            chosen_type_label.config(text="Chosen type: " + GUICreator.ChartCreator.chart_type.get())
            # remove anything that is present in name_entry, but only in case if it is different than the plot_name of current data series,
            # and set it to the plot_name of current data series
            if (name_entry.get() != self.data_series_dict[self.data_series_name]["plot_name"]):
                name_entry.delete(0, len(name_entry.get()))
                name_entry.insert(
                    0, self.data_series_dict[self.data_series_name]["plot_name"])
        else:
            name_entry.delete(0, len(name_entry.get()))
            GUICreator.ChartCreator.chart_type.set("")
            self.update_color_labels(
                chosen_color_label, chosen_color_preview_label, "")

    def update_color_labels(self, chosen_color_label, chosen_color_preview_label, color):
        # update text and color in preview label
        chosen_color_label.config(text="Chosen color (hex): {0}".format(color))
        chosen_color_preview_label.config(background=color)

    def event_for_delete_button(self, data_series_combobox, canvas, plot):
        if (self.data_series_name):
            if (self.data_series_dict[self.data_series_name]["artist"]):
                self.remove_artist(self.data_series_dict[self.data_series_name])
                self.data_series_dict[self.data_series_name]["artist_properties_dict"] = None
                self.update_legend(plot)
                canvas.show()
                if (self.data_series_name == self.chosen_plot):
                    self.chosen_plot = ""
                    self.plot_is_chosen = False
                    self.update_chosen_plot_label(self.chosen_plot)
            del self.data_series_dict[self.data_series_name]
            if (data_series_combobox.current()):
                data_series_combobox.current(
                    data_series_combobox.current() - 1)
            elif (not data_series_combobox.current() and len(data_series_combobox["values"]) > 1):
                data_series_combobox.current(
                    data_series_combobox.current() + 1)
            else:
                data_series_combobox.set("") 
            self.event_for_update_data_series_combobox(data_series_combobox)
            data_series_combobox.event_generate("<<ComboboxSelected>>")
        else:
            self.popup_creator.messagebox_popup("No data series selected.")

    def event_for_insert_button(self, data_series_combobox):
        self.popup_creator.popup_for_excel_sheet(
            "Insert data series...",
            lambda: self.event_for_close_popup_button(
                self.popup_creator.excel_sheet_popup),
            lambda: self.event_for_submit_insert_button(data_series_combobox, "Insert data series..."),
            lambda: self.event_for_add_row_button())
        self.popup_creator.excel_sheet_popup.mainloop()

    def event_for_submit_insert_button(self, data_series_combobox, window_title):
        if (self.check_name()):
            self.check_format_and_rewrite_to_dict(data_series_combobox, window_title)
        else:
            self.popup_creator.excel_sheet_popup.lift()

    def check_format_and_rewrite_to_dict(self, data_series_combobox, window_title):
        temp_series_properties_dict = PropertiesDictionaries.create_series_properties_dict()
        for entry_number in range(0, len(self.popup_creator.entry_list), 2):
            x_entry_content = self.popup_creator.entry_list[entry_number].get()
            y_entry_content = self.popup_creator.entry_list[entry_number + 1].get()
            if (not x_entry_content and not y_entry_content):
                pass
            else:
                temp_series_properties_dict["x"].append(x_entry_content)
                temp_series_properties_dict["y"].append(y_entry_content)
        if (self.parser.check_inserted_data_format(temp_series_properties_dict)):
            self.rewrite_values_to_data_series_dict(
                temp_series_properties_dict)
            self.event_for_update_data_series_combobox(data_series_combobox)
            self.event_for_close_popup_button(
                self.popup_creator.excel_sheet_popup)
            if (window_title == "Insert data series..."):
                data_series_combobox.current(
                    len(data_series_combobox["values"]) - 1)
                data_series_combobox.event_generate("<<ComboboxSelected>>")
        else:
            del temp_series_properties_dict
            self.popup_creator.messagebox_popup(
                "Please check if the entered fields are well aligned.")
            self.popup_creator.excel_sheet_popup.lift()

    def event_for_add_row_button(self):
        self.popup_creator.add_entry()
        self.popup_creator.update_scroll_region()

    def event_for_modify_button(self, data_series_combobox, canvas, plot):
        if (self.data_series_name):
            self.popup_creator.popup_for_excel_sheet(
                "Modify data series...",
                lambda: self.event_for_close_popup_button(
                    self.popup_creator.excel_sheet_popup),
                lambda: self.event_for_submit_modify_button(
                    data_series_combobox, "Modify data series...", canvas, plot),
                lambda: self.event_for_add_row_button())
            self.fill_excel_sheet_popup(data_series_combobox)
            # needs to be here so self.fill_excel_sheet_popup(data_series_combobox)
            self.popup_creator.excel_sheet_popup.mainloop()
            # will be executed before the popup will show
        else:
            self.popup_creator.messagebox_popup("No data series selected.")
            return

    def fill_excel_sheet_popup(self, data_series_combobox):
        self.popup_creator.name_entry.insert(0, self.data_series_name)
        if (len(self.data_series_dict[self.data_series_name]["x"]) > int(len(self.popup_creator.entry_list) / 2)):
            for _ in range(0, len(self.data_series_dict[self.data_series_name]["x"]) - int(len(self.popup_creator.entry_list) / 2)):
                self.popup_creator.add_entry()
                self.popup_creator.update_scroll_region()
        # every list is the same length
        for value_index in range(0, len(self.data_series_dict[self.data_series_name]["x"])):
            self.popup_creator.entry_list[int(value_index * 2)].insert(0,  # position
                                                                       self.data_series_dict[self.data_series_name]["x"][value_index])  # value
            self.popup_creator.entry_list[int(value_index * 2) + 1].insert(0,
                                                                           self.data_series_dict[self.data_series_name]["y"][value_index])

    def event_for_submit_modify_button(self, data_series_combobox, window_title, canvas, plot):
        if (self.data_series_name != self.popup_creator.name_entry.get()):
            old_data_series_name = self.data_series_name
            if (self.check_name()):
                self.data_series_dict[self.data_series_name] = self.data_series_dict.pop(
                    old_data_series_name)
                self.check_format_and_rewrite_to_dict(data_series_combobox, window_title)
            else:
                self.popup_creator.excel_sheet_popup.lift()
                return
        else:
            self.check_format_and_rewrite_to_dict(data_series_combobox, window_title)
        if (self.data_series_dict[self.data_series_name]["artist"]):
            self.remove_artist(self.data_series_dict[self.data_series_name])
            self.data_series_dict[self.data_series_name]["artist_properties_dict"] = None
            self.draw_plot(plot)
            canvas.show()

    def event_for_remove_plot_button(self, canvas, data_series_combobox, plot):
        if (not self.data_series_name):
            self.popup_creator.messagebox_popup("No data series selected.")
            return
        if (not self.data_series_dict[self.data_series_name]["artist"]):
            self.popup_creator.messagebox_popup(
                "Data series \"{0}\" not plotted, so cannot be removed.".format(self.data_series_name))
            return
        if (self.chosen_plot == self.data_series_name):
            self.chosen_plot = ""
            self.plot_is_chosen = False
            self.update_chosen_plot_label(self.chosen_plot)
        self.clear_series_properties(
            self.data_series_dict[self.data_series_name])
        self.update_legend(plot)
        canvas.show()
        data_series_combobox.event_generate("<<ComboboxSelected>>")

    def event_for_plot_button(self, plot, canvas, plot_name):
        if (not self.data_series_name):
            self.popup_creator.messagebox_popup("No data series selected.")
            return
        if (self.data_series_dict[self.data_series_name]["artist"]):
            self.popup_creator.messagebox_popup(
                "Data series \"{0}\" already plotted.".format(self.data_series_name))
            return
        if (not GUICreator.ChartCreator.chart_type.get()):
            self.popup_creator.messagebox_popup(
                "No plot type selected.")
            return
        self.data_series_dict[self.data_series_name]["chart_type"] = GUICreator.ChartCreator.chart_type.get()
        self.data_series_dict[self.data_series_name]["plot_name"] = plot_name
        self.data_series_dict[self.data_series_name]["color"] = self.color
        self.draw_plot(plot)
        # If someone passes wrong name in the legend for example: ${_y_t}$, this is double subscript written in a wrong way,
        # so the built in exception will be raised
        try:
            canvas.show()
        except ValueError:
            self.data_series_dict[self.data_series_name]["plot_name"] = ""
            self.update_legend(plot)
            canvas.show()
            self.popup_creator.messagebox_popup("Wrong mathtext syntax. Please check the matplotlib docs for more information "
                                                "about mathtext used in matplotlib.")
        
    def draw_plot(self, plot):
        if (self.data_series_dict[self.data_series_name]["chart_type"] == "Line"):
            if (not self.data_series_dict[self.data_series_name]["artist"]):
                self.data_series_dict[self.data_series_name]["artist"], = plot.plot(self.data_series_dict[self.data_series_name]["x"],
                                                                                    self.data_series_dict[self.data_series_name]["y"],
                                                                                    color=self.data_series_dict[self.data_series_name]["color"],
                                                                                    picker=True)
                if (not self.data_series_dict[self.data_series_name]["artist_properties_dict"]):
                    self.data_series_dict[self.data_series_name]["artist_properties_dict"] = PropertiesDictionaries.create_line_properties_dict()
            else:
                plot.plot(self.data_series_dict[self.data_series_name]["x"], self.data_series_dict[self.data_series_name]["y"],
                          color=self.data_series_dict[self.data_series_name]["color"])
                return
        elif (self.data_series_dict[self.data_series_name]["chart_type"] == "Bars"):
            if (not self.data_series_dict[self.data_series_name]["artist"]):
                self.data_series_dict[self.data_series_name]["artist"] = plot.bar(self.data_series_dict[self.data_series_name]["x"],
                                                                                  self.data_series_dict[self.data_series_name]["y"],
                                                                                  color=self.data_series_dict[self.data_series_name]["color"],
                                                                                  picker=True,
                                                                                  width=2)
                if (not self.data_series_dict[self.data_series_name]["artist_properties_dict"]):
                    self.data_series_dict[self.data_series_name]["artist_properties_dict"] = PropertiesDictionaries.create_bar_properties_dict()
            else:
                plot.bar(self.data_series_dict[self.data_series_name]["x"], self.data_series_dict[self.data_series_name]["y"],
                         color=self.data_series_dict[self.data_series_name]["color"],
                         width=5)
                return
        elif (self.data_series_dict[self.data_series_name]["chart_type"] == "Points"):
            if (not self.data_series_dict[self.data_series_name]["artist"]):
                self.data_series_dict[self.data_series_name]["artist"], = plot.plot(self.data_series_dict[self.data_series_name]["x"],
                                                                                    self.data_series_dict[
                                                                                    self.data_series_name]["y"],
                                                                                    color=self.data_series_dict[self.data_series_name]["color"],
                                                                                    picker=True,
                                                                                    marker=".",
                                                                                    markersize=6,
                                                                                    linewidth=0)
                if (not self.data_series_dict[self.data_series_name]["artist_properties_dict"]):
                    self.data_series_dict[self.data_series_name]["artist_properties_dict"] = PropertiesDictionaries.create_point_properties_dict()                                                                         
            else:
                plot.scatter(self.data_series_dict[self.data_series_name]["x"], self.data_series_dict[self.data_series_name]["y"],
                             color=self.data_series_dict[self.data_series_name]["color"],
                             s=1)
                return
        elif (self.data_series_dict[self.data_series_name]["chart_type"] == "Horizontal bar"):
            if (not self.data_series_dict[self.data_series_name]["artist"]):
                self.data_series_dict[self.data_series_name]["artist"] = plot.barh(self.data_series_dict[self.data_series_name]["x"],
                                                                                   self.data_series_dict[self.data_series_name]["y"],
                                                                                   color=self.data_series_dict[self.data_series_name]["color"],
                                                                                   picker=True,
                                                                                   height=2)
                if (not self.data_series_dict[self.data_series_name]["artist_properties_dict"]):
                    self.data_series_dict[self.data_series_name]["artist_properties_dict"] = PropertiesDictionaries.create_horizontal_bar_properties_dict()
            else:
                plot.barh(self.data_series_dict[self.data_series_name]["x"], self.data_series_dict[self.data_series_name]["y"],
                         color=self.data_series_dict[self.data_series_name]["color"],
                         height=5)
                return
        elif (self.data_series_dict[self.data_series_name]["chart_type"] == "Error bar"):
            if (not self.data_series_dict[self.data_series_name]["artist"]):
                self.data_series_dict[self.data_series_name]["artist"] = plot.errorbar(self.data_series_dict[self.data_series_name]["x"],
                                                                                   self.data_series_dict[self.data_series_name]["y"],
                                                                                   color=self.data_series_dict[self.data_series_name]["color"],
                                                                                   picker=True,
                                                                                   yerr=0.2,
                                                                                   xerr=0.2,
                                                                                   fmt="none")
                mat_art.setp(self.data_series_dict[self.data_series_name]["artist"][2][0],picker = True)
                mat_art.setp(self.data_series_dict[self.data_series_name]["artist"][2][1],picker = True)
                if (not self.data_series_dict[self.data_series_name]["artist_properties_dict"]):
                    self.data_series_dict[self.data_series_name]["artist_properties_dict"] = PropertiesDictionaries.create_error_bar_properties_dict()                                                                                            
            else:
                plot.errorbar(self.data_series_dict[self.data_series_name]["x"], self.data_series_dict[self.data_series_name]["y"],
                        color=self.data_series_dict[self.data_series_name]["color"],
                        yerr=1,
                        xerr=1,
                        fmt="none")
                return
        elif (self.data_series_dict[self.data_series_name]["chart_type"] == "Histogram"):
            if (not self.data_series_dict[self.data_series_name]["artist"]):
                _, _, self.data_series_dict[self.data_series_name]["artist"] = plot.hist(self.data_series_dict[self.data_series_name]["x"],
                                                                                   color=self.data_series_dict[self.data_series_name]["color"],
                                                                                   picker=True)        
                if (not self.data_series_dict[self.data_series_name]["artist_properties_dict"]):                                                          
                    self.data_series_dict[self.data_series_name]["artist_properties_dict"] = PropertiesDictionaries.create_histogram_properties_dict()
            else:
                plot.hist(self.data_series_dict[self.data_series_name]["x"],
                        color=self.data_series_dict[self.data_series_name]["color"],
                        edgecolor="red")
                return
        elif (self.data_series_dict[self.data_series_name]["chart_type"] == "Stack plot"):
            if (not self.data_series_dict[self.data_series_name]["artist"]):
                self.data_series_dict[self.data_series_name]["artist"] = plot.stackplot(self.data_series_dict[self.data_series_name]["x"],
                                                                                   self.data_series_dict[self.data_series_name]["y"],
                                                                                   color=self.data_series_dict[self.data_series_name]["color"],
                                                                                   picker=True).pop()
                if (not self.data_series_dict[self.data_series_name]["artist_properties_dict"]):
                    self.data_series_dict[self.data_series_name]["artist_properties_dict"] = PropertiesDictionaries.create_stack_properties_dict()
            else:
                plot.stackplot(self.data_series_dict[self.data_series_name]["x"],
                        self.data_series_dict[self.data_series_name]["y"],
                        color=self.data_series_dict[self.data_series_name]["color"])
                return
        elif (self.data_series_dict[self.data_series_name]["chart_type"] == "Stem plot"):
            if (not self.data_series_dict[self.data_series_name]["artist"]):
                self.data_series_dict[self.data_series_name]["artist"] = plot.stem(self.data_series_dict[self.data_series_name]["x"],
                                                                                   self.data_series_dict[self.data_series_name]["y"],
                                                                                   color=self.data_series_dict[self.data_series_name]["color"],
                                                                                   picker=True,
                                                                                   basefmt="none")
                if (not self.data_series_dict[self.data_series_name]["artist_properties_dict"]):
                    self.data_series_dict[self.data_series_name]["artist_properties_dict"] = PropertiesDictionaries.create_line_properties_dict()
                    self.data_series_dict[self.data_series_name]["artist_properties_dict"]["marker"] = "."
                    mat_art.setp(self.data_series_dict[self.data_series_name]["artist"][0],
                            **dict(list(self.data_series_dict[self.data_series_name]["artist_properties_dict"].items())[0:1]),
                            **dict(list(self.data_series_dict[self.data_series_name]["artist_properties_dict"].items())[4:9]),
                            **dict(list(self.data_series_dict[self.data_series_name]["artist_properties_dict"].items())[11:]))
                    mat_art.setp(self.data_series_dict[self.data_series_name]["artist"][1], 
                            **dict(list(self.data_series_dict[self.data_series_name]["artist_properties_dict"].items())[0:4]),
                            **dict(list(self.data_series_dict[self.data_series_name]["artist_properties_dict"].items())[9:11]))
                    mat_art.setp(self.data_series_dict[self.data_series_name]["artist"][0], 
                                markerfacecolor=self.data_series_dict[self.data_series_name]["color"],
                                markeredgecolor=self.data_series_dict[self.data_series_name]["color"])
                    mat_art.setp(self.data_series_dict[self.data_series_name]["artist"][1], 
                                color=self.data_series_dict[self.data_series_name]["color"])
                mat_art.setp(self.data_series_dict[self.data_series_name]["artist"][0],picker = True)
                mat_art.setp(self.data_series_dict[self.data_series_name]["artist"][1],picker = True)                                                                   
            else:
                plot.stem(self.data_series_dict[self.data_series_name]["x"],
                        self.data_series_dict[self.data_series_name]["y"],
                        color=self.data_series_dict[self.data_series_name]["color"])
                return
        elif (self.data_series_dict[self.data_series_name]["chart_type"] == "Step plot"):
            if (not self.data_series_dict[self.data_series_name]["artist"]):
                self.data_series_dict[self.data_series_name]["artist"] = plot.step(self.data_series_dict[self.data_series_name]["x"],
                                                                                   self.data_series_dict[self.data_series_name]["y"],
                                                                                   color=self.data_series_dict[self.data_series_name]["color"],
                                                                                   picker=True,
                                                                                   linewidth=1).pop()
                if (not self.data_series_dict[self.data_series_name]["artist_properties_dict"]):
                    self.data_series_dict[self.data_series_name]["artist_properties_dict"] = PropertiesDictionaries.create_step_properties_dict()
            else:
                plot.step(self.data_series_dict[self.data_series_name]["x"],
                        self.data_series_dict[self.data_series_name]["y"],
                        color=self.data_series_dict[self.data_series_name]["color"])
                return
        self.update_legend(plot)

    def event_for_open_in_a_new_window_button(self):
        data_series_name = self.data_series_name
        self.popup_creator.popup_for_plot(
            lambda: self.event_for_close_popup_button(self.popup_creator.plot_popup))
        for dict_name in self.data_series_dict.keys():
            if (self.data_series_dict[dict_name]["artist"]):
                self.data_series_name = dict_name
                self.draw_plot(self.popup_creator.plot)
                self.update_legend(self.popup_creator.plot)
        self.data_series_name = data_series_name
        self.popup_creator.plot_popup.mainloop()

    def event_for_auto_scale_button(self, plot, canvas):
        plot.relim()
        plot.autoscale()
        plot.autoscale_view()
        canvas.show()

    def event_for_clear_button(self, canvas, plot, data_series_combobox):
        for dict in self.data_series_dict.values():
            if (dict["artist"]):
                self.clear_series_properties(dict)
        self.update_legend(plot)
        canvas.show()
        data_series_combobox.event_generate("<<ComboboxSelected>>")
        self.chosen_plot = ""
        self.plot_is_chosen = False
        self.update_chosen_plot_label(self.chosen_plot)
        self.event_for_auto_scale_button(plot, canvas)

    def event_for_radiobutton(self, plot, canvas, chosen_type_label):
        # changes the drawn plot to the new type
        self.handle_chart_type_change(plot, canvas, chosen_type_label)

    def name_entry_callback(self, plot_name, canvas, plot):
        if (self.data_series_name and self.data_series_dict[self.data_series_name]["artist"] and
                self.data_series_dict[self.data_series_name]["plot_name"] != plot_name):
            old_plot_name = self.data_series_dict[self.data_series_name]["plot_name"]
            self.data_series_dict[self.data_series_name]["plot_name"] = plot_name
            self.update_legend(plot)
            # If someone passes wrong name in the legend for example: ${_y_t}$, this is double subscript written in a wrong way,
            # so the built in exception will be raised
            try:
                canvas.show()
            except ValueError:
                self.data_series_dict[self.data_series_name]["plot_name"] = old_plot_name
                self.update_legend(plot)
                canvas.show()
                self.popup_creator.messagebox_popup("Wrong mathtext syntax. Please check the matplotlib docs for more information "
                                                    "about mathtext used in matplotlib.")
                return
            if (self.data_series_name == self.chosen_plot):
                self.update_chosen_plot_label(self.data_series_dict[self.data_series_name]["plot_name"])
            
    def update_legend(self, plot):
        artist_list = []
        label_list = []
        for dictionary in self.data_series_dict.values():
            if (dictionary["artist"]):
                if (type(dictionary["artist"]) != matplotlib.cbook.silent_list):
                        artist_list.append(dictionary["artist"])
                else:
                    artist_list.append(matplotlib.patches.Patch(edgecolor=dictionary["artist"][0].get_edgecolor(), 
                                                                facecolor=dictionary["artist"][0].get_facecolor(),
                                                                hatch=dictionary["artist_properties_dict"]["hatch"],
                                                                fill=dictionary["artist_properties_dict"]["fill"],
                                                                alpha=dictionary["artist_properties_dict"]["alpha"]))
            
                label_list.append(dictionary["plot_name"])
        if (artist_list):
            plot.legend(artist_list, label_list, **dict(list(legend_properties_dict.items())[2:]))
            try:
                plot.get_legend().set(**legend_properties_dict)
            except AttributeError:
                pass
            plot.get_legend().draggable(state=legend_properties_dict["draggable"])
            return
        if (plot.get_legend()):
            plot.get_legend().set_visible(False)

    def click_artist_callback(self, event):
        self.plot_is_chosen = True
        for data_series_name, properties_dict in self.data_series_dict.items():
            if (data_series_name != self.chosen_plot):
                try:
                    if (properties_dict["artist"] == event.artist or event.artist in properties_dict["artist"] or event.artist in properties_dict["artist"].get_children()):
                        self.chosen_plot = data_series_name
                        self.update_chosen_plot_label(properties_dict["plot_name"])
                except TypeError:
                    pass
                
    def update_chosen_plot_label(self, plot_name):
        if (plot_name):
            if (len(plot_name) > 12):
                GUICreator.ChartCreator.chosen_plot_label.config(text="Chosen: " + plot_name[:12] + "...", font=Constants.MONOSPACED_FONT)
            else:
                GUICreator.ChartCreator.chosen_plot_label.config(text="Chosen: " + plot_name, font=Constants.MONOSPACED_FONT)
        elif (self.plot_is_chosen):
            GUICreator.ChartCreator.chosen_plot_label.config(text="Chosen: (Unnamed)", font=Constants.MONOSPACED_FONT)
        else:
            GUICreator.ChartCreator.chosen_plot_label.config(text="Chosen:", font=Constants.MONOSPACED_FONT)

    def event_for_chart_configuration(self, plot, canvas, tab_title):
        self.popup_creator.popup_for_chart_configuration(
            lambda: self.event_for_close_popup_button(
                self.popup_creator.chart_configuration_popup),
            lambda: self.event_for_submit_config_button(plot, canvas),
            lambda: self.event_for_apply_config_button(plot, canvas, False),
            tab_title
        )

    # remember about ticks
    def clear_series_properties(self, properties_dict):
        self.remove_artist(properties_dict)
        properties_dict["artist_properties_dict"] = None
        properties_dict["chart_type"] = ""
        properties_dict["color"] = ""
        properties_dict["plot_name"] = ""

    def remove_artist(self, properties_dict):
        # in case of list of artist we need to remove them one by one from the plot
        if (type(self.data_series_dict[self.data_series_name]["artist"]) == list):
            for artist in reversed(self.data_series_dict[self.data_series_name]["artist"][2]):
                artist.remove()
        elif (type(self.data_series_dict[self.data_series_name]["artist"]) == matplotlib.cbook.silent_list):
            for artist in reversed(self.data_series_dict[self.data_series_name]["artist"]):
                artist.remove()
        else:
            properties_dict["artist"].remove()
        properties_dict["artist"] = None

    def event_for_apply_config_button(self, plot, canvas, open_file):
        if (not open_file):
            self.update_values_of_properties_dict(self.popup_creator.axes_frame.winfo_children(), axes_properties_dict,
                                                axes_properties_UI_dict, axes_properties_mapping_dict)
            self.update_values_of_properties_dict(self.popup_creator.grid_frame.winfo_children(), grid_properties_dict,
                                                grid_properties_UI_dict, gird_properties_mapping_dict)
            self.update_values_of_properties_dict(self.popup_creator.ticks_frame.winfo_children(), ticks_properties_dict,
                                                ticks_properties_UI_dict, ticks_properties_mapping_dict)
            self.update_values_of_properties_dict(self.popup_creator.legend_frame.winfo_children(), legend_properties_dict,
                                                legend_properties_UI_dict, legend_properties_mapping_dict)
        mat_art.setp(plot, **axes_properties_dict)
        plot.grid(**grid_properties_dict)
        # there is no visible attribute for ticks, alternative are 2 attributes bottom, left. 
        # There is no point to put them into the GUI so it needs to
        # be changed into visibility in the GUI, and GUI dict needs to have as many attributes as prop dict
        # so there is visible att in the prop dict which needs to be omitted while passing to configuration function
        plot.tick_params(**dict(list(ticks_properties_dict.items())[:2]), **dict(list(ticks_properties_dict.items())[3:7]),
                        **dict(list(ticks_properties_dict.items())[8:]))
        self.handle_ticks_visibility(plot)
        self.update_legend(plot)
        canvas.show()

    def handle_ticks_visibility(self, plot):
        plot.tick_params(axis=ticks_properties_dict["axis"], which=ticks_properties_dict["which"],
                        bottom=ticks_properties_dict["visible"], left=ticks_properties_dict["visible"])
        if (ticks_properties_dict["axis"] == "x"):
            self.change_ticks_locator(plot.xaxis)
            self.change_ticks_formatter(plot.xaxis)
        elif (ticks_properties_dict["axis"] == "y"):
            self.change_ticks_locator(plot.yaxis)
            self.change_ticks_formatter(plot.yaxis)
        else:
            self.change_ticks_locator(plot.xaxis)
            self.change_ticks_locator(plot.yaxis)
            self.change_ticks_formatter(plot.xaxis)
            self.change_ticks_formatter(plot.yaxis)

    def change_ticks_locator(self, axis):
        if (ticks_properties_dict["which"] == "minor"):
            if (ticks_properties_dict["visible"]):
                axis.set_minor_locator(ticker.AutoMinorLocator(4))
            else:
                axis.set_minor_locator(ticker.NullLocator())
        elif (ticks_properties_dict["which"] == "major"):
            if (ticks_properties_dict["visible"]):
                axis.set_major_locator(ticker.AutoLocator())
            else:
                axis.set_major_locator(ticker.NullLocator())
        else:
            if (ticks_properties_dict["visible"]):
                axis.set_minor_locator(ticker.AutoMinorLocator(4))
                axis.set_major_locator(ticker.AutoLocator())
            else:
                axis.set_minor_locator(ticker.NullLocator())
                axis.set_major_locator(ticker.NullLocator())

    def change_ticks_formatter(self, axis):
        if (ticks_properties_dict["which"] == "minor"):
            if (ticks_properties_dict["label"]):
                axis.set_minor_formatter(ticker.ScalarFormatter())
            else:
                axis.set_minor_formatter(ticker.NullFormatter())
        elif (ticks_properties_dict["which"] == "major"):
            if (ticks_properties_dict["label"]):
                axis.set_major_formatter(ticker.ScalarFormatter())
            else:
                axis.set_major_formatter(ticker.NullFormatter())
        else:
            if (ticks_properties_dict["label"]):
                axis.set_minor_formatter(ticker.ScalarFormatter())
                axis.set_major_formatter(ticker.ScalarFormatter())
            else:
                axis.set_minor_formatter(ticker.NullFormatter())
                axis.set_major_formatter(ticker.NullFormatter())

    def event_for_submit_config_button(self, plot, canvas):
        self.event_for_apply_config_button(plot, canvas, False)
        self.event_for_close_popup_button(
            self.popup_creator.chart_configuration_popup)

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

    def event_for_more_plot_types_button(self, plot, canvas, chosen_type_label):
        self.popup_creator.popup_for_plot_types(lambda: self.event_for_close_popup_button(self.popup_creator.plot_types_popup),
                                                lambda: self.event_for_submit_plot_type_button(plot, canvas, chosen_type_label))

    def event_for_submit_plot_type_button(self, plot, canvas, chosen_type_label):
        if (self.popup_creator.plot_types_listbox.curselection()):
            GUICreator.ChartCreator.chart_type.set(self.popup_creator.plot_types_listbox.get(
                                                self.popup_creator.plot_types_listbox.curselection()[0])[1:])
            self.handle_chart_type_change(plot, canvas, chosen_type_label)
        self.event_for_close_popup_button(self.popup_creator.plot_types_popup)

    def handle_chart_type_change(self, plot, canvas, chosen_type_label):
        chosen_type_label.config(text="Chosen type: " + GUICreator.ChartCreator.chart_type.get())
        if (self.data_series_name and self.data_series_dict[self.data_series_name]["artist"]):
            if (GUICreator.ChartCreator.chart_type.get() != self.data_series_dict[self.data_series_name]["chart_type"]):
                self.data_series_dict[self.data_series_name]["chart_type"] = GUICreator.ChartCreator.chart_type.get()
                self.remove_artist(self.data_series_dict[self.data_series_name])
                self.data_series_dict[self.data_series_name]["artist_properties_dict"] = None
                self.draw_plot(plot)
                canvas.show()

    def event_for_apply_plot_config_button(self, plot, canvas, file_opened):
        UI_dict, mapping_dict = choose_proper_dicts(self.data_series_dict[self.chosen_plot]["chart_type"])
        if (not file_opened):
            self.update_values_of_properties_dict(self.popup_creator.plot_options_frame.winfo_children(),
                                                self.data_series_dict[self.chosen_plot]["artist_properties_dict"],
                                                UI_dict, mapping_dict)
        if (self.data_series_dict[self.chosen_plot]["chart_type"] == "Error bar"):
            self.remove_artist(self.data_series_dict[self.chosen_plot])
            self.data_series_dict[self.chosen_plot]["artist"] = plot.errorbar(self.data_series_dict[self.chosen_plot]["x"],
                                                                            self.data_series_dict[self.chosen_plot]["y"],
                                                                            fmt="none",
                                                                            **self.data_series_dict[self.chosen_plot]["artist_properties_dict"])
        elif (self.data_series_dict[self.chosen_plot]["chart_type"] == "Stem plot"):
            mat_art.setp(self.data_series_dict[self.chosen_plot]["artist"][0],
                        **dict(list(self.data_series_dict[self.chosen_plot]["artist_properties_dict"].items())[0:1]),
                        **dict(list(self.data_series_dict[self.chosen_plot]["artist_properties_dict"].items())[4:9]),
                        **dict(list(self.data_series_dict[self.chosen_plot]["artist_properties_dict"].items())[11:]))
            mat_art.setp(self.data_series_dict[self.chosen_plot]["artist"][1], 
                        **dict(list(self.data_series_dict[self.chosen_plot]["artist_properties_dict"].items())[0:4]),
                        **dict(list(self.data_series_dict[self.chosen_plot]["artist_properties_dict"].items())[9:11]))
        elif (self.data_series_dict[self.chosen_plot]["chart_type"] == "Step plot"):
            self.remove_artist(self.data_series_dict[self.chosen_plot])
            self.data_series_dict[self.chosen_plot]["artist"] = plot.step(self.data_series_dict[self.chosen_plot]["x"],
                                                                    self.data_series_dict[self.chosen_plot]["y"],
                                                                    where=self.data_series_dict[self.chosen_plot]["artist_properties_dict"]["where"],
                                                                    **dict(list(self.data_series_dict[self.chosen_plot]["artist_properties_dict"].items())[0:1]),
                                                                    **dict(list(self.data_series_dict[self.chosen_plot]["artist_properties_dict"].items())[2:])).pop()
        else:
            mat_art.setp(self.data_series_dict[self.chosen_plot]["artist"], 
                        **self.data_series_dict[self.chosen_plot]["artist_properties_dict"])
        self.update_legend(plot)
        canvas.show()

    def event_for_submit_plot_config_button(self, plot, canvas):
        self.event_for_apply_plot_config_button(plot, canvas, False)
        self.event_for_close_popup_button(
            self.popup_creator.plot_configuration_popup)

    def event_for_modify_plot_button(self, plot, canvas):
        if (not self.chosen_plot):
            self.popup_creator.messagebox_popup("No plot chosen for modification. "
                                                "First click on a specific plot to pick it and then click on the \"Modify chosen\" button.")
            return
        self.popup_creator.popup_for_plot_configuration(lambda: self.event_for_close_popup_button(self.popup_creator.plot_configuration_popup),
                                                        lambda: self.event_for_apply_plot_config_button(plot, canvas, False),
                                                        lambda: self.event_for_submit_plot_config_button(plot, canvas),
                                                        self.data_series_dict[self.chosen_plot]["artist_properties_dict"],
                                                        self.data_series_dict[self.chosen_plot]["chart_type"])

    def event_for_new_file(self, chart_creator):
        GUICreator.ChartCreator.chart_type.set("")
        GUICreator.ChartCreator.chosen_plot_label = None
        chart_creator.new_file = True
        PropertiesDictionaries.axes_properties_dict = PropertiesDictionaries.create_axes_properties_dict()
        PropertiesDictionaries.grid_properties_dict = PropertiesDictionaries.create_grid_properties_dict()
        PropertiesDictionaries.ticks_properties_dict = PropertiesDictionaries.create_ticks_properties_dict()
        PropertiesDictionaries.legend_properties_dict = PropertiesDictionaries.create_legend_properties_dict()
        chart_creator.quit()
        chart_creator.destroy()

    def event_for_save_file(self):
        path_to_file = self.popup_creator.popup_for_save_file()
        if (path_to_file and self.parser.check_application_file_extension(path_to_file)):
            self.parser.write_dicts_to_file(path_to_file, self.data_series_dict)
        else:
            self.popup_creator.messagebox_popup("Files can be saved with .cc extension only.")
                
    def event_for_open_file(self, plot, canvas, data_series_combobox):
        path_to_file = self.popup_creator.popup_for_openfile()
        if (path_to_file and self.parser.check_application_file_extension(path_to_file)):
            self.parser.read_dicts_from_file(path_to_file, self.data_series_dict)
            for data_series_name in self.data_series_dict.keys():
                if (self.data_series_dict[data_series_name]["chart_type"] and not self.data_series_dict[data_series_name]["artist"]):
                    self.data_series_name = data_series_name
                    self.draw_plot(plot)
                    self.chosen_plot = data_series_name
                    self.event_for_apply_plot_config_button(plot, canvas, True)
            self.chosen_plot = ""
            self.update_chosen_plot_label(self.chosen_plot)
            self.event_for_update_data_series_combobox(data_series_combobox)
            data_series_combobox.current(
                len(data_series_combobox["values"]) - 1)
            self.data_series_name = data_series_combobox["values"][len(data_series_combobox["values"]) - 1]
            data_series_combobox.event_generate("<<ComboboxSelected>>")
            self.event_for_apply_config_button(plot, canvas, True)
        else:
            self.popup_creator.messagebox_popup("Wrong file format. Only .cc files can be opened.")
