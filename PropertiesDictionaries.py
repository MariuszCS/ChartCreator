import numpy as np
from Constants import *
from matplotlib import font_manager

def create_color_dict():
    return dict(
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
            "z": [],
            "artist": None,
            "chart_type": "",
            "color": "",
            "plot_name": ""
        }
    )


"""
Dictionary that will be passed as **kwargs to the .grid() function of the subplot object with all the settable grid properties
"""
grid_properties_dict = dict(
    {
        "axis": "both",
        "which": "major",
        "visible": True,
        "alpha": 0.8,
        "color": "#b3b3b3",
        "linestyle": "solid",
        "linewidth": 1,
        "dash_capstyle": "butt",
        "dash_joinstyle": "miter"
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
        "Transparency": {(x / 10): str((x / 10)) for x in range(1, 11)},
        "Color": create_color_dict(),
        "Style": dict(
            {
                "solid": "Solid (-)",
                "dashed": "Dashed (--)",
                "dashdot": "Dashdot (-.)",
                "dotted": "Dotted (..)"
            }
        ),
        "Width": {(x / 10): str((x / 10)) for x in range(1, 31)},
        "Cap style": dict(
            {
                "butt": "Butt",
                "round": "Round",
                "projecting": "Projecting"
            }
        ),
        "Join style": dict(
            {
                "miter": "Miter",
                "round": "Round",
                "bevel": "Bevel"
            }
        )
    }
)
"""
Dictionary mapping the key from the dictionary that it displayed in the GUI to the key from the dictionary that is passed
as **kwargs to the drawing function
"""
gird_properties_mapping_dict = {list(grid_properties_UI_dict.keys())[index]: list(grid_properties_dict.keys())[index]
                                for index in range(0, len(grid_properties_dict.keys()))}

ticks_properties_dict = dict(
    {
        "axis": "both",
        "which": "major",
        "visible": True,
        "direction": "out",
        "length": 4,
        "width": 1,
        "color": "#000000",
        "label": False,
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
        "Visibility": dict(
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
        "Ticks color": create_color_dict(),
        "Label": dict(
            {
                True: "Show",
                False: "Hide"
            }
        ),
        "Label-tick distance": {x: str(x) for x in range(1, 11)},
        "Label size": {x: str(x) for x in range(4, 21)},
        "Label color": create_color_dict(),
        "Label rotation": {x: str(x) for x in range(0, 360, 10)}
    }
)

ticks_properties_mapping_dict = {list(ticks_properties_UI_dict.keys())[index]: list(ticks_properties_dict.keys())[index]
                                for index in range(0, len(ticks_properties_dict.keys()))}

axes_properties_dict = dict(
    {
        "visible": True,
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
        "Visibility": dict(
            {
                True: "Show",
                False: "Hide"
            }
        ),
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
        "Background color": create_color_dict(),
        "X axis label": "x",
        "Y axis label": "y",
    }
)

axes_properties_mapping_dict = {list(axes_properties_UI_dict.keys())[index]: list(axes_properties_dict.keys())[index]
                                for index in range(0, len(axes_properties_dict.keys()))}

legend_properties_dict = dict(
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
        "scatterpoints": 1,
        #"prop": {"style": 'normal', "size": 'x-small'},     
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
        "Transparency": {(x / 10): str((x / 10)) for x in range(1, 11)},
        "Border color": create_color_dict(),
        "Background color": create_color_dict(),
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
        "Nr. of scatter points": {x: str(x) for x in range(1, 4)},
        #"prop": {SMALL_FONT: SMALL_FONT},
    }
)

legend_properties_mapping_dict = {list(legend_properties_UI_dict.keys())[index]: list(legend_properties_dict.keys())[index]
                                for index in range(0, len(legend_properties_dict.keys()))}