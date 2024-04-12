from dataclasses import dataclass

from ..graph import PathwayGraph, PathwayMap, SequenceGraph


Colour = tuple[float, float, float, float]
Colours = list[Colour]


@dataclass
class PlotColours:
    node_colours: Colours | None = None
    edge_colours: Colours | None = None
    node_edge_colours: Colours | None = None
    label_colour: Colour | None = None


nord_palette_nominal = [
    (191 / 255, 97 / 255, 106 / 255, 1.0),  # Redish
    (208 / 255, 135 / 255, 112 / 255, 1.0),  # Orange
    (235 / 255, 203 / 255, 139 / 255, 1.0),  # Dark yellow
    (163 / 255, 190 / 255, 140 / 255, 1.0),  # Green
    (180 / 255, 142 / 255, 173 / 255, 1.0),  # Purple
]

nord_palette_dark = [
    (46 / 255, 52 / 255, 64 / 255, 1.0),  # Dark
    (59 / 255, 66 / 255, 82 / 255, 1.0),  # Lighter than nord0
    (67 / 255, 76 / 255, 94 / 255, 1.0),  # Lighter than nord1
    (76 / 255, 86 / 255, 106 / 255, 1.0),  # Lighter than nord2
]

nord_palette_light = [
    (216 / 255, 222 / 255, 233 / 255, 1.0),  # Bright
    (229 / 255, 233 / 255, 240 / 255, 1.0),  # Lighter than nord4
    (236 / 255, 239 / 255, 244 / 255, 1.0),  # Lighter than nord5
]

nord_palette_blue = [
    (143 / 255, 188 / 255, 187 / 255, 1.0),  # Calm, frozen polar water
    (136 / 255, 192 / 255, 208 / 255, 1.0),  # Bright, shiny, pure and clear ice
    (129 / 255, 161 / 255, 193 / 255, 1.0),  # Darkened, arctic waters
    (94 / 255, 129 / 255, 172 / 255, 1.0),  # Dark, deep arctic ocean
]


def default_nominal_palette() -> Colours:
    palette = nord_palette_nominal
    palette.append(nord_palette_blue[0])

    return palette


def default_edge_colours(
    graph: SequenceGraph | PathwayGraph,
) -> Colours:
    colour = nord_palette_dark[3]
    colours = [colour] * len(list(graph.graph.edges))

    return colours


def default_node_edge_colours(
    graph: SequenceGraph | PathwayGraph | PathwayMap,
) -> Colours:
    colour = nord_palette_dark[3]
    colours = [colour] * len(list(graph.graph.edges))

    return colours


def default_node_colour() -> Colour:
    return nord_palette_dark[3]


def default_label_colour() -> Colour:
    return nord_palette_dark[0]


def default_action_colours(nr_actions: int) -> Colours:
    colours: Colours = []

    while len(colours) < nr_actions:
        colours += default_nominal_palette()

    return colours[:nr_actions]


def rgba_to_hex(colour: Colour) -> str:
    r = int(colour[0] * 255)
    g = int(colour[1] * 255)
    b = int(colour[2] * 255)
    a = int(colour[3] * 255)

    # argb format
    return f"#{a:02x}{r:02x}{g:02x}{b:02x}"


def hex_to_rgba(colour: str) -> Colour:
    assert len(colour) == 9, colour
    assert colour[0] == "#", colour
    colour = colour[1:]
    argb = tuple(int(colour[i : i + 2], 16) for i in (0, 2, 4, 6))

    return argb[1] / 255.0, argb[2] / 255.0, argb[3] / 255.0, argb[0] / 255.0
