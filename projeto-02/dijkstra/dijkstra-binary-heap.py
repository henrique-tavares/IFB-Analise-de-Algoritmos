from collections import defaultdict
from typing import Dict, List, Tuple
import heapq
import sys

sys.path.append("../../projeto-02")

from graph import Graph, Edge


class Dijkstra:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.paths: Dict[str, Dict[str, Tuple[str, float]]] = defaultdict(dict)

    def calculate_shortest_paths(self, source: str) -> Dict[str, Tuple[str, float]]:
        if source not in self.graph:
            raise ValueError(f"vertice {source} not found in graph {self.graph}")

        paths: Dict[str, Tuple[str, float]] = defaultdict(lambda: ("", float("inf")))
        paths[source] = ("", 0)

        visited_vertices: List[str] = list()

        vertices_queue = list()
        heapq.heappush(vertices_queue, (0, source))

        while len(vertices_queue) > 0:
            accumulated_distance, current_vertice = heapq.heappop(vertices_queue)
            if current_vertice in visited_vertices:
                continue

            for (next_vertice, distance) in self.graph[current_vertice].items():
                new_distance = accumulated_distance + distance
                if new_distance < paths[next_vertice][1]:
                    paths[next_vertice] = current_vertice, new_distance

                heapq.heappush(vertices_queue, (new_distance, next_vertice))

            visited_vertices.append(current_vertice)

        self.paths[source] = dict(paths)
        return dict(paths)

    def build_path(self, source: str, destination: str) -> str:
        if source not in self.paths:
            raise ValueError(f"There are no paths calculated from source vertice: {source}")

        if destination not in self.paths[source]:
            raise ValueError(f"Destination: {destination} unreacheable from source: {source}")

        path: List[str] = list()
        current_step = destination

        while current_step != "":
            path.append(f"{current_step} ({self.paths[source][current_step][1]})")
            current_step = self.paths[source][current_step][0]

        return " -> ".join(path[::-1])


if __name__ == "__main__":
    g = Graph()
    g.add("1", Edge("2", 50), Edge("3", 45), Edge("4", 10, True))
    g.add("2", Edge("4", 15), Edge("3", 10))
    g.add("3", Edge("5", 30))
    g.add("4", Edge("5", 15))
    g.add("5", Edge("2", 20), Edge("3", 35))
    g.add("6", Edge("5", 3))

    d = Dijkstra(g)
    d.calculate_shortest_paths("1")

    for v in g:
        try:
            print(d.build_path("1", v))
        except Exception as e:
            print(e)
