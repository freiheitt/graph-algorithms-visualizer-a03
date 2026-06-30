import pytest

from src.bfs import breadth_first_search
from src.graph import Graph


def make_graph() -> Graph:
    return Graph.from_edges(
        ["A", "B", "C", "D", "E"],
        [("A", "B", 1), ("A", "C", 1), ("B", "D", 1), ("C", "E", 1)],
    )


def test_bfs_visits_vertices_by_layers() -> None:
    result = breadth_first_search(make_graph(), "A")
    assert result.order == ["A", "B", "C", "D", "E"]


def test_bfs_records_parents() -> None:
    result = breadth_first_search(make_graph(), "A")
    assert result.parents == {"A": None, "B": "A", "C": "A", "D": "B", "E": "C"}


def test_bfs_counts_number_of_edges_from_start() -> None:
    result = breadth_first_search(make_graph(), "A")
    assert result.distances["D"] == 2


def test_bfs_does_not_visit_disconnected_vertex() -> None:
    graph = make_graph()
    graph.add_vertex("Z")
    assert "Z" not in breadth_first_search(graph, "A").order


def test_bfs_rejects_missing_start_vertex() -> None:
    with pytest.raises(KeyError):
        breadth_first_search(make_graph(), "Z")


def test_bfs_creates_steps_for_visualisation() -> None:
    result = breadth_first_search(make_graph(), "A")
    assert result.steps
    assert any(step.active_edge == ("A", "B") for step in result.steps)
