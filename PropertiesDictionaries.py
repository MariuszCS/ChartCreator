import numpy as np
from Constants import *
import matplotlib

def create_dict_for_open_button(chart_type):
    if (chart_type == "Line" or chart_type == "Stem plot"):   
        return create_line_properties_dict()
    elif (chart_type == "Points"):
        return create_point_properties_dict()
    elif (chart_type == "Bars"):
        return create_bar_properties_dict()
    elif (chart_type == "Horizontal bar"):
        return create_horizontal_bar_properties_dict()
    elif (chart_type == "Error bar"):
        return create_error_bar_properties_dict()
    elif (chart_type == "Histogram"):
        return create_histogram_properties_dict()
    elif (chart_type == "Stack plot"):
        return create_stack_properties_dict()
    elif (chart_type == "Step plot"):
        return create_step_properties_dict()

def choose_proper_dicts(chart_type):
    if (chart_type == "Line" or chart_type == "Stem plot"):   
        return line_properties_UI_dict, line_properties_mapping_dict
    elif (chart_type == "Points"):
        return point_properties_UI_dict, point_properties_mapping_dict
    elif (chart_type == "Bars"):
        return bar_properties_UI_dict, bar_properties_mapping_dict
    elif (chart_type == "Horizontal bar"):
        return horizontal_bar_properties_UI_dict, horizontal_bar_properties_mapping_dict
    elif (chart_type == "Error bar"):
        return error_bar_properties_UI_dict, error_bar_properties_mapping_dict
    elif (chart_type == "Histogram"):
        return histogram_properties_UI_dict, histogram_properties_mapping_dict
    elif (chart_type == "Stack plot"):
        return stack_properties_UI_dict, stack_properties_mapping_dict
    elif (chart_type == "Step plot"):
        return step_properties_UI_dict, step_properties_mapping_dict

color_dict = dict(
        {
            "#ffffff": "White",
            "#b3b3b3": "Grey",
            "#000000": "Black",
            "#ff0000": "Red",
            "#ffff00": "Yellow",
            "#00ff00": "Green",
            "#0000ff": "Blue",
            "#ff00ff": "Purple",
            "#ffa500": "Orange",
            "#cc6600": "Brown",
            "#ffc0cb": "Pink",
            "#00ffff": "Aqua"
        }
    )

"""
Every data series that is plotted has its own series properties dict, so no instance created here, but only function, to create one during
plotting and configuration (temp objects for config.)
"""
def create_series_properties_dict():
    return dict(
        {
            "x": [],
            "y": [],
            "artist": None,
            "chart_type": "",
            "color": "",
            "plot_name": "",
            "artist_properties_dict": None
        }
    )


"""
Dictionary that will be passed as **kwargs to the .grid() function of the subplot object with all the settable grid properties
"""
def create_grid_properties_dict():
    return dict(
        {
            "axis": "both",
            "which": "major",
            "visible": True,
            "alpha": 0.8,
            "color": "#b3b3b3",
            "linestyle": "solid",
            "linewidth": 1,
        }
    )
"""
Dictionary which keys and values (values of the sub dictionaries) are displayed in the GUI
"""
grid_properties_UI_dict = dict(
    {
        "Apply to axis": dict(
            {
                "x": "Only x",
                "y": "Only y",
                "both": "Both x and y"
            }
        ),
        "Apply to lines for ": dict(
            {
                "minor": "Minor ticks",
                "major": "Major ticks",
                "both": "Both major and minor ticks"
            }
        ),
        "Visibility": dict(
            {
                True: "Show",
                False: "Hide"
            }
        ),
        "Opacity": {round(x, 1): str(round(x, 1)) for x in np.linspace(0.1, 1, 10)},
        "Color": color_dict,
        "Style": dict(
            {
                "solid": "Solid (-)",
                "dashed": "Dashed (--)",
                "dashdot": "Dashdot (-.)",
                "dotted": "Dotted (..)"
            }
        ),
        "Width": {(x / 10): str((x / 10)) for x in range(1, 31)},
    }
)

grid_properties_dict = create_grid_properties_dict()
"""
Dictionary mapping the key from the dictionary that it displayed in the GUI to the key from the dictionary that is passed
as **kwargs to the drawing function
"""
gird_properties_mapping_dict = {list(grid_properties_UI_dict.keys())[index]: list(grid_properties_dict.keys())[index]
                                for index in range(0, len(grid_properties_dict.keys()))}

def create_ticks_properties_dict():
    return dict(
        {
            "axis": "both",
            "which": "major",
            "visible": True,
            "direction": "out",
            "length": 4,
            "width": 1,
            "color": "#000000",
            "label": True,
            "pad": 2,
            "labelsize": 10,
            "labelcolor": "#000000",
            "rotation": 0
        }
    )

ticks_properties_UI_dict = dict(
    {
        "Apply to axis": dict(
            {
                "x": "Only x",
                "y": "Only y",
                "both": "Both x and y",
            }
        ),
        "Apply to ticks": dict(
            {
                "major": "Major",
                "minor": "Minor",
                "both": "Both major and minor"
            }
        ),
        "Ticks": dict(
            {
                True: "Show",
                False: "Hide"
            }
        ),
        "Ticks position": dict(
            {
                "in": "Inside the axes",
                "out": "Outside the axes",
                "inout": "Both inside and outside"
            }
        ),
        "Ticks length": {x: str(x) for x in range(1, 11)},
        "Ticks width": {x: str(x) for x in range(1, 11)},
        "Ticks color": color_dict,
        "Label": dict(
            {
                True: "Show",
                False: "Hide"
            }
        ),
        "Label-tick distance": {x: str(x) for x in range(1, 11)},
        "Label size": {x: str(x) for x in range(4, 21)},
        "Label color": color_dict,
        "Label rotation": {x: str(x) for x in range(0, 360, 10)}
    }
)

ticks_properties_dict = create_ticks_properties_dict()

ticks_properties_mapping_dict = {list(ticks_properties_UI_dict.keys())[index]: list(ticks_properties_dict.keys())[index]
                                for index in range(0, len(ticks_properties_dict.keys()))}

def create_axes_properties_dict():
    return dict(
        {
            "axisbelow": True,
            "frame_on": True,
            "title": "Chart",
            "facecolor": "#ffffff",
            "xlabel": "x",
            "ylabel": "y",
        }
    )

axes_properties_UI_dict = dict(
    {
        "Axis position": dict(
            {
                True: "Below",
                False: "Above"
            }
        ),
        "Axis frame": dict(
            {
                True: "On",
                False: "Off"
            }
        ),
        "Title": "Chart",
        "Background color": color_dict,
        "X axis label": "x",
        "Y axis label": "y",
    }
)

axes_properties_dict = create_axes_properties_dict()

axes_properties_mapping_dict = {list(axes_properties_UI_dict.keys())[index]: list(axes_properties_dict.keys())[index]
                                for index in range(0, len(axes_properties_dict.keys()))}

def create_legend_properties_dict():
    return dict(
        {
            "visible": True,
            "draggable": False,
            "loc": 0,
            "frameon": True,
            "fancybox": True,
            "shadow": False,
            "framealpha": 0.8,
            "edgecolor": "#b3b3b3",
            "facecolor": "#ffffff",
            "title": "Legend",
            "fontsize": 10,
            "borderpad": 1,
            "labelspacing": 1,
            "handletextpad": 1,
            "borderaxespad": 1,
            "columnspacing": 1,
            "ncol": 1,
            "markerscale": 1,
            "markerfirst": True,
            "scatterpoints": 1
        }
    )

legend_properties_UI_dict = dict(
    {
        "Visibility": dict(
            {
                True: "Show",
                False: "Hide"
            }
        ),
        "Draggable": dict(
            {
                True: "On",
                False: "Off"
            }
        ),
        "Location": dict(
            {
                0: "Best",
                1: "Upper right",
                2: "Upper left",
                3: "Lower left",
                4: "Lower right",
                5: "Right",
                6: "Center left",
                7: "Center right",
                8: "Lower center",
                9: "Upper center",
                10: "Center",
            }
        ),
        "Box": dict(
            {
                True: "On",
                False: "Off"
            }
        ),
        "Box layout": dict(
            {
                True: "Fancy",
                False: "Normal"
            }
        ),
        "Box shadow": dict(
            {
                True: "On",
                False: "Off"
            }
        ),
        "Opacity": {(x / 10): str((x / 10)) for x in range(1, 11)},
        "Border color": color_dict,
        "Background color": color_dict,
        "Title": "Legend",
        "Font size": {x: str(x) for x in range(6, 14)},
        "Border-inside spacing": {(x / 10): str(x / 10) for x in range(0, 21)},
        "Label spacing": {(x / 10): str(x / 10) for x in range(0, 21)},
        "Marker-text spacing": {(x / 10): str(x / 10) for x in range(0, 21)},
        "Border-axes spacing": {(x / 10): str(x / 10) for x in range(0, 31)},
        "Column spacing": {(x / 10): str(x / 10) for x in range(0, 41, 2)},
        "Number of columns": {x: str(x) for x in range(1, 5)},
        "Marker scale": {(x / 10): str(x / 10) for x in range(1, 31)},
        "Marker position": dict(
            {
                True: "Left",
                False: "Right"
            }
        ),
        "No. of scatter points": {x: str(x) for x in range(1, 4)},
    }
)

legend_properties_dict = create_legend_properties_dict()

legend_properties_mapping_dict = {list(legend_properties_UI_dict.keys())[index]: list(legend_properties_dict.keys())[index]
                                for index in range(0, len(legend_properties_dict.keys()))}

def create_line_properties_dict():
    return dict(
        {
            "alpha": 1,
            "linewidth": 1,
            "color": "#000000",
            "linestyle": "solid",
            "marker": "None",
            "markersize": 4,
            "markeredgecolor": "#000000",
            "markerfacecolor": "#000000",
            "markeredgewidth": 1,
            "solid_capstyle": "projecting",
            "dash_capstyle": "projecting",
            "zorder": 1
        }
    )

line_properties_UI_dict = dict(
    {
        "Opacity": {(x / 10): str((x / 10)) for x in range(1, 11)},
        "Line width": {(x / 10): str((x / 10)) for x in range(2, 112, 2)},
        "Line color": color_dict,
        "Line style": dict(
            {
                "solid": "Solid (-)",
                "dashed": "Dashed (--)",
                "dashdot": "Dashdot (-.)",
                "dotted": "Dotted (..)"
            }
        ),
        "Marker type": dict(
            {
                "None": "None",
                ".": "Point",
                "v": "Triangle down",
                "^": "Triangle up",
                "<": "Triangle left",
                ">": "Triangle right",
                "1": "Tri down",
                "2": "Tri up",
                "3": "Tri left",
                "4": "Tri right",
                "8": "Octagon",
                "s": "Square",
                "p": "Pentagon",
                "P": "Plus (filled)",
                "*": "Star",
                "h": "Hexagon1",
                "+": "Plus",
                "x": "X",
                "X": "X (filled)",
                "D": "Diamond",
                "d": "Thin diamond"
            }
        ),
        "Marker size": {(x / 10): str((x / 10)) for x in range(2, 112, 2)},
        "Marker edge color": color_dict,
        "Marker body color": color_dict,
        "Marker edge width": {(x / 10): str((x / 10)) for x in range(2, 52, 2)},
        "Solid line end type": dict(
            {
                "projecting": "Flat",
                "round": "Round",
            }
        ),
        "Dash line end type": dict(
            {
                "projecting": "Flat",
                "round": "Round",
            }
        ),
        "Z order": {x : str(x) for x in range(1, 31)}
    }
)

line_properties_dict = create_line_properties_dict()

line_properties_mapping_dict = {list(line_properties_UI_dict.keys())[index]: list(line_properties_dict.keys())[index]
                                for index in range(0, len(line_properties_dict.keys()))}

def create_bar_properties_dict():
    return dict(
        {
            "alpha": 1,
            "width": 2,
            "fill": True,
            "facecolor": "#000000",
            "linestyle": "solid",
            "linewidth": 1,
            "edgecolor": "#000000",
            "hatch": ".",
            "capstyle": "projecting",
            "zorder": 1
        }
    )

bar_properties_UI_dict = dict(
    {
        "Opacity": {(x / 10): str((x / 10)) for x in range(1, 11)},
        "Bar width": {(x / 10): str((x / 10)) for x in range(2, 112, 2)},
        "Fill": dict(
            {
                True: "Filled",
                False: "Empty"
            }
        ),
        "Bar body color": color_dict,
        "Edge style": dict(
            {
                "solid": "Solid (-)",
                "dashed": "Dashed (--)",
                "dashdot": "Dashdot (-.)",
                "dotted": "Dotted (..)"
            }
        ),
        "Edge width": {(x / 10): str((x / 10)) for x in range(2, 52, 2)},
        "Bar edge/hatch color": color_dict,
        "Hatch type": dict(
            {
                "/": "diagonal hatching",
                "\\": "back diagonal",
                "|": "vertical",
                "-": "horizontal",
                "+": "crossed",
                "x": "crossed diagonal",
                "o": "small circle",
                "O": "large circle",
                ".": "dots",
                "*": "stars"
            }
        ),
        "Dashed edge end type": dict(
            {
                "projecting": "Flat",
                "round": "Round",
            }
        ),
        "Z order": {x : str(x) for x in range(1, 31)}
    }
)

bar_properties_dict = create_bar_properties_dict()

bar_properties_mapping_dict = {list(bar_properties_UI_dict.keys())[index]: list(bar_properties_dict.keys())[index]
                                for index in range(0, len(bar_properties_dict.keys()))}

def create_point_properties_dict():
    return dict(
        {
            "alpha": 1,
            "marker": ".",
            "markersize": 6,
            "markeredgecolor": "#000000",
            "markerfacecolor": "#000000",
            "markeredgewidth": 1,
            "zorder": 1
        }
    )

point_properties_UI_dict = dict(
    {
        "Opacity": {(x / 10): str((x / 10)) for x in range(1, 11)},
        "Marker type": dict(
            {
                "None": "None",
                ".": "Point",
                "v": "Triangle down",
                "^": "Triangle up",
                "<": "Triangle left",
                ">": "Triangle right",
                "1": "Tri down",
                "2": "Tri up",
                "3": "Tri left",
                "4": "Tri right",
                "8": "Octagon",
                "s": "Square",
                "p": "Pentagon",
                "P": "Plus (filled)",
                "*": "Star",
                "h": "Hexagon1",
                "+": "Plus",
                "x": "X",
                "X": "X (filled)",
                "D": "Diamond",
                "d": "Thin diamond"
            }
        ),
        "Marker size": {(x / 10): str((x / 10)) for x in range(2, 202, 2)},
        "Marker edge color": color_dict,
        "Marker body color": color_dict,
        "Marker edge width": {(x / 10): str((x / 10)) for x in range(2, 52, 2)},
        "Z order": {x : str(x) for x in range(1, 31)}
    }
)

point_properties_dict = create_point_properties_dict()

point_properties_mapping_dict = {list(point_properties_UI_dict.keys())[index]: list(point_properties_dict.keys())[index]
                                for index in range(0, len(point_properties_dict.keys()))}

def create_horizontal_bar_properties_dict():
    return dict(
        {
            "alpha": 1,
            "height": 2,
            "fill": True,
            "facecolor": "#000000",
            "linestyle": "solid",
            "linewidth": 1,
            "edgecolor": "#000000",
            "hatch": ".",
            "capstyle": "projecting",
            "zorder": 1
        }
    )

horizontal_bar_properties_UI_dict = dict(
    {
        "Opacity": {(x / 10): str((x / 10)) for x in range(1, 11)},
        "Bar height": {(x / 10): str((x / 10)) for x in range(2, 112, 2)},
        "Fill": dict(
            {
                True: "Filled",
                False: "Empty"
            }
        ),
        "Bar body color": color_dict,
        "Edge style": dict(
            {
                "solid": "Solid (-)",
                "dashed": "Dashed (--)",
                "dashdot": "Dashdot (-.)",
                "dotted": "Dotted (..)"
            }
        ),
        "Edge width": {(x / 10): str((x / 10)) for x in range(2, 52, 2)},
        "Bar edge/hatch color": color_dict,
        "Hatch type": dict(
            {
                "/": "diagonal hatching",
                "\\": "back diagonal",
                "|": "vertical",
                "-": "horizontal",
                "+": "crossed",
                "x": "crossed diagonal",
                "o": "small circle",
                "O": "large circle",
                ".": "dots",
                "*": "stars"
            }
        ),
        "Dashed edge end type": dict(
            {
                "projecting": "Flat",
                "round": "Round",
            }
        ),
        "Z order": {x : str(x) for x in range(1, 31)}
    }
)

horizontal_bar_properties_dict = create_horizontal_bar_properties_dict()

horizontal_bar_properties_mapping_dict = {list(horizontal_bar_properties_UI_dict.keys())[index]: list(horizontal_bar_properties_dict.keys())[index]
                                            for index in range(0, len(horizontal_bar_properties_dict.keys()))}

def create_error_bar_properties_dict():
    return dict(
        {
            "alpha": 1,
            "xerr": 0.2,
            "yerr": 0.2,
            "elinewidth": 1,
            "ecolor": "#000000",
            "capsize": 0,
            "zorder": 1
        }
    )

error_bar_properties_UI_dict = dict(
    {
        "Opacity": {(x / 10): str((x / 10)) for x in range(1, 11)},
        "X width": {(x / 10): str((x / 10)) for x in range(1, 21)},
        "Y height": {(x / 10): str((x / 10)) for x in range(1, 21)},
        "Line width": {(x / 10): str((x / 10)) for x in range(2, 52, 2)},
        "Line color": color_dict,
        "Cap size": {(x / 10): str((x / 10)) for x in range(0, 82, 2)},
        "Z order": {x : str(x) for x in range(1, 31)}
    }
)

error_bar_properties_dict = create_error_bar_properties_dict()

error_bar_properties_mapping_dict = {list(error_bar_properties_UI_dict.keys())[index]: list(error_bar_properties_dict.keys())[index]
                                for index in range(0, len(error_bar_properties_dict.keys()))}

def create_histogram_properties_dict():
    return dict(
        {
            "alpha": 1,
            "fill": True,
            "facecolor": "#000000",
            "linestyle": "solid",
            "linewidth": 1,
            "edgecolor": "#000000",
            "hatch": ".",
            "capstyle": "projecting",
            "zorder": 1
        }
    )

histogram_properties_UI_dict = dict(
    {
        "Opacity": {(x / 10): str((x / 10)) for x in range(1, 11)},
        "Fill": dict(
            {
                True: "Filled",
                False: "Empty"
            }
        ),
        "Bar body color": color_dict,
        "Edge style": dict(
            {
                "solid": "Solid (-)",
                "dashed": "Dashed (--)",
                "dashdot": "Dashdot (-.)",
                "dotted": "Dotted (..)"
            }
        ),
        "Edge width": {(x / 10): str((x / 10)) for x in range(2, 52, 2)},
        "Bar edge/hatch color": color_dict,
        "Hatch type": dict(
            {
                "/": "diagonal hatching",
                "\\": "back diagonal",
                "|": "vertical",
                "-": "horizontal",
                "+": "crossed",
                "x": "crossed diagonal",
                "o": "small circle",
                "O": "large circle",
                ".": "dots",
                "*": "stars"
            }
        ),
        "Dashed edge end type": dict(
            {
                "projecting": "Flat",
                "round": "Round",
            }
        ),
        "Z order": {x : str(x) for x in range(1, 31)}
    }
)

histogram_properties_dict = create_histogram_properties_dict()

histogram_properties_mapping_dict = {list(histogram_properties_UI_dict.keys())[index]: list(histogram_properties_dict.keys())[index]
                                for index in range(0, len(histogram_properties_dict.keys()))}

def create_stack_properties_dict():
    return dict(
        {
            "alpha": 1,
            "facecolor": "#000000",
            "linestyle": "solid",
            "linewidth": 1,
            "edgecolor": "#000000",
            "zorder": 1
        }
    )

stack_properties_UI_dict = dict(
    {
        "Opacity": {(x / 10): str((x / 10)) for x in range(1, 11)},
        "Body color": color_dict,
        "Edge style": dict(
            {
                "solid": "Solid (-)",
                "dashed": "Dashed (--)",
                "dashdot": "Dashdot (-.)",
                "dotted": "Dotted (..)"
            }
        ),
        "Edge width": {(x / 10): str((x / 10)) for x in range(2, 52, 2)},
        "Edge color": color_dict,
        "Z order": {x : str(x) for x in range(1, 31)}
    }
)

stack_properties_dict = create_stack_properties_dict()

stack_properties_mapping_dict = {list(stack_properties_UI_dict.keys())[index]: list(stack_properties_dict.keys())[index]
                                for index in range(0, len(stack_properties_dict.keys()))}

def create_step_properties_dict():
    return dict(
        {
            "alpha": 1,
            "where": "pre",
            "linewidth": 1,
            "color": "#000000",
            "linestyle": "solid",
            "marker": "None",
            "markersize": 4,
            "markeredgecolor": "#000000",
            "markerfacecolor": "#000000",
            "markeredgewidth": 1,
            "solid_capstyle": "projecting",
            "dash_capstyle": "projecting",
            "zorder": 1
        }
    )

step_properties_UI_dict = dict(
    {
        "Opacity": {(x / 10): str((x / 10)) for x in range(1, 11)},
        "Steps placed": dict(
            {
                "pre": "Before point",
                "mid": "Middle way",
                "post": "After point",
            }
        ),
        "Line width": {(x / 10): str((x / 10)) for x in range(2, 112, 2)},
        "Line color": color_dict,
        "Line style": dict(
            {
                "solid": "Solid (-)",
                "dashed": "Dashed (--)",
                "dashdot": "Dashdot (-.)",
                "dotted": "Dotted (..)"
            }
        ),
        "Marker type": dict(
            {
                "None": "None",
                ".": "Point",
                "v": "Triangle down",
                "^": "Triangle up",
                "<": "Triangle left",
                ">": "Triangle right",
                "1": "Tri down",
                "2": "Tri up",
                "3": "Tri left",
                "4": "Tri right",
                "8": "Octagon",
                "s": "Square",
                "p": "Pentagon",
                "P": "Plus (filled)",
                "*": "Star",
                "h": "Hexagon1",
                "+": "Plus",
                "x": "X",
                "X": "X (filled)",
                "D": "Diamond",
                "d": "Thin diamond"
            }
        ),
        "Marker size": {(x / 10): str((x / 10)) for x in range(2, 112, 2)},
        "Marker edge color": color_dict,
        "Marker body color": color_dict,
        "Marker edge width": {(x / 10): str((x / 10)) for x in range(2, 52, 2)},
        "Solid line end type": dict(
            {
                "projecting": "Flat",
                "round": "Round",
            }
        ),
        "Dash line end type": dict(
            {
                "projecting": "Flat",
                "round": "Round",
            }
        ),
        "Z order": {x : str(x) for x in range(1, 31)}
    }
)

step_properties_dict = create_step_properties_dict()

step_properties_mapping_dict = {list(step_properties_UI_dict.keys())[index]: list(step_properties_dict.keys())[index]
                                for index in range(0, len(step_properties_dict.keys()))}