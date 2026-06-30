"""Общие типы результатов для пошаговой визуализации алгоритмов."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import inf


@dataclass
class AlgorithmStep:
    """Один понятный шаг выполнения алгоритма."""

    message: str
    active_vertex: str | None = None
    active_edge: tuple[str, str] | None = None
    visited: set[str] = field(default_factory=set)
    selected_edges: list[tuple[str, str, float]] = field(default_factory=list)
    distances: dict[str, float] = field(default_factory=dict)


@dataclass
class AlgorithmResult:
    """Результат алгоритма и последовательность шагов для интерфейса."""

    name: str
    order: list[str] = field(default_factory=list)
    parents: dict[str, str | None] = field(default_factory=dict)
    distances: dict[str, float] = field(default_factory=dict)
    selected_edges: list[tuple[str, str, float]] = field(default_factory=list)
    total_weight: float | None = None
    steps: list[AlgorithmStep] = field(default_factory=list)


def display_distance(value: float) -> str:
    return "∞" if value == inf else f"{value:g}"
