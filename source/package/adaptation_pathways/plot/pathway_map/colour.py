from ...action_combination import ActionCombination
from ...graph import PathwayMap
from ...graph.node import ActionBegin, ActionEnd
from .. import alias
from ..colour import (
    PlotColours,
    default_edge_style,
    default_label_colour,
    default_node_edge_colours,
    default_node_style,
    default_nominal_palette,
)


def node_colours(
    graph: PathwayMap, colour_by_action_name: dict[str, alias.Colour]
) -> list[alias.Colour | alias.Colours]:
    colours: list[alias.Colour | alias.Colours] = []

    # Colour each action begin / end combo unique
    for node in graph._graph.nodes:
        assert isinstance(node, (ActionBegin, ActionEnd)), node

        action = node.action

        if isinstance(action, ActionCombination):
            # Multi-colour node
            colours.append(
                list(
                    colour_by_action_name[combined_action.name]
                    for combined_action in action.actions
                )
            )
        else:
            colours.append(colour_by_action_name[action.name])

    return colours


def edge_colours(
    graph: PathwayMap, colour_by_action_name: dict[str, alias.Colour]
) -> list[alias.Colour | alias.Colours]:
    colours: list[alias.Colour | alias.Colours] = []

    # Iterate over all edges and use the colour associated with the action associated with the edge
    for from_node, _ in graph._graph.edges:
        assert isinstance(from_node, (ActionBegin, ActionEnd)), from_node

        action = from_node.action

        if isinstance(from_node, ActionBegin) and isinstance(action, ActionCombination):
            # Multi-colour dash
            colours.append(
                list(
                    colour_by_action_name[combined_action.name]
                    for combined_action in action.actions
                )
            )
        else:
            colours.append(colour_by_action_name[action.name])

    return colours


def colour_by_action_name_pathway_map(
    graph: PathwayMap, palette: alias.Colours
) -> dict[str, alias.Colour]:
    palette_size = len(palette)
    colour_by_action_name = {}
    idx = 0

    for action in graph.actions():
        if action.name not in colour_by_action_name:
            colour_by_action_name[action.name] = palette[idx % palette_size]
            idx += 1

    return colour_by_action_name


def default_node_colours(graph: PathwayMap) -> list[alias.Colour | alias.Colours]:
    colour_by_action_name = (
        graph.graph.graph["colour_by_action_name"]
        if "colour_by_action_name" in graph.graph.graph
        else colour_by_action_name_pathway_map(graph, default_nominal_palette())
    )

    return node_colours(graph, colour_by_action_name)


def _node_style_by_action(
    graph: PathwayMap,
) -> dict[ActionBegin, alias.FillStyle | alias.FillStyles]:
    result: dict[ActionBegin, alias.FillStyle | alias.FillStyles] = {}

    for node in graph._graph.nodes:
        assert type(node) in (ActionBegin, ActionEnd), node
        assert not node in result, node
        action = node.action

        if isinstance(action, ActionCombination):
            # Multi-colour fill
            result[node] = len(action.actions) * ["bottom"]  # type: ignore[assignment]
        else:
            result[node] = default_node_style()

    return result


def node_styles(graph: PathwayMap) -> list[alias.FillStyle | alias.FillStyles]:
    styles_by_action_begin = _node_style_by_action(graph)
    styles: list[alias.FillStyle | alias.FillStyles] = []

    for node in graph._graph.nodes:
        styles.append(styles_by_action_begin[node])

    return styles


def default_node_styles(graph: PathwayMap) -> list[alias.FillStyle | alias.FillStyles]:
    """
    For each node in the graph, return a style
    """
    return node_styles(graph)


def default_edge_colours(graph: PathwayMap) -> list[alias.Colour | alias.Colours]:
    colour_by_action_name = (
        graph.graph.graph["colour_by_action_name"]
        if "colour_by_action_name" in graph.graph.graph
        else colour_by_action_name_pathway_map(graph, default_nominal_palette())
    )

    return edge_colours(graph, colour_by_action_name)


def _styles_by_action_begin(
    graph: PathwayMap,
) -> dict[ActionBegin, alias.Style | alias.Styles]:
    result: dict[ActionBegin, alias.Style | alias.Styles] = {}

    for from_node, _ in graph._graph.edges:
        assert type(from_node) in [ActionBegin, ActionEnd], from_node

        if isinstance(from_node, ActionBegin):
            assert not from_node in result
            action = from_node.action

            if isinstance(action, ActionCombination):
                # Multi-colour dash
                result[from_node] = list(
                    (2 * idx, (2, 2)) for idx in range(len(action.actions))
                )
            else:
                result[from_node] = default_edge_style()

    return result


def edge_styles(graph: PathwayMap) -> list[alias.Style | alias.Styles]:
    """
    For each edge in the graph, return a style
    """
    styles_by_action_begin = _styles_by_action_begin(graph)
    styles: list[alias.Style | alias.Styles] = []

    for from_node, _ in graph._graph.edges:
        assert isinstance(from_node, (ActionBegin, ActionEnd)), from_node

        if isinstance(from_node, ActionBegin):
            styles.append(styles_by_action_begin[from_node])
        else:
            styles.append(default_edge_style())

    return styles


def default_edge_styles(graph: PathwayMap) -> list[alias.Style | alias.Styles]:
    return edge_styles(graph)


def default_colours(pathway_map: PathwayMap) -> PlotColours:
    return PlotColours(
        default_node_colours(pathway_map),
        default_node_styles(pathway_map),
        default_edge_colours(pathway_map),
        default_edge_styles(pathway_map),
        default_node_edge_colours(pathway_map),
        default_label_colour(),
    )
