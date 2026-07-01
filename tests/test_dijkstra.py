import pytest

from src.dijkstra import dijkstra_shortest_paths
from src.graph import Graph


def make_graph() -> Graph:
    return Graph.from_edges(
        ["A", "B", "C", "D", "E"],
        [("A", "B", 4), ("A", "C", 1), ("C", "B", 2), ("B", "D", 1), ("C", "D", 5)],
    )


def test_dijkstra_finds_shortest_distances() -> None:
    result = dijkstra_shortest_paths(make_graph(), "A")
    assert result.distances["A"] == 0
    assert result.distances["B"] == 3
    assert result.distances["D"] == 4


def test_dijkstra_records_best_parents() -> None:
    result = dijkstra_shortest_paths(make_graph(), "A")
    assert result.parents["B"] == "C"
    assert result.parents["D"] == "B"


def test_dijkstra_leaves_unreachable_distance_as_infinity() -> None:
    graph = make_graph()
    graph.add_vertex("Z")
    result = dijkstra_shortest_paths(graph, "A")
    assert result.distances["Z"] == float("inf")


def test_dijkstra_rejects_negative_weights() -> None:
    graph = Graph.from_edges(["A", "B"], [("A", "B", -1)])
    with pytest.raises(ValueError):
        dijkstra_shortest_paths(graph, "A")


def test_dijkstra_rejects_unknown_start() -> None:
    with pytest.raises(KeyError):
        dijkstra_shortest_paths(make_graph(), "Z")


def test_dijkstra_creates_steps() -> None:
    result = dijkstra_shortest_paths(make_graph(), "A")
    assert any(step.active_edge == ("A", "C") for step in result.steps)
