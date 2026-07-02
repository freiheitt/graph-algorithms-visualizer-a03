import pytest

from src.bfs import breadth_first_search
from src.dijkstra import dijkstra_shortest_paths
from src.graph import Graph
from src.kruskal import kruskal_minimum_spanning_tree


def test_bfs_on_single_vertex_graph() -> None:
    graph = Graph()
    graph.add_vertex("A")
    assert breadth_first_search(graph, "A").order == ["A"]


def test_dijkstra_on_single_vertex_graph() -> None:
    graph = Graph()
    graph.add_vertex("A")
    assert dijkstra_shortest_paths(graph, "A").distances == {"A": 0.0}


def test_kruskal_on_disconnected_graph_returns_forest() -> None:
    graph = Graph.from_edges(["A", "B", "C", "D"], [("A", "B", 1), ("C", "D", 2)])
    result = kruskal_minimum_spanning_tree(graph)
    assert result.total_weight == 3
    assert len(result.selected_edges) == 2


def test_graph_remove_missing_vertex_raises_key_error() -> None:
    with pytest.raises(KeyError):
        Graph().remove_vertex("Missing")


def test_graph_remove_missing_edge_raises_key_error() -> None:
    graph = Graph.from_edges(["A", "B"], [])
    with pytest.raises(KeyError):
        graph.remove_edge("A", "B")
