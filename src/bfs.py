"""Реализация обхода графа в ширину (Breadth-First Search)."""

from __future__ import annotations

from collections import deque

from src.graph import Graph
from src.results import AlgorithmResult, AlgorithmStep


def breadth_first_search(graph: Graph, start: str) -> AlgorithmResult:
    """Обходит достижимые из ``start`` вершины слоями, используя очередь."""
    if not graph.has_vertex(start):
        raise KeyError(f"Стартовая вершина {start!r} не найдена.")

    queue: deque[str] = deque([start])
    visited = {start}
    parents: dict[str, str | None] = {start: None}
    distances = {start: 0.0}
    order: list[str] = []
    steps = [AlgorithmStep(f"Помещаем стартовую вершину {start} в очередь.", active_vertex=start, visited=set(visited))]

    while queue:
        current = queue.popleft()
        order.append(current)
        steps.append(AlgorithmStep(f"Извлекаем вершину {current} из очереди.", active_vertex=current, visited=set(visited)))

        for neighbour, _ in graph.neighbours(current):
            if neighbour in visited:
                continue
            visited.add(neighbour)
            parents[neighbour] = current
            distances[neighbour] = distances[current] + 1
            queue.append(neighbour)
            steps.append(
                AlgorithmStep(
                    f"Находим вершину {neighbour} через {current} и добавляем её в очередь.",
                    active_vertex=neighbour,
                    active_edge=(current, neighbour),
                    visited=set(visited),
                    distances=dict(distances),
                )
            )

    return AlgorithmResult(
        name="Обход в ширину (BFS)",
        order=order,
        parents=parents,
        distances=distances,
        steps=steps,
    )
