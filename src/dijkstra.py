"""Алгоритм Дейкстры для кратчайших путей с неотрицательными весами."""

from __future__ import annotations

import heapq
from math import inf

from src.graph import Graph
from src.results import AlgorithmResult, AlgorithmStep


def dijkstra_shortest_paths(graph: Graph, start: str) -> AlgorithmResult:
    """Находит кратчайшие расстояния от ``start`` до достижимых вершин."""
    if not graph.has_vertex(start):
        raise KeyError(f"Стартовая вершина {start!r} не найдена.")
    graph.ensure_non_negative_weights()

    distances = {vertex: inf for vertex in graph.vertices}
    distances[start] = 0.0
    parents: dict[str, str | None] = {start: None}
    queue: list[tuple[float, str]] = [(0.0, start)]
    finalised: set[str] = set()
    order: list[str] = []
    steps = [AlgorithmStep(f"Расстояние до стартовой вершины {start} равно 0.", active_vertex=start, distances=dict(distances))]

    while queue:
        current_distance, current = heapq.heappop(queue)
        if current in finalised:
            continue
        finalised.add(current)
        order.append(current)
        steps.append(
            AlgorithmStep(
                f"Фиксируем кратчайшее расстояние до вершины {current}: {current_distance:g}.",
                active_vertex=current,
                visited=set(finalised),
                distances=dict(distances),
            )
        )

        for neighbour, weight in graph.neighbours(current):
            candidate = current_distance + weight
            if candidate < distances[neighbour]:
                distances[neighbour] = candidate
                parents[neighbour] = current
                heapq.heappush(queue, (candidate, neighbour))
                steps.append(
                    AlgorithmStep(
                        f"Улучшаем путь до {neighbour}: {current_distance:g} + {weight:g} = {candidate:g}.",
                        active_vertex=neighbour,
                        active_edge=(current, neighbour),
                        visited=set(finalised),
                        distances=dict(distances),
                    )
                )

    return AlgorithmResult(
        name="Алгоритм Дейкстры",
        order=order,
        parents=parents,
        distances=distances,
        steps=steps,
    )
