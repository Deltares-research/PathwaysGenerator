import math
from collections.abc import Iterable

import matplotlib as mpl
import numpy as np

from ...action import Action
from ...action_combination import ActionCombination
from ...graph import PathwayMap
from ...graph.node import ActionBegin, Node
from .. import alias
from ..colour import PlotColours
from ..util import add_position
from .colour import default_colours


# pylint: disable=too-many-arguments
def _draw_edges(
    axes,
    pathway_map,
    layout,
    edge_colours,
    edge_style: list[alias.Style | alias.Styles],
    edge_list=None,
    node_list=None,
) -> mpl.collections.LineCollection:

    if edge_list is None:
        edge_list = list(pathway_map.graph.edges())

    if len(edge_list) == 0:
        return mpl.collections.LineCollection([])

    if node_list is None:
        node_list = list(pathway_map.graph.nodes())

    edge_pos = [(layout[e[0]], layout[e[1]]) for e in edge_list]

    # The edge styles passed in may contain lists of styles. In that case, records for all
    # per-edge collections must be duplicated.
    if isinstance(edge_style, Iterable):
        expansions = []
        for idx, style in enumerate(edge_style):
            if not isinstance(style, str) and isinstance(style, Iterable):
                expansions.append((idx, len(style)))

        # Duplicate by iterating from last to first expansion
        expansions.reverse()

        for idx, count in expansions:
            edge_pos[idx : idx + 1] = count * [edge_pos[idx]]
            if not isinstance(edge_colours[idx], tuple) and isinstance(
                edge_colours[idx], Iterable
            ):
                assert len(edge_colours[idx]) == count, "Not enough colours for styles"
                edge_colours[idx : idx + 1] = edge_colours[idx]
            else:
                edge_colours[idx : idx + 1] = count * [edge_colours[idx]]
            edge_style[idx : idx + 1] = edge_style[idx]  # type: ignore[assignment]

    edge_pos = np.asarray(edge_pos)

    edge_collection = mpl.collections.LineCollection(
        edge_pos,
        colors=edge_colours,
        linestyle=edge_style,
        antialiaseds=(1,),
    )
    edge_collection.set_zorder(1)  # edges go behind nodes
    axes.add_collection(edge_collection)

    return edge_collection


def _draw_nodes(
    axes,
    pathway_map,
    layout,
    node_colours,
    node_style: list[alias.FillStyle | alias.FillStyles],
    node_list=None,
) -> mpl.collections.PathCollection:

    if node_list is None:
        node_list = list(pathway_map.graph)

    if len(node_list) == 0:
        return mpl.collections.PathCollection(None)

    node_pos = np.asarray([layout[v] for v in node_list])

    # Unfortunately, scatter doesn't seem to support passing in marker properties that change
    # per symbol
    # node_collection = axes.scatter(
    #     node_pos[:, 0],
    #     node_pos[:, 1],
    #     c=node_colours,
    # )

    # Not sure how to build a PathCollection from individual plot commands. Do we need to?
    node_collection = mpl.collections.PathCollection(None)

    for idx, pos in enumerate(node_pos):
        if node_style[idx] == "full":
            axes.plot(
                pos[0],
                pos[1],
                marker="o",
                fillstyle="full",
                color=node_colours[idx],
                markeredgecolor="none",
            )
        else:
            assert len(node_colours[idx]) == 2, "Only two colours supported ATM"
            axes.plot(
                pos[0],
                pos[1],
                marker="o",
                fillstyle="bottom",
                markerfacecolor=node_colours[idx][0],
                markerfacecoloralt=node_colours[idx][1],
                markeredgecolor="none",
            )

    node_collection.set_zorder(2)

    return node_collection


def _hide_spines(axes):
    axes.spines.top.set_visible(False)
    axes.spines.right.set_visible(False)
    axes.spines.bottom.set_visible(False)
    axes.spines.left.set_visible(False)


def _update_data_limits(axes, coordinates):
    min_x, min_y = np.min(coordinates, 0)
    max_x, max_y = np.max(coordinates, 0)
    width = max_x - min_x
    height = max_y - min_y
    pad_x = 0.05 * width
    pad_y = 0.05 * height
    corners = (min_x - pad_x, min_y - pad_y), (max_x + pad_x, max_y + pad_y)

    axes.update_datalim(corners)


def _configure_axes(axes, pathway_map, layout, title, plot_colours) -> None:
    # pylint: disable=too-many-locals
    if len(title) > 0:
        axes.set_title(title)

    axes.tick_params(
        left=False,
        bottom=False,
    )
    axes.set_xlabel("time")

    actions = pathway_map.actions()
    action_names = [action.name for action in actions]

    y_labels = []
    y_coordinates = []
    label_colours = []
    action_by_y_coordinate: dict[float, set[Action]] = {}
    colour_by_action: dict[Action, alias.Colour] = {}

    # Action combinations that continue a single action end up at the same y-coordinate as
    # the action which they continue. Coordinates and labels for only these specific combinations
    # must be sieved out of the collections.
    for action_name in action_names:
        for idx, action_node in enumerate(layout):
            if action_node.action.name == action_name:
                y_coordinate = layout[action_node][1]
                action_by_y_coordinate.setdefault(y_coordinate, set()).add(
                    action_node.action
                )
                colour_by_action[action_node.action] = plot_colours.node_colours[idx]

    for y_coordinate, actions in action_by_y_coordinate.items():
        assert len(actions) > 0

        regular_actions = [
            action for action in actions if not isinstance(action, ActionCombination)
        ]

        if len(actions) > 1 and len(regular_actions) > 0:
            # Combination of regular actions and action combinations at same y-coordinate
            # Use regular action for label and colour
            action = next(iter(regular_actions))
        else:
            # Only a single action or only multiple action combinations at same y-coordinate
            # Use first action for label and colour
            action = next(iter(actions))

        y_coordinates.append(y_coordinate)
        y_labels.append(action.name)
        label_colours.append(colour_by_action[action])

    axes.set_yticks(y_coordinates, labels=y_labels)

    for colour, tick in zip(label_colours, axes.yaxis.get_major_ticks()):
        tick.label1.set_color(colour)

    _hide_spines(axes)

    if len(layout) > 0:
        coordinates = np.concatenate(list(layout.values())).reshape(len(layout), 2)
        _update_data_limits(axes, coordinates)

        x_ticks = axes.get_xticks()

        if len(x_ticks) > 0:
            x_ticks = x_ticks[1:]

        x_labels = [f"{int(tick)}" for tick in x_ticks]
        axes.set_xticks(x_ticks, labels=x_labels)

    axes.autoscale_view()


def classic_pathway_map_plotter(
    axes,
    pathway_map,
    layout,
    title,
    plot_colours,
) -> tuple[mpl.collections.LineCollection, mpl.collections.PathCollection]:

    edge_artist = _draw_edges(
        axes, pathway_map, layout, plot_colours.edge_colours, plot_colours.edge_style
    )
    node_artist = _draw_nodes(
        axes, pathway_map, layout, plot_colours.node_colours, plot_colours.node_style
    )

    _configure_axes(axes, pathway_map, layout, title, plot_colours)

    # Return the result(s) of a plot function(s) (artists?)
    return edge_artist, node_artist


def _distribute_horizontally(
    pathway_map: PathwayMap,
    action_begin: ActionBegin,
    position_by_node: dict[Node, np.ndarray],
) -> None:
    assert isinstance(action_begin, ActionBegin)

    action_end = pathway_map.action_end(action_begin)
    end_x = action_end.tipping_point

    add_position(position_by_node, action_end, (end_x, np.nan))

    for action_begin_new in pathway_map.action_begins(
        pathway_map.action_end(action_begin)
    ):
        begin_x = end_x

        add_position(position_by_node, action_begin_new, (begin_x, np.nan))
        _distribute_horizontally(pathway_map, action_begin_new, position_by_node)


# pylint: disable-next=too-many-locals, too-many-branches
def _distribute_vertically(
    pathway_map: PathwayMap,
    root_action_begin: ActionBegin,
    position_by_node: dict[Node, np.ndarray],
) -> None:

    action_end = pathway_map.action_end(root_action_begin)
    position_by_node[action_end][1] = position_by_node[root_action_begin][1]

    # min_distance = 1.0

    # All unique action instances in the graph
    actions = pathway_map.actions()

    # Sieve out combined actions that combine a single *existing* action with a *new* one. These
    # must be positioned at the same y-coordinate as the existing action. These combined actions
    # must not interfere with the distribution of y-coordinates.

    # Sieve out actions that only differ with respect to the edition. These must be positioned
    # at the same y-coordinate and must not interfere with the distribution of y-coordinates.

    action_combinations_sieved: dict[ActionCombination, Action] = {}
    action_combinations_continuations: dict[ActionCombination, list[Action]] = {}
    names_of_actions_to_distribute: list[str] = []

    for action in actions:
        if not isinstance(action, ActionCombination):
            if action.name not in names_of_actions_to_distribute:
                names_of_actions_to_distribute.append(action.name)
        else:
            continued_actions = pathway_map.continued_actions(action)

            if len(continued_actions) == 1:
                # Action is a combination of a single existing action with a new one
                action_combinations_sieved[action] = continued_actions[0]
            else:
                if len(continued_actions) > 1:
                    action_combinations_continuations[action] = continued_actions

                if action.name not in names_of_actions_to_distribute:
                    names_of_actions_to_distribute.append(action.name)

    # We now have the names of the actions to distribute. What is important here is that the
    # number of actions is correct.
    y_coordinates = list(
        range(
            math.floor(len(names_of_actions_to_distribute) / 2),
            -math.floor((len(names_of_actions_to_distribute) - 1) / 2) - 1,
            -1,
        )
    )

    # Nodes related to the root action are already positioned
    # Delete the y-coordinate of the root action
    assert y_coordinates[math.floor(len(names_of_actions_to_distribute) / 2)] == 0.0
    del y_coordinates[math.floor(len(names_of_actions_to_distribute) / 2)]

    # Delete the name of the root action
    assert (
        names_of_actions_to_distribute[0] == root_action_begin.action.name
    ), names_of_actions_to_distribute[0]
    del names_of_actions_to_distribute[0]

    # Now it is time to re-order the actions to distribute, based on their level, if any was set
    level_by_action = (
        pathway_map.graph.graph["level_by_action"]
        if "level_by_action" in pathway_map.graph.graph
        else {}
    )

    # Update the levels of action combinations that continue multiple existing actions. These
    # must end up somewhere in between the continued actions.
    if level_by_action:
        for action, continued_actions in action_combinations_continuations.items():
            assert action in level_by_action
            level_by_action[action] = sum(
                level_by_action[action] for action in continued_actions
            ) / len(continued_actions)

    levels_of_actions_to_distribute = []

    for action_name in names_of_actions_to_distribute:
        level = next(
            (
                level_by_action[action]
                for action in actions
                if action.name == action_name and action in level_by_action
            ),
            0,
        )
        levels_of_actions_to_distribute.append(level)

    # Sort action names based on their individual level. Actions with lower levels must end up
    # higher in the pathway map.
    levels_of_actions_to_distribute, names_of_actions_to_distribute = (
        list(t)
        for t in zip(
            *sorted(
                zip(levels_of_actions_to_distribute, names_of_actions_to_distribute)
            )
        )
    )

    y_coordinate_by_action = dict(zip(names_of_actions_to_distribute, y_coordinates))
    # y_coordinate_by_action[root_action_begin.action.name] = 0

    for action_begin in pathway_map.all_action_begins()[1:]:  # Skip root node
        action = action_begin.action

        if (
            isinstance(action, ActionCombination)
            and action in action_combinations_sieved
        ):
            # In this case we want the combination to end up at the same y-coordinate as the
            # one action that is being continued
            action = action_combinations_sieved[action]

        y_coordinate = y_coordinate_by_action[action.name]

        assert np.isnan(position_by_node[action_begin][1])
        position_by_node[action_begin][1] = y_coordinate
        action_end = pathway_map.action_end(action_begin)

        assert np.isnan(position_by_node[action_end][1])
        position_by_node[action_end][1] = y_coordinate


def _layout(
    pathway_map: PathwayMap,
) -> dict[Node, np.ndarray]:
    """
    Layout that replicates the pathway map layout of the original (pre-2024) pathway generator

    :param pathway_map: Pathway map
    :return: Node positions

    The layout has the following characteristics:

    - A pathway map is a stack of horizontal lines representing actions
    - Each action ends up at its own level in the stack
    - Pathways jump from horizontal line to horizontal line, depending on the sequences of
      actions that make up each pathway

    The pathway map passed in must contain sane tipping points. When in doubt, call
    ``verify_tipping_points()`` before calling this function.

    The graph in the pathway map passed in must contain an attribute called "level_by_action",
    with a numeric value per action, which corresponds with the position in the above mentioned
    stack.  Low numbers correspond with a high position in the stack (large y-coordinate). Such
    actions will be positioned at the top of the pathway map.
    """
    position_by_node: dict[Node, np.ndarray] = {}

    if pathway_map.nr_edges() > 0:
        root_action_begin = pathway_map.root_node
        root_action_end = pathway_map.action_end(root_action_begin)
        tipping_point = root_action_end.tipping_point

        min_tipping_point, max_tipping_point = pathway_map.tipping_point_range()
        tipping_point_range = max_tipping_point - min_tipping_point
        assert tipping_point_range >= 0
        x_coordinate = tipping_point - 0.1 * tipping_point_range

        add_position(position_by_node, root_action_begin, (x_coordinate, 0))

        _distribute_horizontally(pathway_map, root_action_begin, position_by_node)
        _distribute_vertically(pathway_map, root_action_begin, position_by_node)

    return position_by_node


def plot(
    axes: mpl.axes.Axes,
    pathway_map: PathwayMap,
    title: str = "",
    plot_colours: PlotColours | None = None,
) -> None:
    if plot_colours is None:
        plot_colours = default_colours(pathway_map)

    classic_pathway_map_plotter(
        axes, pathway_map, _layout(pathway_map), title, plot_colours
    )
