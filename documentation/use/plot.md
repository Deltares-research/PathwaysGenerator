# Plotting pathways

The package contains multiple command-line applications. `ap_plot_graphs` can be used to gain insight into
various kinds of graphs used to store information about pathways. `ap_plot_pathway_map` can be used to
visualize pathway maps in the so-called metro map layout. `ap_plot_bars` can be used to visualize pathways
using bar plots.


## `ap_plot_graphs`

See also:
{mod}`adaptation_pathways.cli.plot_graphs`,
{class}`SequenceGraph <adaptation_pathways.graph.sequence_graph.SequenceGraph>`,
{class}`PathwayGraph <adaptation_pathways.graph.pathway_graph.PathwayGraph>`,
{class}`PathwayMap <adaptation_pathways.graph.pathway_map.PathwayMap>`

This command takes information about pathways as input, and outputs a plot of the sequence graph, a plot of
the pathway graph and a plot of the pathway map in default layout.

Example for creating plots from `my_pathways-action.txt` and `my_pathways-sequence.txt` (or `my_pathways.apw`)
to `./my_pathways-sequence_graph.pdf`, `./my_pathways-pathway_graph.pdf`, and `./my_pathways-pathway_map.pdf`:

```bash
ap_plot_graphs my_pathways .
```

For help about the usage of the command type `ap_plot_graphs --help`.


## `ap_plot_pathway_map`

See also:
{mod}`adaptation_pathways.cli.plot_pathway_map`,
{class}`PathwayMap <adaptation_pathways.graph.pathway_map.PathwayMap>`

This command takes information about pathways as input, and outputs a single plot containing the pathway map
in metro map layout.

Example for creating a plot from `my_pathways-action.txt` and `my_pathways-sequence.txt`
(or `my_pathways.apw`) to `./my_pathways.pdf`:

```bash
ap_plot_pathway_map my_pathways my_pathways.pdf
```

For help about the usage of the command type `ap_plot_pathway_map --help`.


## `ap_plot_bars`

See also:
{mod}`adaptation_pathways.cli.plot_bars`,
{class}`PathwayMap <adaptation_pathways.graph.pathway_map.PathwayMap>`

This command takes information about pathways as input, and outputs a single plot containing the pathways
visualized by horizontal bars.

Example for creating a plot from `my_pathways-action.txt` and `my_pathways-sequence.txt` (or
`my_pathways.apw`) to `./my_pathways.pdf`:

```bash
ap_plot_bars my_pathways my_pathways.pdf
```

For help about the usage of the command type `ap_plot_bars --help`.
