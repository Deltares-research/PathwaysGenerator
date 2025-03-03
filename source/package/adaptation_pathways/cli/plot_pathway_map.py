import os.path
import sys
import typing

import docopt
import matplotlib.pyplot as plt

from ..graph import SequenceGraph, sequence_graph_to_pathway_map, verify_tipping_points
from ..io import read_dataset
from ..plot.pathway_map import plot_classic_pathway_map
from ..plot.util import init_axes, save_plot
from ..version import __version__ as version
from .main import main_function


@main_function
def plot_map(
    basename_pathname: str,
    plot_pathname: str,
    *,
    arguments,
    legend_arguments,
) -> int:

    # pylint: disable-next=unused-variable
    _, sequences, tipping_point_by_action, colour_by_action_name = read_dataset(
        basename_pathname
    )

    sequence_graph = SequenceGraph(sequences)
    pathway_map = sequence_graph_to_pathway_map(sequence_graph)

    verify_tipping_points(pathway_map, tipping_point_by_action)

    _, axes = plt.subplots(layout="constrained")
    init_axes(axes)

    arguments["colour_by_action_name"] = colour_by_action_name
    arguments["tipping_point_by_action"] = tipping_point_by_action

    # TODO Doc this:
    # from svg_pltmarker import get_marker_from_svg

    # marker = get_marker_from_svg(
    #     url="https://upload.wikimedia.org/wikipedia/commons/8/84/Matplotlib_icon.svg"
    # )
    # arguments["marker_by_action_name"] = {
    #     action_name: marker for action_name in colour_by_action_name
    # }
    # arguments["marker_style"] = {
    #     "markerfacecolor": "none",
    #     "markeredgewidth": 0.2,
    #     "markersize": 15,
    # }
    # arguments["use_markers_as_yticks"] = True

    plot_classic_pathway_map(
        axes, pathway_map, **arguments, legend_arguments=legend_arguments
    )
    save_plot(plot_pathname)

    return 0


def parse_spread(spread: str) -> tuple[float, float]:
    spreads = spread.split(",")

    if len(spreads) == 1:
        result = float(spreads[0]), float(spreads[0])
    else:
        assert (
            len(spreads) == 2
        ), "Pass in a single floating point value, or two separated by a comma"
        result = float(spreads[0]), float(spreads[1])

    return result


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Plot pathway map

Usage:
    {command} [--title=<title>] [--x_label=<label>] [--show_legend]
        [--overshoot] [--spread=<spread>] <basename> <plot>

Arguments:
    basename           Either, the name without postfix and extension of text
                       file(s) to read information from, or the name of a
                       binary file to read information from.
    plot               Name of file to store plot in. The format will be
                       based on the extension of the name passed in. The
                       default, when no extension is present, is pdf.

Options:
    -h --help          Show this screen and exit
    --version          Show version and exit
    --overshoot        Show tipping points as overshoots, extending a little
                       bit beyond the actual point
    --show_legend      Show legend
    --spread=<spread>  Separate overlapping lines by a percentage [0, 1] of
                       the data range. A value of 0.01 means 1% of the
                       range. Passing in a value > 0.02 is likely not useful.
                       Pass in a tuple of hspread,vspread to separate between
                       horizontal and vertical spread. Horizontal spread is
                       about the separation of vertical lines (transitions).
                       Vertical spread is about horizontal lines (actions).
                       [default: 0]
    --title=<title>    Title
    --x_label=<label>  Label of x-axis

The format for storing sequences is simple: per line mention the names of
two actions that form a sequence. Information from multiple lines can result
in longer sequences. To allow for the same action to occur in different
sequences, a number can be added to the name.

Examples:
    {command} serial serial.pdf
    {command} serial.apw serial.pdf
"""
    arguments = docopt.docopt(usage, sys.argv[1:], version=version)
    basename_pathname = arguments["<basename>"]
    plot_pathname = arguments["<plot>"]
    title = arguments["--title"] if arguments["--title"] is not None else ""
    x_label = arguments["--x_label"] if arguments["--x_label"] is not None else ""
    show_legend = arguments["--show_legend"]
    overshoot = arguments["--overshoot"]
    overlapping_lines_spread: tuple[float, float] = parse_spread(arguments["--spread"])

    plot_arguments: dict[str, typing.Any] = {
        "title": title,
        "x_label": x_label,
        "show_legend": show_legend,
        "overlapping_lines_spread": overlapping_lines_spread,
    }

    if overshoot:
        plot_arguments["tipping_point_overshoot"] = 0.4

    if len(os.path.splitext(plot_pathname)[1]) == 0:
        plot_pathname += ".pdf"

    legend_arguments = {
        "framealpha": 0.2,
        "fancybox": False,
    }

    return plot_map(
        basename_pathname,
        plot_pathname,
        arguments=plot_arguments,
        legend_arguments=legend_arguments,
    )
