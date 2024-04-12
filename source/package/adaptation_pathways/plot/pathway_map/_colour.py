from ...graph import PathwayMap
from ...graph.node import ActionBegin, ActionEnd
from ..colour import (
    Colour,
    Colours,
    PlotColours,
    default_label_colour,
    default_node_edge_colours,
    default_nominal_palette,
)


def node_colours(
    graph: PathwayMap, colour_by_action_name: dict[str, Colour]
) -> Colours:
    colours = []

    # Colour each action begin / end combo unique

    for node in graph._graph.nodes:
        assert type(node) in [ActionBegin, ActionEnd]

        action = node.action
        colour = colour_by_action_name[action.name]

        colours.append(colour)

    return colours


def edge_colours(
    graph: PathwayMap, colour_by_action_name: dict[str, Colour]
) -> Colours:
    colours = []

    # Iterate over all edges and use the colour associated with the action associated with the edge
    for from_node, _ in graph._graph.edges:
        assert isinstance(from_node, (ActionBegin, ActionEnd)), from_node

        action = from_node.action
        colour = colour_by_action_name[action.name]

        colours.append(colour)

    return colours


def colour_by_action_name_pathway_map(
    graph: PathwayMap, palette: Colours
) -> dict[str, Colour]:
    palette_size = len(palette)
    colour_by_action_name = {}
    idx = 0

    for action in graph.actions():
        if action.name not in colour_by_action_name:
            colour_by_action_name[action.name] = palette[idx % palette_size]
            idx += 1

    return colour_by_action_name


def default_node_colours(graph: PathwayMap) -> Colours:
    colour_by_action_name = (
        graph.graph.graph["colour_by_action_name"]
        if "colour_by_action_name" in graph.graph.graph
        else colour_by_action_name_pathway_map(graph, default_nominal_palette())
    )

    return node_colours(graph, colour_by_action_name)


def default_edge_colours(graph: PathwayMap) -> Colours:
    colour_by_action_name = (
        graph.graph.graph["colour_by_action_name"]
        if "colour_by_action_name" in graph.graph.graph
        else colour_by_action_name_pathway_map(graph, default_nominal_palette())
    )

    return edge_colours(graph, colour_by_action_name)


def default_colours(pathway_map: PathwayMap) -> PlotColours:
    return PlotColours(
        default_node_colours(pathway_map),
        default_edge_colours(pathway_map),
        default_node_edge_colours(pathway_map),
        default_label_colour(),
    )
