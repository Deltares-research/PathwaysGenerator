import unittest

import numpy.testing as npt

from adaptation_pathways.action import Action
from adaptation_pathways.action_combination import ActionCombination
from adaptation_pathways.graph import SequenceGraph
from adaptation_pathways.graph.node import Action as ActionNode
from adaptation_pathways.plot.sequence_graph.default import _layout as default_layout


# pylint: disable=too-many-locals


class SequenceGraphLayoutTest(unittest.TestCase):
    def test_empty(self):
        sequence_graph = SequenceGraph()
        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), 0)

    def test_root_node(self):
        """
        current
        """
        sequence_graph = SequenceGraph()
        current = Action("current")

        current_node = ActionNode(current)
        action_nodes = [current_node]

        sequence_graph.add_action(current_node)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(action_nodes))
        self.assertTrue(all(action_node in positions for action_node in action_nodes))
        npt.assert_almost_equal(positions[current_node], (0, 0))

    def test_single_sequence(self):
        """
        current → a
        """
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")

        current_node = ActionNode(current)
        a_node = ActionNode(a)

        action_nodes = [current_node, a_node]

        sequence_graph.add_sequence(current_node, a_node)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(action_nodes))
        self.assertTrue(all(action_node in positions for action_node in action_nodes))
        npt.assert_almost_equal(positions[current_node], (0, 0))
        npt.assert_almost_equal(positions[a_node], (1, 0))

    def test_serial_sequence(self):
        """
        current → a → b → c
        """
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)

        action_nodes = [current_node, a_node, b_node, c_node]

        sequence_graph.add_sequence(current_node, a_node)
        sequence_graph.add_sequence(a_node, b_node)
        sequence_graph.add_sequence(b_node, c_node)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(action_nodes))
        self.assertTrue(all(action_node in positions for action_node in action_nodes))
        npt.assert_almost_equal(positions[current_node], (0, 0))
        npt.assert_almost_equal(positions[a_node], (1, 0))
        npt.assert_almost_equal(positions[b_node], (2, 0))
        npt.assert_almost_equal(positions[c_node], (3, 0))

    def test_diverging_sequence(self):
        """
                ↗ a
        current
                ↘ b
        """
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)

        action_nodes = [current_node, a_node, b_node]

        sequence_graph.add_sequence(current_node, a_node)
        sequence_graph.add_sequence(current_node, b_node)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(action_nodes))
        self.assertTrue(all(action_node in positions for action_node in action_nodes))
        npt.assert_almost_equal(positions[current_node], (0, 0))
        npt.assert_almost_equal(positions[a_node], (1, 0.5))
        npt.assert_almost_equal(positions[b_node], (1, -0.5))

    def test_converging_sequence(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = Action("d")

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)

        action_nodes = [current_node, a_node, b_node, c_node, d_node]

        sequence_graph.add_sequence(current_node, a_node)
        sequence_graph.add_sequence(current_node, b_node)
        sequence_graph.add_sequence(current_node, c_node)
        sequence_graph.add_sequence(a_node, d_node)
        sequence_graph.add_sequence(b_node, d_node)
        sequence_graph.add_sequence(c_node, d_node)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(action_nodes))
        self.assertTrue(all(action_node in positions for action_node in action_nodes))
        npt.assert_almost_equal(positions[current_node], (0, 0))
        npt.assert_almost_equal(positions[a_node], (1, 1))
        npt.assert_almost_equal(positions[b_node], (1, 0))
        npt.assert_almost_equal(positions[c_node], (1, -1))
        npt.assert_almost_equal(positions[d_node], (2, 0))

    def test_use_case_01(self):
        """
        test_use_case_01
        current - a - e
        current - b - f
        current - c - f
        current - d - f
        current - f - e

        e has in-degree of two, f has in-degree of three, but since e follows f, it must be
        positioned to the right of it
        """
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = Action("d")
        e = Action("e")
        f = Action("f")

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)
        e_node = ActionNode(e)
        f_node = ActionNode(f)

        action_nodes = [current_node, a_node, b_node, c_node, d_node, e_node, f_node]

        sequence_graph.add_sequences(
            [
                (current_node, a_node),
                (a_node, e_node),
                (current_node, b_node),
                (b_node, f_node),
                (current_node, c_node),
                (c_node, f_node),
                (current_node, d_node),
                (d_node, f_node),
                (f_node, e_node),
            ]
        )

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(action_nodes))
        self.assertTrue(all(action_node in positions for action_node in action_nodes))
        npt.assert_almost_equal(positions[current_node], (0, 0))
        npt.assert_almost_equal(positions[a_node], (1, 1.5))
        npt.assert_almost_equal(positions[b_node], (1, 0.5))
        npt.assert_almost_equal(positions[c_node], (1, -0.5))
        npt.assert_almost_equal(positions[d_node], (1, -1.5))
        npt.assert_almost_equal(positions[e_node], (3, 0.5))
        npt.assert_almost_equal(positions[f_node], (2, -0.5))

    def test_action_combination_01(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = ActionCombination("d", [a, b])

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)

        action_nodes = [current_node, a_node, b_node, c_node, d_node]

        sequence_graph.add_sequence(current_node, a_node)
        sequence_graph.add_sequence(current_node, b_node)
        sequence_graph.add_sequence(current_node, c_node)
        sequence_graph.add_sequence(a_node, d_node)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(action_nodes))
        self.assertTrue(all(action_node in positions for action_node in action_nodes))
        npt.assert_almost_equal(positions[current_node], (0, 0))
        npt.assert_almost_equal(positions[a_node], (1, 1))
        npt.assert_almost_equal(positions[b_node], (1, 0))
        npt.assert_almost_equal(positions[c_node], (1, -1))
        npt.assert_almost_equal(positions[d_node], (2, 1))

    def test_action_combination_02(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = ActionCombination("d", [a, b])

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)

        action_nodes = [current_node, a_node, b_node, c_node, d_node]

        sequence_graph.add_sequence(current_node, a_node)
        sequence_graph.add_sequence(current_node, b_node)
        sequence_graph.add_sequence(current_node, c_node)
        sequence_graph.add_sequence(a_node, d_node)
        sequence_graph.add_sequence(b_node, d_node)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(action_nodes))
        self.assertTrue(all(action_node in positions for action_node in action_nodes))
        npt.assert_almost_equal(positions[current_node], (0, 0))
        npt.assert_almost_equal(positions[a_node], (1, 1))
        npt.assert_almost_equal(positions[b_node], (1, 0))
        npt.assert_almost_equal(positions[c_node], (1, -1))
        npt.assert_almost_equal(positions[d_node], (2, 0.5))

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

        action_nodes = [current_node, a1_node, b_node, a2_node]

        sequence_graph.add_sequence(current_node, a1_node)
        sequence_graph.add_sequence(current_node, b_node)
        sequence_graph.add_sequence(b_node, a2_node)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(action_nodes))
        self.assertTrue(all(action_node in positions for action_node in action_nodes))
        npt.assert_almost_equal(positions[current_node], (0, 0))
        npt.assert_almost_equal(positions[a1_node], (1, 0.5))
        npt.assert_almost_equal(positions[b_node], (1, -0.5))
        npt.assert_almost_equal(positions[a2_node], (2, -0.5))
