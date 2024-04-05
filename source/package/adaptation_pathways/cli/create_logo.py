import os.path
import sys
from io import StringIO

import docopt
import matplotlib.pyplot as plt

from ..graph import conversion
from ..io import text
from ..plot import init_axes, plot_classic_pathway_map, save_plot
from ..plot.util import action_level_by_first_occurrence
from ..version import __version__ as version
from .main import main_function


@main_function
def create_logo(plot_pathname: str) -> int:
    actions, colour_by_action = text.read_actions(
        StringIO(
            """
            a #ffbf616a
            b #ffd08770
            c #ffebcb8b
            d #ffa3be8c
            """
        )
    )
    sequences, tipping_point_by_action = text.read_sequences(
        StringIO(
            """
            a a    2040
            a b    2050
            a c    2060
            a d[1] 2070
            c d[2] 2070
    """
        ),
        actions,
    )
    sequence_graph = conversion.sequences_to_sequence_graph(sequences)
    pathway_map = conversion.sequence_graph_to_pathway_map(sequence_graph)

    level_by_action = action_level_by_first_occurrence(sequences)
    colour_by_action_name = {
        action.name: colour for action, colour in colour_by_action.items()
    }

    pathway_map.assign_tipping_points(tipping_point_by_action)
    pathway_map.set_attribute("level_by_action", level_by_action)
    pathway_map.set_attribute("colour_by_action_name", colour_by_action_name)

    _, axes = plt.subplots(layout="constrained")
    init_axes(axes)
    plot_classic_pathway_map(axes, pathway_map)

    save_plot(plot_pathname + ".pdf")
    save_plot(plot_pathname + ".svg")

    # TODO Create raster images in various resolutions.

    return 0


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Create logo

Usage:
    {command} <logo>

Arguments:
    logo            Basename of file to store the logo in. Files with
                    different formats and resolutions will be created.

Options:
    -h --help       Show this screen and exit
    --version       Show version and exit
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=version)
    logo_pathname = arguments["<logo>"]  # type: ignore

    assert len(os.path.splitext(logo_pathname)[1]) == 0, "Please remove the extension"

    return create_logo(logo_pathname)
