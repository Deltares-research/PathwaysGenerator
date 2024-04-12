import math

import matplotlib as mpl
import numpy as np

from ...action import Action
from ...action_combination import ActionCombination
from ...graph import PathwayMap
from ...graph.node import ActionBegin, Node
from ..colour import PlotColours
from ..util import add_position
from ._colour import default_colours


# pylint: disable=too-many-arguments
def _draw_edges(
    axes,
    pathway_map,
    layout,
    edge_colours,
    edge_list=None,
    node_list=None,
) -> mpl.collections.LineCollection:
    # The default behavior is to use LineCollection to draw edges for
    # undirected graphs (for performance reasons) and use FancyArrowPatches
    # for directed graphs.
    # The `arrows` keyword can be used to override the default behavior
    ### use_linecollection = not pathway_map.graph.is_directed()
    ### if arrows in (True, False):
    ###     use_linecollection = not arrows

    ### # Some kwargs only apply to FancyArrowPatches. Warn users when they use
    ### # non-default values for these kwargs when LineCollection is being used
    ### # instead of silently ignoring the specified option
    ### if use_linecollection and any(
    ###     [
    ###         arrowstyle is not None,
    ###         arrowsize != 10,
    ###         connectionstyle != "arc3",
    ###         min_source_margin != 0,
    ###         min_target_margin != 0,
    ###     ]
    ### ):
    ###     import warnings

    ###     msg = (
    ###         "\n\nThe {0} keyword argument is not applicable when drawing edges\n"
    ###         "with LineCollection.\n\n"
    ###         "To make this warning go away, either specify `arrows=True` to\n"
    ###         "force FancyArrowPatches or use the default value for {0}.\n"
    ###         "Note that using FancyArrowPatches may be slow for large graphs.\n"
    ###     )
    ###     if arrowstyle is not None:
    ###         msg = msg.format("arrowstyle")
    ###     if arrowsize != 10:
    ###         msg = msg.format("arrowsize")
    ###     if connectionstyle != "arc3":
    ###         msg = msg.format("connectionstyle")
    ###     if min_source_margin != 0:
    ###         msg = msg.format("min_source_margin")
    ###     if min_target_margin != 0:
    ###         msg = msg.format("min_target_margin")
    ###     warnings.warn(msg, category=UserWarning, stacklevel=2)

    ### if arrowstyle == None:
    ###     if pathway_map.graph.is_directed():
    ###         arrowstyle = "-|>"
    ###     else:
    ###         arrowstyle = "-"
    # arrowstyle = "-|>"

    if edge_list is None:
        edge_list = list(pathway_map.graph.edges())

    if len(edge_list) == 0:  # no edges!
        return mpl.collections.LineCollection([])

    if node_list is None:
        node_list = list(pathway_map.graph.nodes())

    # FancyArrowPatch handles color=None different from LineCollection
    if edge_colours is None:
        # edge_colours = "k"
        pass
    # edgelist_tuple = list(map(tuple, edge_list))

    # set edge positions
    edge_pos = np.asarray([(layout[e[0]], layout[e[1]]) for e in edge_list])

    # # Check if edge_colours is an array of floats and map to edge_cmap.
    # # This is the only case handled differently from matplotlib
    # if (
    #     np.iterable(edge_colours)
    #     and (len(edge_colours) == len(edge_pos))
    #     and np.all([isinstance(c, Number) for c in edge_colours])
    # ):
    #     if edge_cmap is not None:
    #         assert isinstance(edge_cmap, mpl.colors.Colormap)
    #     else:
    #         edge_cmap = plt.get_cmap()
    #     if edge_vmin is None:
    #         edge_vmin = min(edge_colours)
    #     if edge_vmax is None:
    #         edge_vmax = max(edge_colours)
    #     color_normal = mpl.colors.Normalize(vmin=edge_vmin, vmax=edge_vmax)
    #     edge_colours = [edge_cmap(color_normal(e)) for e in edge_colours]

    def _draw_networkx_edges_line_collection():
        edge_collection = mpl.collections.LineCollection(
            edge_pos,
            colors=edge_colours,
            antialiaseds=(1,),
            # linestyle=style,
            # alpha=alpha,
        )
        # edge_collection.set_cmap(edge_cmap)
        # edge_collection.set_clim(edge_vmin, edge_vmax)
        edge_collection.set_zorder(1)  # edges go behind nodes
        # edge_collection.set_label(label)
        axes.add_collection(edge_collection)

        return edge_collection

    # Draw the edges
    edge_viz_obj = _draw_networkx_edges_line_collection()

    return edge_viz_obj


def _draw_nodes(
    axes,
    pathway_map,
    layout,
    node_colours,
    node_list=None,
) -> mpl.collections.PathCollection:
    if node_list is None:
        node_list = list(pathway_map.graph)

    if len(node_list) == 0:  # empty node_list, no drawing
        return mpl.collections.PathCollection(None)

    try:
        xy = np.asarray([layout[v] for v in node_list])
    except KeyError as exception:
        raise RuntimeError(f"Node {exception} has no position.") from exception

    node_collection = axes.scatter(
        xy[:, 0],
        xy[:, 1],
        c=node_colours,
    )

    # TODO What is this?
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


def _configure_axes(axes, pathway_map, layout, title, plot_colours):
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

    labels = []
    y_coordinates = []
    label_colours = []
    is_action_combination = []
    y_coordinates_of_regular_actions = []

    # Action combinations that continue a single action end up at the same y-coordinate as
    # the action which they continue. Coordinates and labels for only these specific combinations
    # must be sieved out of the collections.
    for action_name in action_names:
        for idx, action_node in enumerate(layout):
            if action_node.action.name == action_name:
                y_coordinate = layout[action_node][1]
                colour = plot_colours.node_colours[idx]

                labels.append(action_name)
                y_coordinates.append(y_coordinate)
                label_colours.append(colour)

                is_action_combination.append(
                    isinstance(action_node.action, ActionCombination)
                )
                if not isinstance(action_node.action, ActionCombination):
                    y_coordinates_of_regular_actions.append(y_coordinate)

    # Sieve out the information for those action combinations that continue a single action

    # sieve = [
    #     is_action_combination[idx]
    #     and y_coordinates_of_regular_actions.count([y_coordinates[idx]]) > 0
    #     for idx in range(len(y_coordinates))
    # ]
    # y_coordinates = [
    #     y_coordinates[idx] for idx in range(len(y_coordinates)) if not sieve[idx]
    # ]
    # labels = [labels[idx] for idx in range(len(labels)) if not sieve[idx]]
    # label_colours = [
    #     label_colours[idx] for idx in range(len(label_colours)) if not sieve[idx]
    # ]

    axes.set_yticks(y_coordinates, labels=labels)

    for colour, tick in zip(label_colours, axes.yaxis.get_major_ticks()):
        tick.label1.set_color(colour)

    _hide_spines(axes)

    if len(layout) > 0:
        _update_data_limits(
            axes,
            coordinates=np.concatenate(list(layout.values())).reshape(len(layout), 2),
        )

    axes.autoscale_view()


def classic_pathway_map_plotter(
    axes,
    pathway_map,
    layout,
    title,
    plot_colours,
) -> tuple[mpl.collections.LineCollection, mpl.collections.PathCollection]:
    # TODO
    # - Get rid of the frames
    # - Transparent background
    # - Support dashed lines when multiple colours are passed for an edge
    # - Understand size and scale of plot + coordinates

    # Once we understand plotting with matplotlib, adjust the layout of parallel pathways. They
    # need to be separated a bit vertically.
    # - Use existing distribute function, center around Action's y-coordinate

    edge_artist = _draw_edges(axes, pathway_map, layout, plot_colours.edge_colours)
    node_artist = _draw_nodes(axes, pathway_map, layout, plot_colours.node_colours)

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
