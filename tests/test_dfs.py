import pytest

from src.dfs import depth_first_search
from src.graph import Graph


def make_graph() -> Graph:
    return Graph.from_edges(
        ["A", "B", "C", "D", "E"],
        [("A", "B", 1), ("A", "C", 1), ("B", "D", 1), ("C", "E", 1)],
    )


def test_dfs_follows_one_branch_before_returning() -> None:
    result = depth_first_search(make_graph(), "A")
    assert result.order == ["A", "B", "D", "C", "E"]


def test_dfs_records_parent_relations() -> None:
    result = depth_first_search(make_graph(), "A")
    assert result.parents["D"] == "B"
    assert result.parents["E"] == "C"


def test_dfs_distance_is_depth_in_search_tree() -> None:
    result = depth_first_search(make_graph(), "A")
    assert result.distances["D"] == 2


def test_dfs_does_not_visit_disconnected_vertex() -> None:
    graph = make_graph()
    graph.add_vertex("Z")
    assert "Z" not in depth_first_search(graph, "A").order


def test_dfs_rejects_unknown_start() -> None:
    with pytest.raises(KeyError):
        depth_first_search(make_graph(), "Z")


def test_dfs_creates_visualisation_steps() -> None:
    result = depth_first_search(make_graph(), "A")
    assert any(step.active_edge == ("A", "B") for step in result.steps)
