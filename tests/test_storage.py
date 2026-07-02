from src.graph import Graph
from src.storage import load_graph, save_graph


def test_save_and_load_graph_with_positions(tmp_path) -> None:
    graph = Graph.from_edges(["A", "B"], [("A", "B", 2)])
    path = tmp_path / "graph.json"
    save_graph(path, graph, {"A": (10, 20), "B": (30, 40)})

    restored, positions = load_graph(path)
    assert restored.to_dict() == graph.to_dict()
    assert positions == {"A": (10.0, 20.0), "B": (30.0, 40.0)}


def test_load_preserves_directed_type(tmp_path) -> None:
    graph = Graph.from_edges(["A", "B"], [("A", "B", 1)], directed=True)
    path = tmp_path / "directed.json"
    save_graph(path, graph, {})
    restored, _ = load_graph(path)
    assert restored.directed is True
