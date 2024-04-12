import matplotlib as mpl

from ...graph import PathwayMap
from ..colour import PlotColours
from ..util import PathwayMapLayout
from .classic import plot as plot_classic
from .default import plot as plot_default


def plot_pathway_map(
    axes: mpl.axes.Axes,
    pathway_map: PathwayMap,
    title: str = "",
    layout: PathwayMapLayout = PathwayMapLayout.DEFAULT,
    plot_colours: PlotColours | None = None,
) -> None:
    if layout == PathwayMapLayout.CLASSIC:
        plot_classic(axes, pathway_map, title, plot_colours)
    else:
        plot_default(axes, pathway_map, title, plot_colours)
