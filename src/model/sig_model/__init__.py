from collections import OrderedDict

from src.model.enum.graph import GraphType
from src.model.enum.problem import ProblemType
from src.model.sig_model.dfs import dfs
from src.utils.graph import Graph


class SIGModel:

    def __init__(self):
        self._graph_links = []
        self._graph_type: GraphType = GraphType.DIRECTED
        self._problem_type: ProblemType = ProblemType.DFS
        self._search_time = None
        self._visited_path = None
        self._search_value = None

        # список наблюдателей
        self._mObservers = []

    @property
    def graph_links(self):
        return self._graph_links

    @graph_links.setter
    def graph_links(self, value):
        self._graph_links = value
        self.notify_observers()

    def add_link(self, from_node: str, to_node: str):
        # todo: проверка
        self.graph_links.append((from_node, to_node))
        self.notify_observers()

    def remove_link(self, index: int = -1):
        if self.graph_links:
            self.graph_links.pop(index)
            self.notify_observers()

    def graph_canvas(self, width: int = 5, height: int = 5):
        # todo: to view
        graph = Graph(arrows=self.graph_type == GraphType.DIRECTED)
        for link in self.graph_links:
            graph.add_edge(*link)

        if self.graph_links:
            start_vertex = self.graph_links[0][0]
            graph.style_node(start_vertex, node_color='aquamarine', node_size=500)

            if self._search_value:
                is_found, self._search_time, self._visited_path = dfs(self.graph_links, self._search_value, self._search_value)
                if is_found:
                    graph.style_node(self._search_value, node_color='red', node_size=500)

        return graph.canvas(width, height)

    def search_path_table(self):
        if self._visited_path is None:
            return None, None

        vertexes = list(OrderedDict.fromkeys([vertex for link in self._graph_links for vertex in link]))
        table: list[list[str]] = [["-"] * len(vertexes) for i in range(len(vertexes))]
        # for vertex in vertexes:
        #     for el in self.graph_links:
        #         if vertex in el and vertex not in table:
        #             table[vertex] = []
        #
        #         if vertex == el[0]:
        #             table[vertex].append(el[1])

        for i in range(len(vertexes)):
            for j in range(len(vertexes)):
                if (vertexes[i], vertexes[j]) in self._visited_path:
                    table[i][j] = "+"
        return table, vertexes

    @property
    def graph_type(self) -> GraphType:
        return self._graph_type

    @property
    def search_time(self):
        return self._search_time

    @graph_type.setter
    def graph_type(self, value: GraphType):
        self._graph_type = value
        self.notify_observers()

    @property
    def problem_type(self) -> ProblemType:
        return self._problem_type

    @problem_type.setter
    def problem_type(self, value: ProblemType):
        self._problem_type = value
        self.notify_observers()

    @property
    def search_value(self):
        return self._search_value

    @search_value.setter
    def search_value(self, value: int):
        self._search_value = value
        self.notify_observers()

    def add_observer(self, observer):
        self._mObservers.append(observer)

    def remove_observer(self, observer):
        self._mObservers.remove(observer)

    def notify_observers(self):
        for observer in self._mObservers:
            observer.model_changed()
