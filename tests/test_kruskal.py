import pytest

from src.graph import Graph
from src.kruskal import kruskal_minimum_spanning_tree


def make_graph() -> Graph:
    return Graph.from_edges(
        ["A", "B", "C", "D"],
        [("A", "B", 1), ("B", "C", 2), ("A", "C", 4), ("C", "D", 3), ("B", "D", 5)],
    )


def test_kruskal_selects_n_minus_one_edges() -> None:
    result = kruskal_minimum_spanning_tree(make_graph())
    assert len(result.selected_edges) == 3


def test_kruskal_calculates_minimum_total_weight() -> None:
    result = kruskal_minimum_spanning_tree(make_graph())
    assert result.total_weight == 6


def test_kruskal_does_not_select_cycle_edge() -> None:
    result = kruskal_minimum_spanning_tree(make_graph())
    assert ("A", "C", 4.0) not in result.selected_edges


def test_kruskal_rejects_directed_graph() -> None:
    graph = Graph.from_edges(["A", "B"], [("A", "B", 1)], directed=True)
    with pytest.raises(ValueError):
        kruskal_minimum_spanning_tree(graph)


def test_kruskal_returns_empty_tree_for_one_vertex() -> None:
    graph = Graph()
    graph.add_vertex("A")
    result = kruskal_minimum_spanning_tree(graph)
    assert result.selected_edges == []
    assert result.total_weight == 0


def test_kruskal_creates_steps() -> None:
    assert kruskal_minimum_spanning_tree(make_graph()).steps
