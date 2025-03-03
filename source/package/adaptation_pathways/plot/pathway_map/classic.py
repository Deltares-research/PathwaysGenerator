import math
import typing

import matplotlib as mpl
import matplotlib.lines as mlines
import matplotlib.markers as mmarkers
import numpy as np

from ...action import Action
from ...action_combination import ActionCombination
from ...alias import TippingPointByAction
from ...graph import PathwayMap, tipping_point_range
from ...graph.node import ActionBegin, ActionEnd
from ..alias import (
    ColourByActionName,
    LevelByActionName,
    MarkerByActionName,
    MarkerStyle,
    PositionByNode,
    Region,
)
from ..colour import default_nominal_palette
from ..plot import configure_title, y_axis_blended_to_data
from ..util import (
    action_level_by_first_occurrence,
    add_position,
    distribute,
    group_overlapping_regions_with_payloads,
)
from .colour import colour_by_action_name_pathway_map


def _plot_action_lines(
    axes,
    pathway_map,
    layout: PositionByNode,
    *,
    colour_by_action_name,
    tipping_point_overshoot,
) -> mpl.collections.LineCollection:

    edge_nodes = list(pathway_map.graph.edges())
    edge_collection = mpl.collections.LineCollection([])

    if len(edge_nodes) > 0:
        edges = np.asarray([(layout[edge[0]], layout[edge[1]]) for edge in edge_nodes])

        # Each edge consists of a start and end point. In case the y-coordinate of both points is the same,
        # then the end point corresponds with a tipping point. The x-coordinate of this point must be tweaked,
        # given the tipping_point_overshoot passed in.

        for edge in edges:
            if edge[0][1] == edge[1][1]:
                edge[1][0] += tipping_point_overshoot

        colours = [colour_by_action_name[edge[0].action.name] for edge in edge_nodes]

        edge_collection = mpl.collections.LineCollection(
            edges,
            colors=colours,
        )
        axes.add_collection(edge_collection)

    return edge_collection


def _plot_action_starts(
    axes,
    pathway_map,
    layout: PositionByNode,
    *,
    colour_by_action_name,
    start_action_marker,
) -> mpl.collections.PathCollection:

    nodes = pathway_map.all_action_begins()
    path_collection = mpl.collections.PathCollection(None)

    if len(nodes) > 0:
        node_pos = np.asarray([layout[node] for node in nodes])
        x, y = zip(*node_pos)
        colours = [colour_by_action_name[node.action.name] for node in nodes]
        path_collection = axes.scatter(x, y, marker=start_action_marker, c=colours)

    return path_collection


def _plot_action_tipping_points(
    axes,
    pathway_map,
    layout: PositionByNode,
    *,
    colour_by_action_name,
    tipping_point_face_colour,
    tipping_point_marker,
    tipping_point_overshoot,
) -> mpl.collections.PathCollection:

    nodes = pathway_map.all_action_ends()
    path_collection = mpl.collections.PathCollection(None)

    if len(nodes) > 0:
        # TODO Skip the tipping point at the end of each individual path way
        node_pos = np.asarray([layout[v] for v in nodes])
        x, y = zip(*node_pos)
        x = np.array(x) + tipping_point_overshoot
        colours = [colour_by_action_name[node.action.name] for node in nodes]

        if tipping_point_marker.is_filled():
            scatter_arguments = {
                "edgecolor": colours,
                "facecolor": tipping_point_face_colour,
            }
        else:
            scatter_arguments = {
                "facecolor": colours,
            }

        path_collection = axes.scatter(
            x, y, marker=tipping_point_marker, **scatter_arguments
        )

    return path_collection


def _configure_y_axes(
    axes,
    y_coordinate_by_action_name: dict[str, float],
    *,
    colour_by_action_name,
    marker_by_action_name: MarkerByActionName,
    marker_style: MarkerStyle,
    use_markers_as_yticks: bool,
):

    # Left y-axis
    axes.spines.left.set_visible(False)
    axes.tick_params(left=False)

    y_labels = list(y_coordinate_by_action_name.keys())

    if use_markers_as_yticks:
        axes.set_yticks(list(y_coordinate_by_action_name.values()), labels="")

        label_colours = [colour_by_action_name[label] for label in y_labels]
        markers = [marker_by_action_name[label] for label in y_labels]

        min_x, max_x = axes.get_xlim()
        x_range = max_x - min_x
        x_offset = 0.01 * x_range  # TODO Heuristic we may want to improve

        for idx, y_tick in enumerate(axes.get_yticklabels()):
            x_coordinate, y_coordinate = y_axis_blended_to_data(
                axes, y_tick.get_position()
            )

            artist = mlines.Line2D(
                [x_coordinate - x_offset],
                [y_coordinate],
                marker=markers[idx],
                color="none",
                markeredgecolor=label_colours[idx],
                clip_on=False,
                **marker_style,
            )
            axes.add_artist(artist)

    # Right y-axis
    axes.spines.right.set_visible(False)

    return y_labels


def _configure_x_axes(
    axes,
    layout: PositionByNode,
    *,
    x_label,
):

    # Top x-axis
    axes.spines.top.set_visible(False)

    # Bottom x-axis
    axes.spines.bottom.set_visible(True)
    axes.tick_params(bottom=True)
    axes.set_xlabel(x_label)

    if len(layout) > 0:
        # TODO Still needed?
        # coordinates = np.concatenate(list(layout.values())).reshape(len(layout), 2)
        # _update_data_limits(axes, coordinates)

        x_ticks = axes.get_xticks()

        if len(x_ticks) > 0:
            x_ticks = x_ticks[1:]

        x_labels = [f"{int(tick)}" for tick in x_ticks]
        axes.set_xticks(x_ticks, labels=x_labels)


def _configure_legend(
    axes,
    *,
    action_names,
    colour_by_action_name: ColourByActionName,
    level_by_action_name: LevelByActionName,
    marker_by_action_name: MarkerByActionName,
    marker_style: MarkerStyle,
    arguments,
):

    # Iterate over all actions that are shown on the y-axis. For each of these create a proxy artist. Then
    # create the legend, passing in the proxy artists.
    # Take the level by action into account.

    action_names = sorted(
        list(action_names), key=lambda action_name: level_by_action_name[action_name]
    )

    handles = []

    for action_name in action_names:
        handles.append(
            mlines.Line2D(
                [],
                [],
                label=action_name,
                marker=marker_by_action_name[action_name],
                color="none",
                markeredgecolor=colour_by_action_name[action_name],
                **marker_style,
            )
        )

    axes.legend(handles=handles, **arguments)


def _plot_annotations(
    axes,
    layout: PositionByNode,
    y_coordinate_by_action_name: dict[str, float],
    *,
    colour_by_action_name: ColourByActionName,
    level_by_action_name: LevelByActionName,
    marker_by_action_name: MarkerByActionName,
    marker_style: MarkerStyle,
    show_legend: bool,
    title: str,
    use_markers_as_yticks: bool,
    x_label: str,
    legend_arguments: dict[str, typing.Any],
) -> None:

    configure_title(axes, title=title)
    y_labels = _configure_y_axes(
        axes,
        y_coordinate_by_action_name,
        colour_by_action_name=colour_by_action_name,
        marker_by_action_name=marker_by_action_name,
        marker_style=marker_style,
        use_markers_as_yticks=use_markers_as_yticks,
    )
    _configure_x_axes(
        axes,
        layout,
        x_label=x_label,
    )

    if show_legend:
        _configure_legend(
            axes,
            action_names=y_labels,
            colour_by_action_name=colour_by_action_name,
            level_by_action_name=level_by_action_name,
            marker_by_action_name=marker_by_action_name,
            marker_style=marker_style,
            arguments=legend_arguments,
        )


# pylint: disable-next=too-many-arguments
def classic_pathway_map_plotter(
    axes,
    pathway_map,
    layout: PositionByNode,
    y_coordinate_by_action_name: dict[str, float],
    *,
    colour_by_action_name,
    level_by_action_name: LevelByActionName,
    marker_by_action_name: MarkerByActionName,
    marker_style: MarkerStyle,
    show_legend,
    start_action_marker,
    tipping_point_face_colour,
    tipping_point_marker,
    tipping_point_overshoot,
    title,
    use_markers_as_yticks: bool,
    x_label,
    legend_arguments: dict[str, typing.Any],
) -> None:

    # Components of a metro map, drawn in increasing z-order:
    # - Action lines
    # - Action start points
    # - Action tipping points
    # - Title, axes and legend

    edge_collection = _plot_action_lines(
        axes,
        pathway_map,
        layout,
        colour_by_action_name=colour_by_action_name,
        tipping_point_overshoot=tipping_point_overshoot,
    )
    edge_collection.set_zorder(0)

    node_collection = _plot_action_starts(
        axes,
        pathway_map,
        layout,
        colour_by_action_name=colour_by_action_name,
        start_action_marker=start_action_marker,
    )
    node_collection.set_zorder(1)

    node_collection = _plot_action_tipping_points(
        axes,
        pathway_map,
        layout,
        colour_by_action_name=colour_by_action_name,
        tipping_point_face_colour=tipping_point_face_colour,
        tipping_point_marker=tipping_point_marker,
        tipping_point_overshoot=tipping_point_overshoot,
    )
    node_collection.set_zorder(1)

    _plot_annotations(
        axes,
        layout,
        y_coordinate_by_action_name,
        colour_by_action_name=colour_by_action_name,
        level_by_action_name=level_by_action_name,
        marker_by_action_name=marker_by_action_name,
        marker_style=marker_style,
        show_legend=show_legend,
        title=title,
        use_markers_as_yticks=use_markers_as_yticks,
        x_label=x_label,
        legend_arguments=legend_arguments,
    )

    axes.autoscale_view()


def _group_overlapping_regions(
    regions: list[tuple[Region, typing.Any]],
) -> list[list[tuple[Region, typing.Any]]]:

    # Given a list of tuples of regions and their payload (additional information not relevant here):
    # - Group the regions into overlapping regions
    # - Return a list of overlapping regions, along with their payload

    # Split list of tuple[Region, Payload] into list[Region] and list[Payload]
    # Group the regions
    # Re-associate each region with its payload again

    grouped_regions, grouped_payloads = group_overlapping_regions_with_payloads(
        *(list(tuples) for tuples in zip(*regions))
    )
    result: list[list[tuple[Region, typing.Any]]] = []

    for region_group, payload_group in zip(grouped_regions, grouped_payloads):
        result.append(list(zip(region_group, payload_group)))

    return result


# pylint: disable-next=too-many-locals
def _spread_vertically(
    pathway_map: PathwayMap,
    position_by_node: PositionByNode,
    overlapping_lines_spread: float,
) -> None:

    # - Assign all action_begin / action_end combinations to bins, by y-coordinate
    # - For those bins that contain more than one element, tweak the y-coordinates
    # - When tweaking y-coordinates take non-overlapping regions into account
    # - Additionally, only tweak y-coordinates of sections that don't share a route from the root node

    # Per y-coordinate a list of regions (x-coordinates), action begin/end tuples
    nodes_by_y: dict[float, list[tuple[Region, tuple[ActionBegin, ActionEnd]]]] = {}

    for action_begin in pathway_map.all_action_begins():
        action_end = pathway_map.action_end(action_begin)

        x_begin, y_begin = position_by_node[action_begin]
        x_end, y_end = position_by_node[action_end]
        assert x_end >= x_begin
        assert y_end == y_begin
        region = x_begin, x_end

        nodes_by_y.setdefault(y_begin, []).append((region, (action_begin, action_end)))

    min_y = min(nodes_by_y.keys())
    max_y = max(nodes_by_y.keys())
    range_y = max_y - min_y

    for y_coordinate, regions in nodes_by_y.items():
        grouped_regions = _group_overlapping_regions(regions)

        for regions in grouped_regions:

            # We now have per non-overlapping region (x-coordinates), one or more pathway sections. Sections
            # that belong to shared routes must not be spread. Whether or not this is the case depends on the
            # ID of the action instances pointed to by the action begin/end nodes. Action instances with the
            # same ID can only be reached using the same, shared, route.

            sections_by_action_id: dict[int, list[tuple[ActionBegin, ActionEnd]]] = {}

            for region_section in regions:
                action_begin, action_end = region_section[1]
                assert action_begin.action is action_end.action
                sections_by_action_id.setdefault(id(action_begin.action), []).append(
                    region_section[1]
                )

            nr_regions = len(sections_by_action_id)

            y_coordinates = distribute(
                nr_regions * [y_coordinate], overlapping_lines_spread * range_y
            )

            for idx, sections in enumerate(sections_by_action_id.values()):
                for section in sections:
                    action_begin, action_end = section
                    position_by_node[action_begin][1] = y_coordinates[idx]
                    position_by_node[action_end][1] = y_coordinates[idx]


def _distribute_horizontally(
    pathway_map: PathwayMap,
    action_begin: ActionBegin,
    tipping_point_by_action: TippingPointByAction,
    position_by_node: PositionByNode,
) -> None:
    assert isinstance(action_begin, ActionBegin)

    action_end = pathway_map.action_end(action_begin)
    end_x = tipping_point_by_action[action_end.action]

    add_position(position_by_node, action_end, (end_x, np.nan))

    for action_begin_new in pathway_map.action_begins(
        pathway_map.action_end(action_begin)
    ):
        begin_x = end_x

        add_position(position_by_node, action_begin_new, (begin_x, np.nan))
        _distribute_horizontally(
            pathway_map, action_begin_new, tipping_point_by_action, position_by_node
        )


# pylint: disable-next=too-many-locals
def _spread_horizontally(
    pathway_map: PathwayMap,
    position_by_node: PositionByNode,
    overlapping_lines_spread: float,
) -> None:

    # - Assign all action_end / action_begin combinations to bins, by x-coordinate
    # - For those bins that contain more than one element, tweak the x-coordinates
    # - When tweaking x-coordinates take non-overlapping regions into account
    # - Additionally, only tweak x-coordinates of sections that don't share a route from the root node

    # Per x-coordinate a list of regions (y-coordinates), action end/begin tuples
    nodes_by_x: dict[float, list[tuple[Region, tuple[ActionEnd, ActionBegin]]]] = {}

    for action_end in pathway_map.all_action_ends():
        action_begins = pathway_map.action_begins(action_end)

        if action_begins:
            x_end, y_end = position_by_node[action_end]

            if x_end not in nodes_by_x:
                nodes_by_x[x_end] = []

            for action_begin in action_begins:
                x_begin, y_begin = position_by_node[action_begin]
                assert x_end == x_begin
                region = tuple(sorted([y_end, y_begin]))

                nodes_by_x[x_end].append((region, (action_end, action_begin)))

    min_x = min(nodes_by_x.keys())
    max_x = max(
        position_by_node[action_end][0] for action_end in pathway_map.leaf_nodes()
    )
    range_x = max_x - min_x

    for x_coordinate, regions in nodes_by_x.items():
        grouped_regions = _group_overlapping_regions(regions)

        for regions in grouped_regions:

            # We now have per non-overlapping region (y-coordinates), one or more pathway sections. Sections
            # that belong to shared routes must not be spread. Whether or not this is the case depends on the
            # ID of the action instances pointed to by the action begin/end nodes. Action instances with the
            # same ID can only be reached using the same, shared, route.

            section_by_action_id: dict[int, list[tuple[ActionEnd, ActionBegin]]] = {}

            for region_section in regions:
                action_end, action_begin = region_section[1]
                assert action_end.action is not action_begin.action
                section_by_action_id.setdefault(id(action_end.action), []).append(
                    region_section[1]
                )

            nr_regions = len(section_by_action_id)

            x_coordinates = distribute(
                nr_regions * [x_coordinate], overlapping_lines_spread * range_x
            )

            for idx, sections in enumerate(section_by_action_id.values()):
                for section in sections:
                    action_end, action_begin = section
                    position_by_node[action_end][0] = x_coordinates[idx]
                    position_by_node[action_begin][0] = x_coordinates[idx]


# pylint: disable-next=too-many-locals, too-many-branches
def _distribute_vertically(
    pathway_map: PathwayMap,
    root_actions_begins: list[ActionBegin],
    level_by_action_name: LevelByActionName,
    position_by_node: PositionByNode,
) -> dict[str, float]:

    for root_action_begin in root_actions_begins:
        action_end = pathway_map.action_end(root_action_begin)
        position_by_node[action_end][1] = position_by_node[root_action_begin][1]

    # All action instances in the graph
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
    y_coordinates: list[float] = list(
        range(
            math.floor(len(names_of_actions_to_distribute) / 2),
            -math.floor((len(names_of_actions_to_distribute) - 1) / 2) - 1,
            -1,
        )
    )

    # Nodes related to the root action are already positioned, at y == 0.0. Delete those coordinates and the
    # root action names.
    y_coordinates = [coordinate for coordinate in y_coordinates if coordinate != 0.0]
    root_actions = [
        root_action_begin.action for root_action_begin in root_actions_begins
    ]
    root_action_names = [action.name for action in root_actions]
    names_of_actions_to_distribute = [
        name for name in names_of_actions_to_distribute if name not in root_action_names
    ]
    assert len(y_coordinates) == len(names_of_actions_to_distribute)

    # Now it is time to re-order the actions to distribute, based on their level, if any was set

    # Update the levels of action combinations that continue multiple existing actions. These
    # must end up somewhere in between the continued actions.
    for action, continued_actions in action_combinations_continuations.items():
        assert action.name in level_by_action_name
        level_by_action_name[action.name] = sum(
            level_by_action_name[action.name] for action in continued_actions
        ) / len(continued_actions)

    names_of_actions_to_distribute.sort(
        key=lambda action_name: level_by_action_name[action_name]
    )

    y_coordinate_by_action_name = dict(
        zip(names_of_actions_to_distribute, y_coordinates)
    )

    for root_action_begin in root_actions_begins:
        y_coordinate_by_action_name[root_action_begin.action.name] = 0

    for action_begin in pathway_map.all_action_begins()[1:]:  # Skip root node
        if action_begin not in root_actions_begins:
            action = action_begin.action

            if (
                isinstance(action, ActionCombination)
                and action in action_combinations_sieved
            ):
                # In this case we want the combination to end up at the same y-coordinate as the
                # one action that is being continued
                action = action_combinations_sieved[action]

            y_coordinate = y_coordinate_by_action_name[action.name]

            assert np.isnan(position_by_node[action_begin][1])
            position_by_node[action_begin][1] = y_coordinate
            action_end = pathway_map.action_end(action_begin)

            assert np.isnan(position_by_node[action_end][1])
            position_by_node[action_end][1] = y_coordinate

    return y_coordinate_by_action_name


def _layout(
    pathway_map: PathwayMap,
    *,
    overlapping_lines_spread=(0.0, 0.0),
    level_by_action_name: LevelByActionName,
    tipping_point_by_action,
) -> tuple[PositionByNode, dict[str, float]]:
    """
    Layout that replicates the pathway map layout of the original (pre-2024) pathway generator

    :param pathway_map: Pathway map
    :return: Node positions

    The layout has the following characteristics:

    - A pathway map is a stack of horizontal lines representing actions
    - Each action ends up at its own level in the stack
    - Pathways jump from horizontal line to horizontal line, depending on the sequences of
      actions that make up each pathway
    """
    # TODO Update and move docs elsewhere
    # The pathway map passed in must contain sane tipping points. When in doubt, call
    # ``verify_tipping_points()`` before calling this function.

    # level_by_action_name:
    # Low numbers correspond with a high position in the stack (large y-coordinate). Such
    # actions will be positioned at the top of the pathway map.

    position_by_node: PositionByNode = {}
    y_coordinate_by_action_name: dict[str, float] = {}

    if pathway_map.nr_edges() > 0:

        min_tipping_point, max_tipping_point = tipping_point_range(
            pathway_map, tipping_point_by_action
        )
        tipping_point_range_ = max_tipping_point - min_tipping_point
        assert tipping_point_range_ >= 0

        root_actions_begins = pathway_map.root_nodes
        root_actions_ends = [
            pathway_map.action_end(root_action_begin)
            for root_action_begin in root_actions_begins
        ]
        root_actions_tipping_points = [
            tipping_point_by_action[root_action_end.action]
            for root_action_end in root_actions_ends
        ]
        x_coordinates = [
            tipping_point - 0.1 * tipping_point_range_
            for tipping_point in root_actions_tipping_points
        ]

        for root_action_begin, x_coordinate in zip(root_actions_begins, x_coordinates):
            add_position(position_by_node, root_action_begin, (x_coordinate, 0))

        for root_action_begin, x_coordinate in zip(root_actions_begins, x_coordinates):
            _distribute_horizontally(
                pathway_map,
                root_action_begin,
                tipping_point_by_action,
                position_by_node,
            )

        y_coordinate_by_action_name = _distribute_vertically(
            pathway_map, root_actions_begins, level_by_action_name, position_by_node
        )

        if not isinstance(overlapping_lines_spread, tuple):
            overlapping_lines_spread = (
                overlapping_lines_spread,
                overlapping_lines_spread,
            )

        horizontal_spread, vertical_spread = overlapping_lines_spread

        if horizontal_spread > 0:
            _spread_horizontally(pathway_map, position_by_node, horizontal_spread)
        if vertical_spread > 0:
            _spread_vertically(pathway_map, position_by_node, vertical_spread)

    return position_by_node, y_coordinate_by_action_name


def plot(
    axes: mpl.axes.Axes,
    pathway_map: PathwayMap,
    *,
    colour_by_action_name: ColourByActionName | None = None,
    legend_arguments: dict[str, typing.Any] | None = None,
    level_by_action_name: LevelByActionName | None = None,
    marker_by_action_name: MarkerByActionName | None = None,
    marker_style: MarkerStyle | None = None,
    overlapping_lines_spread=(0.0, 0.0),
    show_legend: bool = False,
    start_action_marker: mmarkers.MarkerStyle = "o",
    tipping_point_by_action: TippingPointByAction,
    tipping_point_face_colour="white",
    tipping_point_marker: mmarkers.MarkerStyle | str | None = None,
    tipping_point_overshoot: float = 0.0,
    title: str = "",
    use_markers_as_yticks: bool = False,
    x_label: str = "",
) -> None:

    if colour_by_action_name is None:
        colour_by_action_name = colour_by_action_name_pathway_map(
            pathway_map, default_nominal_palette()
        )

    if legend_arguments is None:
        legend_arguments = {}

    if level_by_action_name is None:
        level_by_action_name = action_level_by_first_occurrence(pathway_map)

    if marker_by_action_name is None:
        marker_by_action_name = {
            action_name: "_" for action_name in colour_by_action_name
        }

    if marker_style is None:
        marker_style = {
            "markeredgewidth": 1.5,
            "markersize": 10,
        }

    tipping_point_marker = (
        tipping_point_marker
        if tipping_point_marker is not None
        else ("|" if tipping_point_overshoot > 0 else "o")
    )

    if isinstance(tipping_point_marker, str):
        tipping_point_marker = mmarkers.MarkerStyle(tipping_point_marker)

    layout, y_coordinate_by_action_name = _layout(
        pathway_map,
        overlapping_lines_spread=overlapping_lines_spread,
        level_by_action_name=level_by_action_name,
        tipping_point_by_action=tipping_point_by_action,
    )

    classic_pathway_map_plotter(
        axes,
        pathway_map,
        layout,
        y_coordinate_by_action_name,
        colour_by_action_name=colour_by_action_name,
        legend_arguments=legend_arguments,
        level_by_action_name=level_by_action_name,
        marker_by_action_name=marker_by_action_name,
        marker_style=marker_style,
        show_legend=show_legend,
        start_action_marker=start_action_marker,
        tipping_point_face_colour=tipping_point_face_colour,
        tipping_point_marker=tipping_point_marker,
        tipping_point_overshoot=tipping_point_overshoot,
        title=title,
        use_markers_as_yticks=use_markers_as_yticks,
        x_label=x_label,
    )
