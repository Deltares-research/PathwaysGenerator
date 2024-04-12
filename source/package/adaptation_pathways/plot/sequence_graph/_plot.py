import matplotlib as mpl

from ...graph import SequenceGraph
from ..colour import PlotColours
from .default import plot as plot_default


def plot_sequence_graph(
    axes: mpl.axes.Axes,
    sequence_graph: SequenceGraph,
    title: str = "",
    plot_colours: PlotColours | None = None,
) -> None:
    plot_default(axes, sequence_graph, title, plot_colours)
