import copy
from io import StringIO

from adaptation_pathways.action import Action
from adaptation_pathways.action_combination import ActionCombination


def empty_stream():
    return StringIO(
        """
        """
    )


def serial_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = Action("c")

    actions = [current, a, b, c]

    sequences = [
        (current, a),
        (a, b),
        (b, c),
    ]

    return actions, sequences


def diverging_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = Action("c")

    actions = [current, a, b, c]

    sequences = [
        (current, a),
        (current, b),
        (current, c),
    ]

    return actions, sequences


def converging_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = Action("c")
    d = Action("d")

    actions = [current, a, b, c, d]

    d1 = copy.copy(d)
    d2 = copy.copy(d)
    d3 = copy.copy(d)

    sequences = [
        (current, a),
        (current, b),
        (current, c),
        (a, d1),
        (b, d2),
        (c, d3),
    ]

    return actions, sequences


def action_combination_01_actions():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = ActionCombination("c", [a, b])

    actions = [current, a, b, c]
    sequences = []

    return actions, sequences


def action_combination_01_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = ActionCombination("c", [a, b])

    actions = [current, a, b, c]

    c1 = copy.copy(c)
    c2 = copy.copy(c)

    sequences = [
        (current, a),
        (current, b),
        (a, c1),
        (b, c2),
    ]

    return actions, sequences


def action_combination_02_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = ActionCombination("c", [a, b])

    # Combination before the actions combined
    actions = [current, c, a, b]

    c1 = copy.copy(c)
    c2 = copy.copy(c)

    sequences = [
        (current, a),
        (current, b),
        (a, c1),
        (b, c2),
    ]

    return actions, sequences


def action_combination_03_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = ActionCombination("c", [a, b])

    # Combination before the actions combined
    actions = [current, c, a, b]

    c1 = copy.copy(c)
    c2 = copy.copy(c)

    # Combination before the actions combined
    sequences = [
        (a, c1),
        (b, c2),
        (current, a),
        (current, b),
    ]

    return actions, sequences


def use_case_01_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = Action("c")
    d = Action("d")
    e = Action("e")
    f = Action("f")

    actions = [current, a, b, c, d, e, f]

    e1 = copy.copy(e)
    e2 = copy.copy(e)
    f1 = copy.copy(f)
    f2 = copy.copy(f)
    f3 = copy.copy(f)

    sequences = [
        (current, a),
        (a, e1),
        (current, b),
        (b, f1),
        (current, c),
        (c, f2),
        (current, d),
        (d, f3),
        (f, e2),
    ]

    return actions, sequences


def use_case_02_pathway():
    # pylint: disable=too-many-locals
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = Action("c")
    d = Action("d")

    actions = [current, a, b, c, d]

    a1 = copy.copy(a)
    a2 = copy.copy(a)
    a3 = copy.copy(a)
    a4 = copy.copy(a)
    b1 = copy.copy(b)
    b2 = copy.copy(b)
    c1 = copy.copy(c)
    c2 = copy.copy(c)
    d1 = copy.copy(d)
    d2 = copy.copy(d)
    d3 = copy.copy(d)

    sequences = [
        (current, a1),
        (current, b1),
        (current, c1),
        (current, d1),
        (b1, a2),
        (b1, c2),
        (b1, d2),
        (c, b2),
        (b2, a3),
        (c, a4),
        (c, d3),
    ]

    return actions, sequences
