import pytest

from src.graph import Graph


def test_add_vertex_and_prevent_duplicate() -> None:
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("A")
    assert graph.vertices == ["A"]


def test_empty_vertex_name_is_rejected() -> None:
    with pytest.raises(ValueError):
        Graph().add_vertex("   ")


def test_add_undirected_edge_adds_both_directions() -> None:
    graph = Graph.from_edges(["A", "B"], [("A", "B", 3)])
    assert graph.neighbours("A") == [("B", 3.0)]
    assert graph.neighbours("B") == [("A", 3.0)]


def test_directed_edge_has_one_direction() -> None:
    graph = Graph.from_edges(["A", "B"], [("A", "B", 3)], directed=True)
    assert graph.neighbours("A") == [("B", 3.0)]
    assert graph.neighbours("B") == []


def test_edges_returns_undirected_edge_once() -> None:
    graph = Graph.from_edges(["A", "B"], [("A", "B", 3)])
    assert len(graph.edges()) == 1


def test_remove_vertex_removes_incident_edges() -> None:
    graph = Graph.from_edges(["A", "B", "C"], [("A", "B", 1), ("B", "C", 2)])
    graph.remove_vertex("B")
    assert graph.vertices == ["A", "C"]
    assert graph.edges() == []


def test_remove_edge() -> None:
    graph = Graph.from_edges(["A", "B"], [("A", "B", 1)])
    graph.remove_edge("A", "B")
    assert graph.edges() == []


def test_edge_requires_existing_vertices() -> None:
    graph = Graph()
    graph.add_vertex("A")
    with pytest.raises(KeyError):
        graph.add_edge("A", "B", 1)


def test_self_loop_is_rejected() -> None:
    graph = Graph()
    graph.add_vertex("A")
    with pytest.raises(ValueError):
        graph.add_edge("A", "A", 1)


def test_to_dict_and_from_dict_round_trip() -> None:
    original = Graph.from_edges(["A", "B"], [("A", "B", 2.5)])
    restored = Graph.from_dict(original.to_dict())
    assert restored.to_dict() == original.to_dict()


def test_set_directed_changes_edge_interpretation() -> None:
    graph = Graph.from_edges(["A", "B"], [("A", "B", 1)])
    graph.set_directed(True)
    assert graph.neighbours("A") == [("B", 1.0)]
    assert graph.neighbours("B") == []
