"""
This module contains code related to colours

Default colours are all taken from the `Nord theme palettes <https://www.nordtheme.com>`_.
"""

from dataclasses import dataclass

from ..graph import PathwayGraph, PathwayMap, SequenceGraph
from . import alias


@dataclass
class PlotColours:
    """
    This class aggregates colours used when plotting graphs

    :param node_colours: Fill colours for nodes
    :param node_style: Fill style for nodes
    :param edge_colours: Line colours for edges
    :param edge_style: Line style for edges
    :param node_edge_colours: Line colours for node outline
    :param label_colour: Label colour for labels
    """

    node_colours: list[alias.Colour | alias.Colours] | None = None
    node_style: alias.FillStyle | list[alias.FillStyle | alias.FillStyles] | None = None
    edge_colours: list[alias.Colour | alias.Colours] | None = None
    edge_style: alias.Style | list[alias.Style | alias.Styles] | None = None
    node_edge_colours: alias.Colours | None = None
    label_colour: alias.Colour | None = None


nord_palette_nominal = [
    (191 / 255, 97 / 255, 106 / 255, 1.0),  # Redish
    (208 / 255, 135 / 255, 112 / 255, 1.0),  # Orange
    (235 / 255, 203 / 255, 139 / 255, 1.0),  # Dark yellow
    (163 / 255, 190 / 255, 140 / 255, 1.0),  # Green
    (180 / 255, 142 / 255, 173 / 255, 1.0),  # Purple
    (143 / 255, 188 / 255, 187 / 255, 1.0),  # Calm, frozen polar water
]
"""
Colours to use for nominal values
"""


nord_palette_dark = [
    (46 / 255, 52 / 255, 64 / 255, 1.0),  # Dark
    (59 / 255, 66 / 255, 82 / 255, 1.0),  # Lighter than nord0
    (67 / 255, 76 / 255, 94 / 255, 1.0),  # Lighter than nord1
    (76 / 255, 86 / 255, 106 / 255, 1.0),  # Lighter than nord2
]
"""
Various shades of dark colours
"""


nord_palette_light = [
    (216 / 255, 222 / 255, 233 / 255, 1.0),  # Bright
    (229 / 255, 233 / 255, 240 / 255, 1.0),  # Lighter than nord4
    (236 / 255, 239 / 255, 244 / 255, 1.0),  # Lighter than nord5
]
"""
Various shades of light colours
"""


nord_palette_blue = [
    (143 / 255, 188 / 255, 187 / 255, 1.0),  # Calm, frozen polar water
    (136 / 255, 192 / 255, 208 / 255, 1.0),  # Bright, shiny, pure and clear ice
    (129 / 255, 161 / 255, 193 / 255, 1.0),  # Darkened, arctic waters
    (94 / 255, 129 / 255, 172 / 255, 1.0),  # Dark, deep arctic ocean
]
"""
Various shades of blue colours
"""


def default_nominal_palette() -> alias.Colours:
    """
    Return the default palette with nominal colours
    """
    return nord_palette_nominal


def default_edge_colours(
    graph: SequenceGraph | PathwayGraph,
) -> list[alias.Colour | alias.Colours]:
    """
    For each edge in the graph, return a colour
    """
    colour = nord_palette_dark[3]
    colours: list[alias.Colour | alias.Colours] = [colour] * len(
        list(graph.graph.edges)
    )

    return colours


def default_edge_style() -> alias.Style:
    """
    Return the default edge style
    """
    return "solid"


def default_node_edge_colours(
    graph: SequenceGraph | PathwayGraph | PathwayMap,
) -> alias.Colours:
    """
    For each edge in the graph, return a colour
    """
    colour = nord_palette_dark[3]
    colours = [colour] * len(list(graph.graph.edges))

    return colours


def default_node_colour() -> alias.Colour:
    """
    Return the default node colour
    """
    return nord_palette_dark[3]


def default_node_style() -> alias.FillStyle:
    """
    Return the default node style
    """
    return "full"


def default_label_colour() -> alias.Colour:
    """
    Return the default label colour
    """
    return nord_palette_dark[0]


def default_action_colours(nr_actions: int) -> alias.Colours:
    """
    For each action, return a colour
    """
    colours: alias.Colours = []

    while len(colours) < nr_actions:
        # Append the whole palette as many times as needed
        colours += default_nominal_palette()

    # Return the requested number of colours
    return colours[:nr_actions]


def rgba_to_hex(colour: alias.Colour) -> str:
    """
    Return the hex representation of the colour in RGBA representation
    """
    r = int(colour[0] * 255)
    g = int(colour[1] * 255)
    b = int(colour[2] * 255)
    a = int(colour[3] * 255)

    # argb format
    return f"#{a:02x}{r:02x}{g:02x}{b:02x}"


def hex_to_rgba(colour: str) -> alias.Colour:
    """
    Return the RGBA representation of the colour in hex representation
    """
    assert len(colour) == 9, colour
    assert colour[0] == "#", colour
    colour = colour[1:]
    argb = tuple(int(colour[i : i + 2], 16) for i in (0, 2, 4, 6))

    return argb[1] / 255.0, argb[2] / 255.0, argb[3] / 255.0, argb[0] / 255.0
