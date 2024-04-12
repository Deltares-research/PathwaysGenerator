import unittest

from adaptation_pathways.action import Action
from adaptation_pathways.graph import PathwayGraph
from adaptation_pathways.graph.node import ActionPeriod


class PathwayGraphTest(unittest.TestCase):
    def test_constructor(self):
        graph = PathwayGraph()

        self.assertEqual(graph.nr_nodes(), 0)

    def test_single_period(self):
        graph = PathwayGraph()
        current = Action("current")
        a = Action("a")

        graph.add_conversion(ActionPeriod(current), ActionPeriod(a))

        self.assertEqual(graph.nr_nodes(), 3)
