"""
This sub package contains classes whose instances end up as nodes in graphs. Some of them refer
to one or more actions. Even the ``node.Action`` class refers to an ``Action``. The idea is
that actions can be reused in nodes. Multiple node class instances can refer to the same
``Action`` instance. This is needed because some information needs to be unique per node
(position in a layout for example), and some information needs to be shared between nodes but
unique per action (colour in a plot for example).
"""

from .action import Action
from .action_begin import ActionBegin
from .action_conversion import ActionConversion
from .action_end import ActionEnd
from .action_period import ActionPeriod
from .node import Node
