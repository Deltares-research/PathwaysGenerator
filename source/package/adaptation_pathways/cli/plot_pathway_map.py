import os.path
import sys

import docopt
import matplotlib.pyplot as plt

from ..graph.conversion import (
    sequence_graph_to_pathway_map,
    sequences_to_sequence_graph,
)
from ..io.dataset import read_dataset
from ..plot import init_axes, plot_classic_pathway_map, save_plot
from ..plot.util import action_level_by_first_occurrence
from ..version import __version__ as version
from .main import main_function


@main_function
def plot_map(basename_pathname: str, plot_pathname: str) -> int:

    # pylint: disable-next=unused-variable
    actions, sequences, tipping_point_by_action, colour_by_action = read_dataset(
        basename_pathname
    )

    colour_by_action_name = {
        action.name: colour for action, colour in colour_by_action.items()
    }

    _, axes = plt.subplots(layout="constrained")
    init_axes(axes)

    level_by_action = action_level_by_first_occurrence(sequences)
    sequence_graph = sequences_to_sequence_graph(sequences)
    pathway_map = sequence_graph_to_pathway_map(sequence_graph)

    if pathway_map.nr_nodes() > 0:
        pathway_map.assign_tipping_points(tipping_point_by_action, verify=True)
    pathway_map.set_attribute("level_by_action", level_by_action)
    pathway_map.set_attribute("colour_by_action_name", colour_by_action_name)

    plot_classic_pathway_map(axes, pathway_map, title="Pathway map")
    save_plot(plot_pathname)

    return 0


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Plot pathway map

Usage:
    {command} <basename> <plot>

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

The format for storing sequences is simple: per line mention the names of
two actions that form a sequence. Information from multiple lines can result
in longer sequences. To allow for the same action to occur in different
sequences, a number can be added to the name.

Examples:
    {command} serial serial.pdf
    {command} serial.apw serial.pdf
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=version)
    basename_pathname = arguments["<basename>"]  # type: ignore
    plot_pathname = arguments["<plot>"]  # type: ignore

    if len(os.path.splitext(plot_pathname)[1]) == 0:
        plot_pathname += ".pdf"

    return plot_map(basename_pathname, plot_pathname)
