import random
import time

from src.model.enum.graph import GraphType


def dfs(graph: list[tuple], start_vertex, search_value, graph_type: GraphType = GraphType.DIRECTED):
    """
    Поиск в глубину
    :param graph_type:
    :param graph:
    :param start_vertex:
    :param search_value:
    :return:
    """

    visited = set()
    path = []
    stack = [start_vertex]
    is_found = False

    start_time = time.time()
    prev_vertex = None
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            if prev_vertex is not None:
                path.append((prev_vertex, vertex))
            prev_vertex = vertex
            if graph_type == GraphType.DIRECTED:
                stack.extend([x[1] for x in graph if x[0] == vertex])
            else:
                directions = []
                for x in graph:
                    if x[0] == vertex:
                        directions.append(x[1])
                    elif x[1] == vertex and x[0] not in visited:
                        directions.append(x[0])
                random.shuffle(directions)
                stack.extend(directions)

        if vertex == search_value:
            is_found = True
            break
    end_time = time.time()

    return is_found, (end_time - start_time) * 1000, path
