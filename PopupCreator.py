from Constants import *
from PropertiesDictionaries import *

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser

import re

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.artist as mat_art

class PopupCreator(object):
    def __init__(self):
        self.excel_sheet_popup = None
        self.provide_name_popup = None
        self.plot_popup = None
        self.chart_configuration_popup = None
        self.plot_types_popup = None
        self.name_entry = None
        self.canvas = None
        self.entry_frame = None
        self.entry_list = []
        self.excel_sheet_validation_function = None
        self.plot = None
        self.axes_frame = None
        self.grid_frame = None
        self.ticks_frame = None
        self.legend_frame = None
        self.plot_types_listbox = None

    def popup_for_openfile(self):
        return filedialog.askopenfilename()

    def popup_for_provide_name(self, file_name, event_for_submit_name_button, event_for_close_name_popup_button):
        self.provide_name_popup = tk.Toplevel()
        self.provide_name_popup.grab_set()
        self.provide_name_popup.protocol("WM_DELETE_WINDOW", event_for_close_name_popup_button)
        self.provide_name_popup.wm_title("Load data series...")
        self.provide_name_popup.wm_minsize(300, 150)
        self.provide_name_popup.wm_maxsize(300, 150)
        self.provide_name_popup.rowconfigure(0, weight=1)
        self.provide_name_popup.rowconfigure(1, weight=1)
        self.provide_name_popup.rowconfigure(2, weight=1)
        self.provide_name_popup.columnconfigure(0, weight=1)
        self.provide_name_popup.columnconfigure(1, weight=1)
        name_label = tk.Label(self.provide_name_popup, text="Provide name for chosen data series.")
        name_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=10, padx=38)
        self.name_entry = ttk.Entry(self.provide_name_popup, width=37)
        self.name_entry.grid(row=1, column=0, columnspan=2, sticky="w", padx=38)
        self.name_entry.insert(0, file_name)
        self.name_entry.focus_set()
        submit_button = ttk.Button(self.provide_name_popup, text="Submit", cursor="hand2",
                                   command=event_for_submit_name_button)
        submit_button.grid(row=2, column=0, pady=10, sticky="n")
        cancel_button = ttk.Button(self.provide_name_popup, text="Cancel", cursor="hand2",
                                   command=event_for_close_name_popup_button)
        cancel_button.grid(row=2, column=1, pady=10, sticky="n")
        self.provide_name_popup.mainloop()

    def messagebox_popup(self, message_info):
        messagebox.showinfo("Info", message=message_info)

    def popup_for_excel_sheet(self, window_title, event_for_close_popup, event_for_submit_button,
                              event_for_add_row_button):
        self.excel_sheet_popup = tk.Toplevel()
        self.excel_sheet_popup.grab_set()
        self.excel_sheet_popup.wm_minsize(400, 340)
        self.excel_sheet_popup.wm_maxsize(400, 340)
        self.excel_sheet_popup.wm_title(window_title)
        self.excel_sheet_popup.protocol("WM_DELETE_WINDOW", event_for_close_popup)
        self.excel_sheet_validation_function = self.excel_sheet_popup.register(self.validate_entry_data)
        name_label = tk.Label(self.excel_sheet_popup, text="Name:")
        name_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.name_entry = ttk.Entry(self.excel_sheet_popup, width=40)
        self.name_entry.grid(row=0, column=0, sticky="n", pady=10)
        scrollbar = ttk.Scrollbar(self.excel_sheet_popup, cursor="hand2")
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.canvas = tk.Canvas(self.excel_sheet_popup, yscrollcommand=scrollbar.set, highlightthickness=0)
        self.canvas.grid(row=1, column=0)
        scrollbar.config(command=self.canvas.yview)
        self.entry_frame = tk.Frame(self.canvas, takefocus=0)
        self.canvas.create_window((0, 1), window=self.entry_frame, anchor='nw')
        x_label = tk.Label(self.entry_frame, text="x", font=SMALL_BOLD_FONT, borderwidth=2, relief="groove")
        x_label.grid(row=0, column=0, sticky="we")
        y_label = tk.Label(self.entry_frame, text="y", font=SMALL_BOLD_FONT, borderwidth=2, relief="groove")
        y_label.grid(row=0, column=1, sticky="we")
        z_label = tk.Label(self.entry_frame, text="z", font=SMALL_BOLD_FONT, borderwidth=2, relief="groove")
        z_label.grid(row=0, column=2, sticky="nwe")
        self.create_initial_entries()
        self.update_scroll_region()
        submit_button = ttk.Button(self.excel_sheet_popup, text="Submit", cursor="hand2",
                                   command=event_for_submit_button)
        submit_button.grid(row=2, column=0, sticky="w")
        cancel_button = ttk.Button(self.excel_sheet_popup, text="Cancel", cursor="hand2",
                                   command=event_for_close_popup)
        cancel_button.grid(row=2, column=0, sticky="ns")
        add_row_button = ttk.Button(self.excel_sheet_popup, text="Add row...", cursor="hand2",
                                    command=event_for_add_row_button)
        add_row_button.grid(row=2, column=0, sticky="e")

    def create_initial_entries(self):
        for _ in range(1, 15):
            self.add_entry()

    def update_scroll_region(self):
        self.canvas.yview_moveto(0.0)
        self.excel_sheet_popup.update()
        self.canvas.configure(scrollregion=(
            self.entry_frame.winfo_x(), self.entry_frame.winfo_y(), self.entry_frame.winfo_width(),
            self.entry_frame.winfo_height() + 1))

    def add_entry(self):
        row_number = int((len(self.entry_list) / 3) + 1)
        for column in range(0, 3):
            entry = ttk.Entry(self.entry_frame, width=20, validatecommand=(self.excel_sheet_validation_function, "%P"),
                              validate="key")
            self.entry_list.append(entry)
            entry.grid(row=row_number, column=column)

    def validate_entry_data(self, content):
        if (re.search("[^-0-9.]", content)):
            return False
        if (content.count(".") > 1 or content.count("-") > 1):
            return False
        if (re.match(".+[-]|[-]?\..*", content)):
            return False
        return True

    def popup_for_plot(self, event_for_close_popup):
        self.plot_popup = tk.Toplevel()
        self.plot_popup.grab_set()
        self.plot_popup.wm_title("Plot")
        self.plot_popup.protocol("WM_DELETE_WINDOW", event_for_close_popup)
        figure = Figure(dpi=100)
        self.plot = figure.add_subplot(111)
        mat_art.setp(self.plot, **axes_properties_dict)
        self.plot.grid(**grid_properties_dict)
        self.plot.tick_params(**ticks_properties_dict)
        canvas = FigureCanvasTkAgg(figure, self.plot_popup)
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self.plot_popup)
        toolbar.update()
        canvas._tkcanvas.pack()
        canvas.show()

    def popup_for_chart_configuration(self, event_for_close_popup, event_for_submit_button, event_for_apply_button, tab_title):
        self.chart_configuration_popup = tk.Toplevel()
        self.chart_configuration_popup.grab_set()
        self.chart_configuration_popup.wm_title("Configuration")
        self.chart_configuration_popup.protocol("WM_DELETE_WINDOW", event_for_close_popup)
        self.chart_configuration_popup.wm_minsize(400, 560)
        self.chart_configuration_popup.wm_maxsize(400, 560)
        style = ttk.Style()
        style.configure('TabFont.TNotebook.Tab', font=MEDIUM_FONT)
        option_notebook = ttk.Notebook(self.chart_configuration_popup, style="TabFont.TNotebook", width=380)
        option_notebook.grid(row=0, column=0, columnspan=2, sticky="nwse", padx=10, pady=10)
        submit_button = ttk.Button(self.chart_configuration_popup, text="Submit", command=event_for_submit_button,
                                   cursor="hand2")
        submit_button.grid(row=1, column=0, sticky="w", padx=10)
        apply_button = ttk.Button(self.chart_configuration_popup, text="Apply", command=event_for_apply_button,
                                   cursor="hand2")
        apply_button.grid(row=1, column=0, sticky="e", padx=10)
        cancel_button = ttk.Button(self.chart_configuration_popup, text="Cancel", command=event_for_close_popup,
                                   cursor="hand2")
        cancel_button.grid(row=1, column=1, sticky="s", padx=10)
        self.axes_frame = tk.Frame(option_notebook)
        self.axes_frame.grid(sticky="nwse")
        self.setup_options_for_config_tab(self.axes_frame, axes_properties_dict, axes_properties_UI_dict,
                                          axes_properties_mapping_dict)
        self.grid_frame = tk.Frame(option_notebook)
        self.grid_frame.grid(sticky="nwse")
        self.setup_options_for_config_tab(self.grid_frame, grid_properties_dict, grid_properties_UI_dict,
                                          gird_properties_mapping_dict)
        self.ticks_frame = tk.Frame(option_notebook)
        self.ticks_frame.grid(sticky="nwse")
        self.setup_options_for_config_tab(self.ticks_frame, ticks_properties_dict, ticks_properties_UI_dict,
                                          ticks_properties_mapping_dict)
        legend_tab_frame = tk.Frame(option_notebook, bg="black")
        legend_tab_frame.columnconfigure(0, weight=22)
        legend_tab_frame.columnconfigure(1, weight=1)
        legend_tab_frame.rowconfigure(0, weight=10)
        scrollbar = ttk.Scrollbar(legend_tab_frame, cursor="hand2")
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas = tk.Canvas(legend_tab_frame, yscrollcommand=scrollbar.set, highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nwse")
        scrollbar.config(command=canvas.yview)
        self.legend_frame = tk.Frame(canvas, takefocus=0)
        self.setup_options_for_config_tab(self.legend_frame, legend_properties_dict, legend_properties_UI_dict,
                                          legend_properties_mapping_dict)
        canvas.create_window((0, 1), window=self.legend_frame, anchor='nw', 
                            height=len(self.legend_frame.winfo_children()) * 45 / 2)
        canvas.configure(scrollregion=(0,0,0,len(self.legend_frame.winfo_children()) * 45 / 2))
        option_notebook.add(self.axes_frame, text="Axes")
        option_notebook.add(self.grid_frame, text="Grid")
        option_notebook.add(self.ticks_frame, text="Ticks")
        option_notebook.add(legend_tab_frame, text="Legend")
        for tab in option_notebook.tabs():
            if (option_notebook.tab(tab, "text") == tab_title):
                option_notebook.select(tab)
                break
        self.chart_configuration_popup.mainloop()

    def setup_options_for_config_tab(self, parent_frame, properties_dict, UI_dict, mapping_dict):
        for row_nr in range(0, len(mapping_dict.keys())):
            label = ttk.Label(parent_frame, text=list(mapping_dict.keys())[row_nr] + ":", justify="left",
                              font=SMALL_FONT, width=20)
            label.grid(row=row_nr, column=0, padx=10, pady=12, sticky="w")
            if (type(UI_dict[list(mapping_dict.keys())[row_nr]]) == str):
                entry = ttk.Entry(parent_frame, width=26)
                entry.insert(0, UI_dict[list(mapping_dict.keys())[row_nr]])
                entry.grid(row=row_nr, column=1, padx=20, sticky="e")                           
            else:
                combobox = ttk.Combobox(parent_frame, state="readonly", font=SMALL_FONT,
                                        values=list(UI_dict[list(mapping_dict.keys())[row_nr]].values()))
                combobox.set(UI_dict[list(mapping_dict.keys())[row_nr]]
                             [properties_dict[list(mapping_dict.values())[row_nr]]])
                combobox.grid(row=row_nr, column=1, padx=19, sticky="e")
        if (parent_frame != self.axes_frame and parent_frame != self.legend_frame):
            separator = ttk.Separator(parent_frame, orient="horizontal")
            separator.grid(row=1, column=0, columnspan=2, padx=10, sticky="wse")

    def popup_for_plot_types(self, event_for_close_popup, event_for_submit_button):
        self.plot_types_popup = tk.Toplevel()
        self.plot_types_popup.grab_set()
        self.plot_types_popup.wm_title("Plot types")
        self.plot_types_popup.protocol("WM_DELETE_WINDOW", event_for_close_popup)
        self.plot_types_popup.wm_minsize(250, 260)
        self.plot_types_popup.wm_maxsize(250, 260)
        plot_types = ["Horizontal bar", "Error bar", "Histogram", "Stack plot", "Stem plot", "Step plot"]
        choose_plot_type_label = ttk.Label(self.plot_types_popup, text="Choose plot type:", font=SMALL_FONT)
        choose_plot_type_label.grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")
        self.plot_types_listbox = tk.Listbox(self.plot_types_popup, activestyle="none", font=SMALL_FONT, 
                                        height=10, width=30, highlightthickness=0)
        for plot_type in plot_types:
            self.plot_types_listbox.insert("end", " " + plot_type)
        self.plot_types_listbox.grid(row=1, column=0, columnspan=2, padx=15, sticky="nwse")
        submit_button = ttk.Button(self.plot_types_popup, text="Submit", command=event_for_submit_button,
                                   cursor="hand2")
        submit_button.grid(row=2, column=0, sticky="w", padx=15, pady=10)
        cancel_button = ttk.Button(self.plot_types_popup, text="Cancel", command=event_for_close_popup,
                                   cursor="hand2")
        cancel_button.grid(row=2, column=1, sticky="e", padx=15, pady=10)
        #### think about pie chart
        # barh, broken_barh? just for fun later, cohere?no ide how works, csd OK how, errorbar OK,
        # hexbin? no idea how works, hist ok, loglog OK, semilogx OK, semilogy OK,
        # magnitude_sepctrum OK how, phase_spectrum OK how, pie OK, plot_date? to consider,
        # psd? OK how, quiver? consider, stackplot? OK, stem, step? OK,
        # violinplot? dont think so, 
        # 'convert_xunits', 'convert_yunits', 'format_coord', 'format_cursor_data', 'format_xdata', 'format_ydata', 'minorticks_off', 
        # 'minorticks_on'



        self.plot_types_popup.mainloop()
