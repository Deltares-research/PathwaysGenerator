import unittest

import numpy.testing as npt

from adaptation_pathways.action import Action
from adaptation_pathways.action_combination import ActionCombination
from adaptation_pathways.graph.conversion import sequence_graph_to_pathway_graph
from adaptation_pathways.graph.node import Action as ActionNode
from adaptation_pathways.graph.sequence_graph import SequenceGraph
from adaptation_pathways.plot.pathway_graph.default import _layout as default_layout


class PathwayGraphLayoutTest(unittest.TestCase):
    def assert_equal_positions(self, positions_we_got, path, positions_we_want):
        self.assertEqual(len(path), len(positions_we_want))

        for idx, node in enumerate(path):
            self.assertEqual(positions_we_want[idx][0], node.label)
            npt.assert_almost_equal(positions_we_want[idx][1], positions_we_got[node])

    def test_empty(self):
        sequence_graph = SequenceGraph()
        pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)
        positions = default_layout(pathway_graph)

        self.assertEqual(len(positions), 0)

    def test_serial_pathway(self):
        sequence_graph = SequenceGraph()
        current = ActionNode(Action("current"))
        a = ActionNode(Action("a"))
        b = ActionNode(Action("b"))
        c = ActionNode(Action("c"))

        sequence_graph.add_sequence(current, a)
        sequence_graph.add_sequence(a, b)
        sequence_graph.add_sequence(b, c)

        pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)
        paths = list(pathway_graph.all_paths())
        self.assertEqual(len(paths), 1)

        positions = default_layout(pathway_graph)
        self.assertEqual(len(positions), 7)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("current", (0, 0)),
                ("current | a", (1, 0)),
                ("a", (2, 0)),
                ("a | b", (3, 0)),
                ("b", (4, 0)),
                ("b | c", (5, 0)),
                ("c", (6, 0)),
            ],
        )

    def test_diverging_pathways(self):
        sequence_graph = SequenceGraph()
        current = ActionNode(Action("current"))
        a = ActionNode(Action("a"))
        b = ActionNode(Action("b"))
        c = ActionNode(Action("c"))

        sequence_graph.add_sequence(current, a)
        sequence_graph.add_sequence(current, b)
        sequence_graph.add_sequence(current, c)

        pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)
        paths = list(pathway_graph.all_paths())
        self.assertEqual(len(paths), 3)

        positions = default_layout(pathway_graph)
        self.assertEqual(len(positions), 7)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("current", (0, 0)),
                ("current | a", (1, 1)),
                ("a", (2, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("current", (0, 0)),
                ("current | b", (1, 0)),
                ("b", (2, 0)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("current", (0, 0)),
                ("current | c", (1, -1)),
                ("c", (2, -1)),
            ],
        )

    def test_converging_pathways(self):
        sequence_graph = SequenceGraph()
        current = ActionNode(Action("current"))
        a = ActionNode(Action("a"))
        b = ActionNode(Action("b"))
        c = ActionNode(Action("c"))
        d = ActionNode(Action("d"))

        sequence_graph.add_sequence(current, a)
        sequence_graph.add_sequence(current, b)
        sequence_graph.add_sequence(current, c)
        sequence_graph.add_sequence(a, d)
        sequence_graph.add_sequence(b, d)
        sequence_graph.add_sequence(c, d)

        pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)
        paths = list(pathway_graph.all_paths())
        self.assertEqual(len(paths), 3)

        positions = default_layout(pathway_graph)
        self.assertEqual(len(positions), 13)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("current", (0, 0)),
                ("current | a", (1, 1)),
                ("a", (2, 1)),
                ("a | d", (3, 1)),
                ("d", (4, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("current", (0, 0)),
                ("current | b", (1, 0)),
                ("b", (2, 0)),
                ("b | d", (3, 0)),
                ("d", (4, 0)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("current", (0, 0)),
                ("current | c", (1, -1)),
                ("c", (2, -1)),
                ("c | d", (3, -1)),
                ("d", (4, -1)),
            ],
        )

    def test_use_case_01(self):
        sequence_graph = SequenceGraph()
        current = ActionNode(Action("current"))
        a = ActionNode(Action("a"))
        b = ActionNode(Action("b"))
        c = ActionNode(Action("c"))
        d = ActionNode(Action("d"))
        e = ActionNode(Action("e"))
        f = ActionNode(Action("f"))

        sequence_graph.add_sequences(
            [
                (current, a),
                (a, e),
                (current, b),
                (b, f),
                (current, c),
                (c, f),
                (current, d),
                (d, f),
                (f, e),
            ]
        )

        pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)
        paths = list(pathway_graph.all_paths())
        self.assertEqual(len(paths), 4)

        positions = default_layout(pathway_graph)
        self.assertEqual(len(positions), 23)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("current", (0, 0)),
                ("current | a", (1, 1.5)),
                ("a", (2, 1.5)),
                ("a | e", (3, 1.5)),
                ("e", (4, 1.5)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("current", (0, 0)),
                ("current | b", (1, 0.5)),
                ("b", (2, 0.5)),
                ("b | f", (3, 0.5)),
                ("f", (4, 0.5)),
                ("f | e", (5, 0.5)),
                ("e", (6, 0.5)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("current", (0, 0)),
                ("current | c", (1, -0.5)),
                ("c", (2, -0.5)),
                ("c | f", (3, -0.5)),
                ("f", (4, -0.5)),
                ("f | e", (5, -0.5)),
                ("e", (6, -0.5)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[3],
            [
                ("current", (0, 0)),
                ("current | d", (1, -1.5)),
                ("d", (2, -1.5)),
                ("d | f", (3, -1.5)),
                ("f", (4, -1.5)),
                ("f | e", (5, -1.5)),
                ("e", (6, -1.5)),
            ],
        )

    def test_action_combination_01(self):
        sequence_graph = SequenceGraph()
        current = ActionNode(Action("current"))
        a = Action("a")
        b = Action("b")
        c = ActionNode(Action("c"))
        d = ActionNode(ActionCombination("d", [a, b]))

        a = ActionNode(a)
        b = ActionNode(b)

        sequence_graph.add_sequences(
            [
                (current, a),
                (current, b),
                (current, c),
                (a, d),
            ]
        )

        pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)
        paths = list(pathway_graph.all_paths())
        self.assertEqual(len(paths), 3)

        positions = default_layout(pathway_graph)
        self.assertEqual(len(positions), 9)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("current", (0, 0)),
                ("current | a", (1, 1)),
                ("a", (2, 1)),
                ("a | d", (3, 1)),
                ("d", (4, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("current", (0, 0)),
                ("current | b", (1, 0)),
                ("b", (2, 0)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("current", (0, 0)),
                ("current | c", (1, -1)),
                ("c", (2, -1)),
            ],
        )

    def test_action_combination_02(self):
        sequence_graph = SequenceGraph()
        current = ActionNode(Action("current"))
        a = Action("a")
        b = Action("b")
        c = ActionNode(Action("c"))
        d = ActionNode(ActionCombination("d", [a, b]))

        a = ActionNode(a)
        b = ActionNode(b)

        sequence_graph.add_sequences(
            [
                (current, a),
                (current, b),
                (current, c),
                (a, d),
                (b, d),
            ]
        )

        pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)
        paths = list(pathway_graph.all_paths())
        self.assertEqual(len(paths), 3)

        positions = default_layout(pathway_graph)
        self.assertEqual(len(positions), 11)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("current", (0, 0)),
                ("current | a", (1, 1)),
                ("a", (2, 1)),
                ("a | d", (3, 1)),
                ("d", (4, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("current", (0, 0)),
                ("current | b", (1, 0)),
                ("b", (2, 0)),
                ("b | d", (3, 0)),
                ("d", (4, 0)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("current", (0, 0)),
                ("current | c", (1, -1)),
                ("c", (2, -1)),
            ],
        )

    def test_action_edition_01(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a1 = Action("a")
        b = Action("b")
        a2 = Action("a")

        current_node = ActionNode(current)
        a1_node = ActionNode(a1)
        b_node = ActionNode(b)
        a2_node = ActionNode(a2)

        sequence_graph.add_sequences(
            [
                (current_node, a1_node),
                (current_node, b_node),
                (b_node, a2_node),
            ]
        )

        pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)
        paths = list(pathway_graph.all_paths())
        self.assertEqual(len(paths), 2)

        positions = default_layout(pathway_graph)
        self.assertEqual(len(positions), 7)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("current", (0, 0)),
                ("current | a", (1, 0.5)),
                ("a", (2, 0.5)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("current", (0, 0)),
                ("current | b", (1, -0.5)),
                ("b", (2, -0.5)),
                ("b | a", (3, -0.5)),
                ("a", (4, -0.5)),
            ],
        )
