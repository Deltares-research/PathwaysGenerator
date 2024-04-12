import matplotlib as mpl

from ...graph import PathwayGraph
from ..colour import PlotColours
from .default import plot as plot_default


def plot_pathway_graph(
    axes: mpl.axes.Axes,
    pathway_graph: PathwayGraph,
    title: str = "",
    plot_colours: PlotColours | None = None,
) -> None:
    plot_default(axes, pathway_graph, title, plot_colours)
