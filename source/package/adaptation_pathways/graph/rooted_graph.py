import typing

import networkx as nx


class RootedGraph:
    """
    A rooted graph represents a directed out-graph in which each node can be reached from the
    root node.
    """

    _graph: nx.DiGraph

    def __init__(self) -> None:
        self._graph = nx.DiGraph()

    def __str__(self) -> str:
        return "\n".join(nx.generate_network_text(self._graph))

    @property
    def graph(self) -> nx.DiGraph:
        """
        :return: The layered directed graph instance

        Try not to use it -- it should be an implementation detail as much as possible.
        """
        return self._graph

    # def is_empty(self) -> bool:
    #     """
    #     :return: Whether or not the tree is empty
    #     """
    #     return nx.is_empty(self._graph)

    def nr_nodes(self) -> int:
        """
        :return: Number of nodes
        """
        return len(self._graph.nodes)

    def nr_edges(self) -> int:
        """
        :return: Number of edges
        """
        return len(self._graph.edges)

    @property
    def root_node(self):
        """
        :return: The root node
        """

        root_nodes = [node for node, degree in self._graph.in_degree() if degree == 0]

        nr_root_nodes = len(root_nodes)

        if nr_root_nodes == 0:
            raise LookupError("Graph is empty")

        if nr_root_nodes > 1:
            raise LookupError(
                "Only single rooted graphs are supported, "
                f"but this graph contains {nr_root_nodes} root nodes"
            )

        return root_nodes[0]

    def all_to_nodes(self, from_node):
        # Use shortest_path to find all nodes reachable from the node passed in
        graph = self._graph.subgraph(nx.shortest_path(self._graph, from_node))

        # Remove the from_node itself before returning the result
        result = list(graph.nodes)
        result.remove(from_node)

        return result

    def to_nodes(self, from_node) -> list[typing.Any]:
        """
        :return: Collection of nodes that start at the node passed in
        """
        return list(self._graph.adj[from_node])

    def from_nodes(self, to_node):
        """
        :return: Collection of nodes that end at the node passed in
        """
        # TODO Can this be done more efficiently?
        return [node for node in self._graph.nodes() if to_node in self.to_nodes(node)]

    def leaf_nodes(self) -> typing.Iterable[typing.Any]:
        """
        :Return: Iterable for iterating over all leaf nodes
        """
        return [
            node
            for node in self._graph.nodes()
            if self._graph.in_degree(node) != 0 and self._graph.out_degree(node) == 0
        ]

    def all_paths(self):
        result = []

        if self.nr_nodes() > 0:
            graph = self._graph
            source_node = self.root_node
            target_nodes = self.leaf_nodes()
            cutoff = None
            result = nx.all_simple_paths(graph, source_node, target_nodes, cutoff)

        return result

    def set_attribute(self, name: str, value: typing.Any) -> None:
        """
        Add / update attribute value to / of the graph

        :param name: Name of attribute to set
        :param value: Value of the attribute to set
        """
        self.graph.graph[name] = value
