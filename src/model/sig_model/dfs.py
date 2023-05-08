import time


def dfs(graph: list[tuple], start_vertex, search_value):
    """
    Поиск в глубину
    :param graph:
    :param start_vertex:
    :param search_value:
    :return:
    """

    visited = set()
    path = []
    stack = [graph[0][0]]
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
            stack.extend([x[1] for x in graph if x[0] == vertex])

        if vertex == search_value:
            is_found = True
            break
    end_time = time.time()

    return is_found, (end_time - start_time) * 1000, path
