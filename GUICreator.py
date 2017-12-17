import EventHandler
from Constants import *
from PropertiesDictionaries import *

import tkinter as tk
from tkinter import ttk
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import AutoLocator, AutoMinorLocator
from matplotlib import pyplot as plt
import matplotlib.artist as mat_art

class ChartCreator(tk.Tk):

    chart_type = tk.StringVar

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Plot Creator")
        self.minsize(1000, 650)
        self.event_handler = EventHandler.EventHandler()
        self.data_series_combobox = None
        self.chosen_color_label = None
        self.chosen_color_preview_label = None
        self.name_entry = None
        self.canvas = None
        self.plot = None
        ChartCreator.chart_type = tk.StringVar()
        main_frame = self.setup_main_frame()
        self.setup_menu(main_frame)
        self.setup_top_frame(main_frame)
        self.setup_right_frame(main_frame)
        self.setup_left_frame(main_frame)
        self.setup_bottom_frame(main_frame)
        main_frame.tkraise()

    def setup_main_frame(self):
        main_frame = tk.Frame(self)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=20)
        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.pack(fill="both", expand=True)
        return main_frame

    def setup_menu(self, parent_frame):
        menubar = tk.Menu(parent_frame)
        self.setup_file_menu(menubar)
        self.setup_configure_menu(menubar)
        tk.Tk.config(self, menu=menubar)

    def setup_file_menu(self, parent_menu):
        file_menu = tk.Menu(parent_menu, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_separator()
        file_menu.add_command(label="Open")
        file_menu.add_separator()
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Save as")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        parent_menu.add_cascade(label="File", menu=file_menu)
# axes legend font
    def setup_configure_menu(self, parent_menu):
        configure_menu = tk.Menu(parent_menu, tearoff=0)
        configure_menu.add_command(label="Axes", command=
                                   lambda: self.event_handler.event_for_chart_configuration(self.plot, 
                                                                                            self.canvas,
                                                                                            "Axes"))
        configure_menu.add_separator()
        configure_menu.add_command(label="Grid", command=
                                   lambda: self.event_handler.event_for_chart_configuration(self.plot, 
                                                                                            self.canvas,
                                                                                            "Grid"))
        configure_menu.add_separator()
        configure_menu.add_command(label="Ticks", command=
                                   lambda: self.event_handler.event_for_chart_configuration(self.plot, 
                                                                                            self.canvas,
                                                                                            "Ticks"))
        configure_menu.add_separator()
        configure_menu.add_command(label="Legend", command=
                                   lambda: self.event_handler.event_for_chart_configuration(self.plot, 
                                                                                            self.canvas,
                                                                                            "Legend"))
        parent_menu.add_cascade(label="Configure", menu=configure_menu)

    def setup_top_frame(self, parent_frame):
        top_frame = tk.Frame(parent_frame)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="nwse", padx=3, pady=3)
        title_label = tk.Label(top_frame, text="~~Plot Creator~~", font=BIG_FONT)
        title_label.pack(expand=True)

    def setup_right_frame(self, parent_frame):
        right_frame = tk.LabelFrame(parent_frame, labelanchor="nw", text="Plot")
        right_frame.grid(row=1, column=1, sticky="nwse", padx=3, pady=3)
        self.setup_plot_for_right_frame(right_frame)

    def setup_left_frame(self, parent_frame):
        left_frame = tk.LabelFrame(parent_frame, labelanchor="nw", text="Quick access", width=350)
        left_frame.grid_propagate(0)
        left_frame.rowconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        left_frame.rowconfigure(2, weight=1)
        left_frame.rowconfigure(3, weight=20)
        left_frame.grid(row=1, column=0, sticky="nwse", padx=3, pady=3)
        self.setup_elements_for_left_frame(left_frame)

    def setup_bottom_frame(self, parent_frame):
        bottom_frame = tk.Frame(parent_frame)
        bottom_frame.rowconfigure(0, weight=1)
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky="nwse", padx=3, pady=3)
        self.setup_elements_for_bottom_frame(bottom_frame)

    def setup_elements_for_left_frame(self, parent_frame):
        insert_button = ttk.Button(parent_frame, text="Insert values", cursor="hand2",
                                   command=lambda: self.event_handler.event_for_insert_button(self.data_series_combobox))
        insert_button.grid(row=0, column=0, sticky="n", pady=10)
        load_button = ttk.Button(parent_frame, text="Load file", cursor="hand2",
                                 command=lambda: self.event_handler.event_for_load_button(self.data_series_combobox))
        load_button.grid(row=0, column=1, sticky="n", pady=10)
        self.data_series_combobox = ttk.Combobox(parent_frame, width=38, state="readonly",
                                                 postcommand=lambda: self.event_handler.event_for_update_data_series_combobox(
                                                     self.data_series_combobox))
        self.data_series_combobox.bind("<<ComboboxSelected>>",
                                       lambda event: self.event_handler.data_series_combobox_callback(self.data_series_combobox.get(),
                                                                                                      self.chosen_color_label,
                                                                                                      self.chosen_color_preview_label,
                                                                                                      self.name_entry))
        self.data_series_combobox.grid(row=1, column=0, columnspan=2, sticky="n")
        delete_button = ttk.Button(parent_frame, text="Delete", cursor="hand2",
                                   command=lambda: self.event_handler.event_for_delete_button(self.data_series_combobox,
                                                                                              self.canvas,
                                                                                              self.plot))
        delete_button.grid(row=2, column=0, sticky="n", pady=10)
        modify_button = ttk.Button(parent_frame, text="Modify", cursor="hand2",
                                   command=lambda: self.event_handler.event_for_modify_button(self.data_series_combobox, 
                                                                                              self.canvas,
                                                                                              self.plot))
        modify_button.grid(row=2, column=1, sticky="n", pady=10)
        self.setup_option_frame(parent_frame)

    def setup_option_frame(self, parent_frame):
        option_frame = tk.LabelFrame(parent_frame, labelanchor="nw", text="Options")
        option_frame.grid(row=3, column=0, columnspan=2, sticky="nwse", padx=30, pady=10)
        self.setup_elements_for_option_frame(option_frame)

    def setup_plot_for_right_frame(self, parent_frame):
        figure = Figure(dpi=100)
        self.plot = figure.add_subplot(111)
        self.plot.grid(**grid_properties_dict)
        self.plot.xaxis.set_major_locator(AutoLocator())
        self.plot.xaxis.set_minor_locator(AutoMinorLocator(4))
        self.plot.yaxis.set_major_locator(AutoLocator())
        self.plot.yaxis.set_minor_locator(AutoMinorLocator(4))
        self.plot.tick_params(**ticks_properties_dict)
        mat_art.setp(self.plot, **axes_properties_dict)
        self.plot.autoscale()
        self.canvas = FigureCanvasTkAgg(figure, parent_frame)
        self.canvas.mpl_connect("pick_event", self.event_handler.click_artist_callback) # callback for clicking on the chosen plot event
        #self.canvas.mpl_connect("scroll_event", lambda event: self.event_handler.scroll_callback(event, self.plot, self.canvas))
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        toolbar = NavigationToolbar2TkAgg(self.canvas, parent_frame)
        toolbar.update()
        self.canvas._tkcanvas.pack()

    def setup_elements_for_bottom_frame(self, parent_frame):
        remove_chosen_plot_button = ttk.Button(parent_frame, text="Remove plot", cursor="hand2",
                                               command=lambda: self.event_handler.event_for_remove_plot_button(self.canvas,
                                                                                                               self.data_series_combobox,
                                                                                                               self.plot))
        remove_chosen_plot_button.grid(row=0, column=0, padx=30)
        plot_button = ttk.Button(parent_frame, text="Plot", cursor="hand2",
                                 command=lambda: self.event_handler.event_for_plot_button(self.plot,
                                                                                          self.canvas,
                                                                                          self.name_entry.get()))
        plot_button.grid(row=0, column=1, padx=90)
        open_in_a_new_window_button = ttk.Button(parent_frame, text="Open in a new window", cursor="hand2",
                                                 command=lambda: self.event_handler.event_for_open_in_a_new_window_button())
        open_in_a_new_window_button.grid(row=0, column=2, padx=20)
        auto_scale_button = ttk.Button(parent_frame, text="Auto scale", cursor="hand2",
                                    command=lambda: self.event_handler.event_for_auto_scale_button(self.plot, self.canvas))
        auto_scale_button.grid(row=0, column=3, padx=20)
        clear_button = ttk.Button(parent_frame, text="Clear", cursor="hand2",
                                  command=lambda: self.event_handler.event_for_clear_button(self.canvas,
                                                                                            self.plot,
                                                                                            self.data_series_combobox))
        clear_button.grid(row=0, column=4, padx=20)
        copyright_label = tk.Label(parent_frame, text="Mariusz Chybicki \u00A9", font=SMALL_FONT)
        copyright_label.grid(row=1, column=0, columnspan=4, sticky="w")

    def setup_elements_for_option_frame(self, parent_frame):
        name_label = tk.Label(parent_frame, text="Plot name (legend):", font=MEDIUM_BOLD_FONT)
        name_label.grid(row=0, column=0, columnspan=3, pady=10)
        self.name_entry = ttk.Entry(parent_frame, width=40)
        self.name_entry.grid(row=1, column=0, columnspan=3, padx=15)
        self.name_entry.bind("<Return>",
                             lambda event: self.event_handler.name_entry_callback(self.name_entry.get(),
                                                                                  self.canvas,
                                                                                  self.plot))
        self.name_entry.bind("<FocusOut>",
                             lambda event: self.event_handler.name_entry_callback(self.name_entry.get(),
                                                                                  self.canvas,
                                                                                  self.plot))
        type_label = tk.Label(parent_frame, text="Plot type:", font=MEDIUM_BOLD_FONT)
        type_label.grid(row=2, column=0, columnspan=3, pady=10)
        line_type_radiobutton = ttk.Radiobutton(parent_frame, text="Line", variable=ChartCreator.chart_type, value="line",
                                                cursor="hand2",
                                                command=lambda: self.event_handler.event_for_radiobutton(self.plot,
                                                                                                         self.canvas))
        line_type_radiobutton.grid(row=3, column=0)
        bar_type_radiobutton = ttk.Radiobutton(parent_frame, text="Bars", variable=ChartCreator.chart_type, value="bar",
                                               cursor="hand2",
                                               command=lambda: self.event_handler.event_for_radiobutton(self.plot,
                                                                                                        self.canvas))
        bar_type_radiobutton.grid(row=3, column=1)
        point_type_radiobutton = ttk.Radiobutton(parent_frame, text="Points", variable=ChartCreator.chart_type, value="point",
                                                 cursor="hand2",
                                                 command=lambda: self.event_handler.event_for_radiobutton(self.plot,
                                                                                                          self.canvas))
        point_type_radiobutton.grid(row=3, column=2)
        more_plot_types_button = ttk.Button(parent_frame, text="More...", cursor="hand2",
                                            command=lambda: self.event_handler.event_for_more_plot_types_button(self.plot,
                                                                                                                self.canvas))
        more_plot_types_button.grid(row=4, column=2, pady=10)
        color_label = tk.Label(parent_frame, text="Plot color:", font=MEDIUM_BOLD_FONT)
        color_label.grid(row=5, column=0, columnspan=3)
        color_chooser_button = ttk.Button(parent_frame, text="Color chooser", cursor="hand2",
                                          command=lambda: self.event_handler.event_for_color_chooser_button(self.chosen_color_label,
                                                                                                            self.chosen_color_preview_label,
                                                                                                            self.canvas,
                                                                                                            self.plot))
        color_chooser_button.grid(row=6, column=1, pady=10, sticky="e")
        self.chosen_color_label = ttk.Label(parent_frame, text="Chosen color (hex): ", width=25)
        self.chosen_color_label.grid(row=7, column=0, columnspan=2, padx=15 , pady=10, sticky="w")
        self.chosen_color_preview_label = ttk.Label(parent_frame, width=4)
        self.chosen_color_preview_label.grid(row=7, column=2, padx=15 , pady=10, sticky="nw")
