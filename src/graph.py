"""Модель взвешенного графа, используемая всеми алгоритмами проекта."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, order=True)
class Edge:
    """Ребро графа."""

    source: str
    target: str
    weight: float = 1.0


class Graph:
    """Взвешенный ориентированный или неориентированный граф.

    Внутри граф хранится в виде словаря смежности. Для неориентированного
    графа каждое ребро доступно из обеих вершин, но метод ``edges`` возвращает
    его только один раз.
    """

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self._adjacency: dict[str, dict[str, float]] = {}

    @property
    def vertices(self) -> list[str]:
        return list(self._adjacency.keys())

    def __len__(self) -> int:
        return len(self._adjacency)

    def add_vertex(self, name: str) -> None:
        name = str(name).strip()
        if not name:
            raise ValueError("Имя вершины не может быть пустым.")
        self._adjacency.setdefault(name, {})

    def remove_vertex(self, name: str) -> None:
        if name not in self._adjacency:
            raise KeyError(f"Вершина {name!r} не существует.")
        del self._adjacency[name]
        for neighbours in self._adjacency.values():
            neighbours.pop(name, None)

    def add_edge(self, source: str, target: str, weight: float = 1.0) -> None:
        if source == target:
            raise ValueError("Петли не поддерживаются в учебной версии приложения.")
        numeric_weight = float(weight)
        if source not in self._adjacency or target not in self._adjacency:
            raise KeyError("Перед добавлением ребра необходимо создать обе вершины.")

        self._adjacency[source][target] = numeric_weight
        if not self.directed:
            self._adjacency[target][source] = numeric_weight

    def remove_edge(self, source: str, target: str) -> None:
        if source not in self._adjacency or target not in self._adjacency[source]:
            raise KeyError("Такого ребра в графе нет.")
        del self._adjacency[source][target]
        if not self.directed:
            self._adjacency[target].pop(source, None)

    def neighbours(self, vertex: str) -> list[tuple[str, float]]:
        if vertex not in self._adjacency:
            raise KeyError(f"Вершина {vertex!r} не существует.")
        return sorted(self._adjacency[vertex].items(), key=lambda item: item[0])

    def weight(self, source: str, target: str) -> float:
        return self._adjacency[source][target]

    def has_vertex(self, vertex: str) -> bool:
        return vertex in self._adjacency

    def edges(self) -> list[Edge]:
        result: list[Edge] = []
        seen: set[tuple[str, str]] = set()
        for source in sorted(self._adjacency):
            for target, weight in self._adjacency[source].items():
                key = (source, target) if self.directed else tuple(sorted((source, target)))
                if key not in seen:
                    result.append(Edge(source, target, weight))
                    seen.add(key)
        return sorted(result, key=lambda edge: (edge.source, edge.target, edge.weight))

    def set_directed(self, directed: bool) -> None:
        """Меняет тип графа, сохраняя существующие рёбра насколько возможно."""
        if self.directed == directed:
            return
        old_edges = self.edges()
        self.directed = directed
        names = self.vertices
        self._adjacency = {name: {} for name in names}
        for edge in old_edges:
            self.add_edge(edge.source, edge.target, edge.weight)

    def ensure_non_negative_weights(self) -> None:
        for edge in self.edges():
            if edge.weight < 0:
                raise ValueError("Алгоритм Дейкстры не работает с отрицательными весами.")

    def to_dict(self) -> dict:
        return {
            "directed": self.directed,
            "vertices": self.vertices,
            "edges": [
                {"from": edge.source, "to": edge.target, "weight": edge.weight}
                for edge in self.edges()
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Graph":
        graph = cls(directed=bool(data.get("directed", False)))
        for vertex in data.get("vertices", []):
            graph.add_vertex(str(vertex))
        for edge in data.get("edges", []):
            graph.add_edge(str(edge["from"]), str(edge["to"]), float(edge.get("weight", 1)))
        return graph

    @classmethod
    def from_edges(
        cls,
        vertices: Iterable[str],
        edges: Iterable[tuple[str, str, float]],
        directed: bool = False,
    ) -> "Graph":
        graph = cls(directed=directed)
        for vertex in vertices:
            graph.add_vertex(vertex)
        for source, target, weight in edges:
            graph.add_edge(source, target, weight)
        return graph
