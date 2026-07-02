"""Консольная демонстрация ядра проекта для запуска в Docker."""

from pathlib import Path

from src.bfs import breadth_first_search
from src.dfs import depth_first_search
from src.dijkstra import dijkstra_shortest_paths
from src.kruskal import kruskal_minimum_spanning_tree
from src.storage import load_graph


def main() -> None:
    example_path = Path(__file__).resolve().parent.parent / "data" / "example_graph.json"
    graph, _ = load_graph(example_path)
    print("Визуализатор алгоритмов на графах — консольная проверка")
    print("Вершины:", ", ".join(graph.vertices))

    for result in (
        breadth_first_search(graph, "A"),
        depth_first_search(graph, "A"),
        dijkstra_shortest_paths(graph, "A"),
        kruskal_minimum_spanning_tree(graph),
    ):
        print(f"\n{result.name}")
        if result.order:
            print("Порядок:", " -> ".join(result.order))
        if result.distances:
            print("Расстояния:", result.distances)
        if result.selected_edges:
            print("Рёбра МОД:", result.selected_edges)
            print("Общий вес:", result.total_weight)


if __name__ == "__main__":
    main()
