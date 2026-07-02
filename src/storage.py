"""Сохранение и загрузка графов в JSON-файлах."""

from __future__ import annotations

import json
from pathlib import Path

from src.graph import Graph


def save_graph(path: str | Path, graph: Graph, positions: dict[str, tuple[float, float]]) -> None:
    """Сохраняет структуру графа и координаты вершин в JSON."""
    data = graph.to_dict()
    data["positions"] = {name: [round(x, 2), round(y, 2)] for name, (x, y) in positions.items()}
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_graph(path: str | Path) -> tuple[Graph, dict[str, tuple[float, float]]]:
    """Загружает граф и координаты его вершин из JSON."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    graph = Graph.from_dict(data)
    positions = {
        str(name): (float(point[0]), float(point[1]))
        for name, point in data.get("positions", {}).items()
    }
    return graph, positions
