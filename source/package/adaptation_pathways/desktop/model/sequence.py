from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt

from ... import alias
from ...action import Action
from ...plot.colour import Colour


class SequenceModel(QtCore.QAbstractTableModel):
    _sequences: list[list[Action]]
    _tipping_point_by_action: alias.TippingPointByAction
    _horizonal_headers: tuple[str, str, str]
    _colour_by_action_name: dict[str, Colour]

    def __init__(
        self,
        sequences: list[list[Action]],
        tipping_point_by_action: alias.TippingPointByAction,
        colour_by_action_name: dict[str, Colour],
    ):
        super().__init__()
        self._sequences = sequences
        self._tipping_point_by_action = tipping_point_by_action
        self._horizonal_headers = ("From action", "To action", "Tipping point")
        self._colour_by_action_name = colour_by_action_name

        assert len(self._tipping_point_by_action) == len(self._sequences)
        assert all(
            sequence[1] in self._tipping_point_by_action for sequence in self._sequences
        )
        assert all(
            from_action.name in self._colour_by_action_name
            and to_action.name in self._colour_by_action_name
            for (from_action, to_action) in self._sequences
        )

    # pylint: disable=inconsistent-return-statements
    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() < 2:
                action = self._sequences[index.row()][index.column()]
                return action.name

            assert index.column() == 2, index.column()
            to_action = self._sequences[index.row()][1]
            return f"{self._tipping_point_by_action[to_action]}"

        if role == Qt.DecorationRole:
            if index.column() < 2:
                action = self._sequences[index.row()][index.column()]
                colour = self._colour_by_action_name[
                    next(
                        action_name
                        for action_name in self._colour_by_action_name
                        if action_name == action.name
                    )
                ]
                return QtGui.QColor.fromRgbF(*colour)

    def rowCount(self, index):  # pylint: disable=unused-argument
        return len(self._sequences)

    def columnCount(self, index):  # pylint: disable=unused-argument
        return len(self._horizonal_headers)

    # pylint: disable=inconsistent-return-statements
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._horizonal_headers[section]
            if orientation == Qt.Vertical:
                return f"{section}"

    def removeRows(self, row, nr_rows, parent):  # pylint: disable=unused-argument
        self.beginRemoveRows(QtCore.QModelIndex(), row, row + nr_rows - 1)
        del self._sequences[row : row + nr_rows]
        self.endRemoveRows()
        return True
