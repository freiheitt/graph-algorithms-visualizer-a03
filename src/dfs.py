"""Реализация обхода графа в глубину (Depth-First Search)."""

from __future__ import annotations

from src.graph import Graph
from src.results import AlgorithmResult, AlgorithmStep


def depth_first_search(graph: Graph, start: str) -> AlgorithmResult:
    """Обходит граф в глубину рекурсивно и фиксирует ход выполнения."""
    if not graph.has_vertex(start):
        raise KeyError(f"Стартовая вершина {start!r} не найдена.")

    visited: set[str] = set()
    parents: dict[str, str | None] = {start: None}
    distances: dict[str, float] = {start: 0.0}
    order: list[str] = []
    steps: list[AlgorithmStep] = []

    def visit(vertex: str) -> None:
        visited.add(vertex)
        order.append(vertex)
        steps.append(AlgorithmStep(f"Заходим в вершину {vertex}.", active_vertex=vertex, visited=set(visited), distances=dict(distances)))

        for neighbour, _ in graph.neighbours(vertex):
            if neighbour in visited:
                continue
            parents[neighbour] = vertex
            distances[neighbour] = distances[vertex] + 1
            steps.append(
                AlgorithmStep(
                    f"Переходим по ребру {vertex} — {neighbour}.",
                    active_vertex=neighbour,
                    active_edge=(vertex, neighbour),
                    visited=set(visited),
                    distances=dict(distances),
                )
            )
            visit(neighbour)

    visit(start)
    return AlgorithmResult(
        name="Обход в глубину (DFS)",
        order=order,
        parents=parents,
        distances=distances,
        steps=steps,
    )
