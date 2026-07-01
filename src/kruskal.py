"""Алгоритм Краскала для построения минимального остовного дерева."""

from __future__ import annotations

from src.graph import Graph
from src.results import AlgorithmResult, AlgorithmStep


class DisjointSet:
    """Структура непересекающихся множеств для проверки образования циклов."""

    def __init__(self, vertices: list[str]) -> None:
        self.parent = {vertex: vertex for vertex in vertices}
        self.rank = {vertex: 0 for vertex in vertices}

    def find(self, vertex: str) -> str:
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, first: str, second: str) -> bool:
        first_root = self.find(first)
        second_root = self.find(second)
        if first_root == second_root:
            return False
        if self.rank[first_root] < self.rank[second_root]:
            first_root, second_root = second_root, first_root
        self.parent[second_root] = first_root
        if self.rank[first_root] == self.rank[second_root]:
            self.rank[first_root] += 1
        return True


def kruskal_minimum_spanning_tree(graph: Graph) -> AlgorithmResult:
    """Строит минимальное остовное дерево неориентированного графа."""
    if graph.directed:
        raise ValueError("Алгоритм Краскала в этой версии применяется к неориентированному графу.")

    union_find = DisjointSet(graph.vertices)
    selected: list[tuple[str, str, float]] = []
    total_weight = 0.0
    steps: list[AlgorithmStep] = []

    for edge in sorted(graph.edges(), key=lambda item: (item.weight, item.source, item.target)):
        candidate = (edge.source, edge.target, edge.weight)
        steps.append(
            AlgorithmStep(
                f"Рассматриваем ребро {edge.source} — {edge.target} с весом {edge.weight:g}.",
                active_edge=(edge.source, edge.target),
                selected_edges=list(selected),
            )
        )
        if union_find.union(edge.source, edge.target):
            selected.append(candidate)
            total_weight += edge.weight
            steps.append(
                AlgorithmStep(
                    f"Добавляем ребро {edge.source} — {edge.target}: цикла не возникает.",
                    active_edge=(edge.source, edge.target),
                    selected_edges=list(selected),
                )
            )
        else:
            steps.append(
                AlgorithmStep(
                    f"Пропускаем ребро {edge.source} — {edge.target}: оно образует цикл.",
                    active_edge=(edge.source, edge.target),
                    selected_edges=list(selected),
                )
            )

    visited = set()
    if graph.vertices:
        stack = [graph.vertices[0]]
        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)
            stack.extend(neighbour for neighbour, _ in graph.neighbours(vertex))

    result = AlgorithmResult(
        name="Минимальное остовное дерево (Краскал)",
        selected_edges=selected,
        total_weight=total_weight,
        steps=steps,
    )
    if len(visited) != len(graph.vertices):
        result.steps.append(AlgorithmStep("Граф несвязный: получен минимальный остовный лес.", selected_edges=list(selected)))
    return result
