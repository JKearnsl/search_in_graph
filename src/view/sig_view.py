from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator, QStandardItemModel, QStandardItem, QColor
from PyQt6.QtWidgets import QMainWindow, QAbstractItemView, QVBoxLayout, QWidget, QListWidgetItem, QGraphicsScene, \
    QGraphicsProxyWidget

from src.model.enum.graph import GraphType
from src.model.enum.problem import ProblemType
from src.utils.observer import TransportSolutionDObserver
from src.utils.ts_meta import TSMeta
from src.view.MainWindow import Ui_MainWindow
from src.widgets.relationGraphItem import RGI


class SIGView(QMainWindow, TransportSolutionDObserver, metaclass=TSMeta):
    """
    Визуальное представление SIGModel.

    """

    def __init__(self, controller, model, parent=None):

        super(QMainWindow, self).__init__(parent)
        self.controller = controller
        self.model = model

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        for el in ProblemType:
            self.ui.problemType.addItem(el.value, el)

        for el in GraphType:
            self.ui.graphType.addItem(el.value, el)

        self.ui.inputGraph.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ui.inputGraph.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.ui.outputTable.setModel(QStandardItemModel(1, 1))
        self.ui.outputTable.model().setHorizontalHeaderLabels([" "])
        self.ui.outputTable.model().setVerticalHeaderLabels([" "])
        self.ui.outputTable.setColumnWidth(0, 50)

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.problemType.currentIndexChanged.connect(self.controller.input_problem_type)
        self.ui.graphType.currentIndexChanged.connect(self.controller.input_graph_type)
        self.ui.searchValue.textChanged.connect(self.controller.input_search_value)
        self.ui.addVertexButton.clicked.connect(self.controller.add_link)
        self.ui.rmVertexButton.clicked.connect(self.controller.remove_link)
        self.ui.updateGraph.clicked.connect(self.controller.update_graph_canvas)

    def model_changed(self):
        """
        Метод вызывается при изменении модели.
        Запрашивает и отображает решение
        """
        self.ui.inputGraph.clear()

        for i, el in enumerate(self.model.graph_links):
            _from, _to = el
            item = QListWidgetItem(self.ui.inputGraph)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            rgi_widget = RGI(i, _from, _to)
            rgi_widget.valueChanged.connect(self.controller.graph_data_changed)
            self.ui.inputGraph.addItem(item)
            item.setSizeHint(rgi_widget.sizeHint())
            self.ui.inputGraph.setItemWidget(item, rgi_widget)

        # Перерисовка графа
        self.model.graph_canvas().figure.clf()
        scene = self.ui.outputGraph.scene()
        if scene is not None:
            for item in scene.items():
                scene.removeItem(item)

        scene = QGraphicsScene()
        self.ui.outputGraph.setScene(scene)
        proxy_widget = QGraphicsProxyWidget()
        proxy_widget.setWidget(self.model.graph_canvas(
            width=self.ui.outputGraph.width()/self.ui.outputGraph.physicalDpiX()*1.5,
            height=self.ui.outputGraph.height()/self.ui.outputGraph.physicalDpiY()*1.5,
        ))
        scene.addItem(proxy_widget)

        # Время поиска
        if self.model.search_time:
            self.ui.searchTime.setText(f"Время поиска: {round(self.model.search_time, 6)} мс.")

        # Перерисовка таблицы
        table, vertexes = self.model.search_path_table()

        if table is None:
            return

        self.ui.outputTable.model().setRowCount(len(table))
        self.ui.outputTable.model().setColumnCount(len(table[0]))
        self.ui.outputTable.model().setHorizontalHeaderLabels(vertexes)
        self.ui.outputTable.model().setVerticalHeaderLabels(vertexes)

        for i, row in enumerate(table):
            for j, el in enumerate(row):
                item = QStandardItem(str(el))
                item.setEditable(False)
                if el == "+":
                    item.setBackground(QColor(0, 255, 0, 100))
                self.ui.outputTable.model().setItem(i, j, item)
