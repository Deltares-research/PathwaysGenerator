from ...graph import SequenceGraph
from ...graph.node import Action as ActionNode
from ..colour import (
    Colour,
    Colours,
    PlotColours,
    default_edge_colours,
    default_label_colour,
    default_node_edge_colours,
    default_nominal_palette,
)


def colour_by_node(
    graph: SequenceGraph, colour_by_action_name: dict[str, Colour]
) -> Colours:
    # pylint: disable=redefined-outer-name
    colours = []

    for node in graph._graph.nodes:
        assert isinstance(node, ActionNode)
        assert node.action.name in colour_by_action_name, node.action
        colours.append(colour_by_action_name[node.action.name])

    return colours


def colour_by_action_name(graph: SequenceGraph, palette: Colours) -> dict[str, Colour]:
    palette_size = len(palette)
    result = {}

    idx = 0

    for node in graph._graph.nodes:
        assert isinstance(node, ActionNode)
        if node.action.name not in result:
            result[node.action.name] = palette[idx % palette_size]
            idx += 1

    return result


def default_node_colours(graph: SequenceGraph) -> Colours:
    colour_by_action_name_ = (
        graph.graph.graph["colour_by_action_name"]
        if "colour_by_action_name" in graph.graph.graph
        else colour_by_action_name(graph, default_nominal_palette())
    )

    return colour_by_node(graph, colour_by_action_name_)


def default_colours(sequence_graph: SequenceGraph) -> PlotColours:
    return PlotColours(
        default_node_colours(sequence_graph),
        default_edge_colours(sequence_graph),
        default_node_edge_colours(sequence_graph),
        default_label_colour(),
    )
