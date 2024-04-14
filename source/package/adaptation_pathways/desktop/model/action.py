from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt

from ... import alias


class ActionModel(QtCore.QAbstractTableModel):

    _actions: list[list]
    _headers: tuple[str]
    _colour_by_action_name: dict[str, alias.Colour]

    def __init__(
        self, actions: list[list], colour_by_action_name: dict[str, alias.Colour]
    ):

        super().__init__()
        self._actions = actions
        self._headers = ("Name",)
        self._colour_by_action_name = colour_by_action_name

    # pylint: disable=inconsistent-return-statements, no-else-return
    def data(self, index, role):
        if role == Qt.DisplayRole:
            record = self._actions[index.row()]
            if index.column() == 0:
                action = record[0]
                return action.name
        elif role == Qt.DecorationRole:
            if index.column() == 0:
                action = self._actions[index.row()][0]
                colour = self._colour_by_action_name[action.name]
                return QtGui.QColor.fromRgbF(*colour)

    def rowCount(self, index):  # pylint: disable=unused-argument
        return len(self._actions)

    def columnCount(self, index):  # pylint: disable=unused-argument
        return len(self._headers)

    # pylint: disable=inconsistent-return-statements
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]

    def removeRows(self, row, nr_rows, parent):  # pylint: disable=unused-argument
        self.beginRemoveRows(QtCore.QModelIndex(), row, row + nr_rows - 1)
        del self._actions[row : row + nr_rows]
        self.endRemoveRows()
        return True
