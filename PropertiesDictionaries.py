import numpy as np

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
            }),

        "Apply to lines for ": dict(
            {
                "minor": "Minor ticks",
                "major": "Major ticks",
                "both": "Both major and minor ticks"
            }),
        "Visibility": dict(
            {
                True: "Show",
                False: "Hide"
            }),
        "Transparency": {(x / 10): str((x / 10)) for x in range(1, 11)},
        "Color": create_color_dict(),
        "Style": dict(
            {
                "solid": "Solid (-)",
                "dashed": "Dashed (--)",
                "dashdot": "Dashdot (-.)",
                "dotted": "Dotted (..)"
            }),
        "Width": {(x / 10): str((x / 10)) for x in range(1, 31)},
        "Cap style": dict(
            {
                "butt": "Butt",
                "round": "Round",
                "projecting": "Projecting"
            }),
        "Join style": dict(
            {
                "miter": "Miter",
                "round": "Round",
                "bevel": "Bevel"
            })
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
        "direction": "out",
        "length": 4,
        "width": 1,
        "color": "#000000",
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
        "Ticks position": dict(
            {
                "in": "Inside the axes",
                "out": "Outside the axes",
                "inout": "Both inside and outside"
            }
        ),
        "Ticks length": {x: str(x) for x in range(0, 11)},
        "Ticks width": {x: str(x) for x in range(0, 11)},
        "Ticks color": create_color_dict(),
        "Label-tick distance": {x: str(x) for x in range(1, 11)},
        "Label size": {x: str(x) for x in range(0, 21)},
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
        #"path_effects": None,
        #"xbound": None,
        "xlabel": "x",
        #"xlim": None,
        #"ybound": None,
        "ylabel": "y",
        #"ylim": None,
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
        #"path_effects": None,
        #"Bound x axis (x1, x2)": None,
        "X axis label": "x",
        #"Limit x axis (x1, x2)": None,
        #"Bound y axis (y1, y2)": None,
        "Y axis label": "y",
        #"Limit y axis (y1, y2)": None,
    }
)

axes_properties_mapping_dict = {list(axes_properties_UI_dict.keys())[index]: list(axes_properties_dict.keys())[index]
                                for index in range(0, len(axes_properties_dict.keys()))}

legedn_properties_dict = dict(
    {
        "visible": True,
        
    }
)