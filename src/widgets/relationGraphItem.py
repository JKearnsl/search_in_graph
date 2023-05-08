from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


class RGI(QtWidgets.QWidget):
    """
    Виджет представляет собой элемент входных
    данных графа: связь между вершинами.
    """

    valueChanged = QtCore.pyqtSignal(tuple)

    def __init__(self, index, _from=0, _to=0, *args, **kwargs):
        super().__init__()

        self._index = index

        layout = QtWidgets.QHBoxLayout()

        layout.addWidget(QtWidgets.QLabel(f"[{index + 1}]"))

        layout.addItem(QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        ))

        layout.addWidget(QtWidgets.QLabel("Из: "))
        self._from_widget = QtWidgets.QLineEdit()
        self._from_widget.setText(str(_from))
        self._from_widget.textChanged.connect(self.signal_change)
        layout.addWidget(self._from_widget)

        layout.addWidget(QtWidgets.QLabel("В: "))
        self._to_widget = QtWidgets.QLineEdit()
        self._to_widget.setText(str(_to))
        self._to_widget.textChanged.connect(self.signal_change)
        layout.addWidget(self._to_widget)

        self.setLayout(layout)

    def signal_change(self):
        """
        Вызывается при изменении любого из полей
        """
        from_value = self._from_widget.text()
        to_value = self._to_widget.text()
        self.valueChanged.emit((self._index, from_value, to_value))
