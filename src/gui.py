"""Настольный интерфейс визуализатора алгоритмов на графах."""

from __future__ import annotations

import math
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from src.bfs import breadth_first_search
from src.dfs import depth_first_search
from src.dijkstra import dijkstra_shortest_paths
from src.graph import Graph
from src.kruskal import kruskal_minimum_spanning_tree
from src.results import AlgorithmResult, AlgorithmStep, display_distance
from src.storage import load_graph, save_graph


class GraphVisualizerApp:
    """Главное окно программы и редактор графа."""

    NODE_RADIUS = 22

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Визуализатор алгоритмов на графах — вариант А-03")
        self.root.geometry("1320x790")
        self.root.minsize(1050, 650)

        self.graph = Graph(directed=False)
        self.positions: dict[str, tuple[float, float]] = {}
        self.current_result: AlgorithmResult | None = None
        self.step_index = -1
        self.auto_running = False
        self.dragged_vertex: str | None = None

        self._build_layout()
        self._load_builtin_example()

    def run(self) -> None:
        self.root.mainloop()

    def _build_layout(self) -> None:
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        controls = ttk.Frame(self.root, padding=12)
        controls.grid(row=0, column=0, sticky="ns")
        canvas_frame = ttk.Frame(self.root, padding=(0, 12, 12, 12))
        canvas_frame.grid(row=0, column=1, sticky="nsew")
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)

        ttk.Label(controls, text="Редактор графа", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 8))

        self.directed_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            controls,
            text="Ориентированный граф",
            variable=self.directed_var,
            command=self._change_graph_type,
        ).pack(anchor="w", pady=(0, 10))

        vertex_box = ttk.LabelFrame(controls, text="Вершины", padding=8)
        vertex_box.pack(fill="x", pady=(0, 8))
        self.vertex_name_var = tk.StringVar()
        ttk.Entry(vertex_box, textvariable=self.vertex_name_var, width=18).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(vertex_box, text="Добавить", command=self._add_vertex).grid(row=0, column=1)
        ttk.Button(vertex_box, text="Удалить", command=self._remove_vertex).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))

        edge_box = ttk.LabelFrame(controls, text="Рёбра", padding=8)
        edge_box.pack(fill="x", pady=(0, 8))
        self.source_var = tk.StringVar()
        self.target_var = tk.StringVar()
        self.weight_var = tk.StringVar(value="1")
        self.source_box = ttk.Combobox(edge_box, textvariable=self.source_var, width=15, state="readonly")
        self.target_box = ttk.Combobox(edge_box, textvariable=self.target_var, width=15, state="readonly")
        ttk.Label(edge_box, text="Откуда").grid(row=0, column=0, sticky="w")
        self.source_box.grid(row=1, column=0, sticky="ew")
        ttk.Label(edge_box, text="Куда").grid(row=2, column=0, sticky="w", pady=(5, 0))
        self.target_box.grid(row=3, column=0, sticky="ew")
        ttk.Label(edge_box, text="Вес").grid(row=4, column=0, sticky="w", pady=(5, 0))
        ttk.Entry(edge_box, textvariable=self.weight_var, width=16).grid(row=5, column=0, sticky="ew")
        ttk.Button(edge_box, text="Добавить ребро", command=self._add_edge).grid(row=6, column=0, sticky="ew", pady=(7, 0))
        ttk.Button(edge_box, text="Удалить выбранное", command=self._remove_selected_edge).grid(row=8, column=0, sticky="ew", pady=(5, 0))
        self.edge_list = tk.Listbox(edge_box, height=7, width=25, exportselection=False)
        self.edge_list.grid(row=7, column=0, sticky="ew", pady=(7, 0))

        algorithm_box = ttk.LabelFrame(controls, text="Алгоритм", padding=8)
        algorithm_box.pack(fill="x", pady=(0, 8))
        self.algorithm_var = tk.StringVar(value="BFS")
        ttk.Combobox(
            algorithm_box,
            textvariable=self.algorithm_var,
            values=["BFS", "DFS", "Дейкстра", "Краскал"],
            state="readonly",
            width=16,
        ).pack(fill="x")
        ttk.Label(algorithm_box, text="Стартовая вершина").pack(anchor="w", pady=(6, 0))
        self.start_var = tk.StringVar()
        self.start_box = ttk.Combobox(algorithm_box, textvariable=self.start_var, state="readonly", width=16)
        self.start_box.pack(fill="x")
        ttk.Button(algorithm_box, text="Запустить", command=self._run_algorithm).pack(fill="x", pady=(7, 0))

        step_box = ttk.LabelFrame(controls, text="Шаги", padding=8)
        step_box.pack(fill="x", pady=(0, 8))
        row = ttk.Frame(step_box)
        row.pack(fill="x")
        ttk.Button(row, text="◀", width=5, command=self._previous_step).pack(side="left")
        ttk.Button(row, text="▶", width=5, command=self._next_step).pack(side="left", padx=5)
        self.auto_button = ttk.Button(row, text="Авто", command=self._toggle_auto)
        self.auto_button.pack(side="left")
        self.step_label = ttk.Label(step_box, text="Шаг: —")
        self.step_label.pack(anchor="w", pady=(6, 0))
        ttk.Label(step_box, text="Оранжевым показан текущий шаг.", foreground="#a34a11").pack(anchor="w", pady=(2, 0))

        file_box = ttk.LabelFrame(controls, text="Файл", padding=8)
        file_box.pack(fill="x")
        ttk.Button(file_box, text="Загрузить JSON", command=self._load_from_file).pack(fill="x")
        ttk.Button(file_box, text="Сохранить JSON", command=self._save_to_file).pack(fill="x", pady=5)
        ttk.Button(file_box, text="Загрузить пример", command=self._load_builtin_example).pack(fill="x")

        self.canvas = tk.Canvas(canvas_frame, bg="#fbfcfe", highlightthickness=1, highlightbackground="#c7cbd1")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<ButtonPress-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._drag_vertex)
        self.canvas.bind("<ButtonRelease-1>", self._stop_drag)

        result_frame = ttk.LabelFrame(canvas_frame, text="Результат и пояснение текущего шага", padding=7)
        result_frame.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        self.result_text = ScrolledText(result_frame, height=9, wrap="word", font=("Consolas", 10))
        self.result_text.pack(fill="x")
        self.result_text.configure(state="disabled")

    def _load_builtin_example(self) -> None:
        sample = Path(__file__).resolve().parent.parent / "data" / "example_graph.json"
        if sample.exists():
            self.graph, self.positions = load_graph(sample)
        else:
            self.graph = Graph()
            self.positions = {}
        self.directed_var.set(self.graph.directed)
        self._reset_algorithm_state()
        self._refresh_controls()

    def _change_graph_type(self) -> None:
        self.graph.set_directed(self.directed_var.get())
        self._reset_algorithm_state()
        self._refresh_controls()

    def _add_vertex(self) -> None:
        try:
            name = self.vertex_name_var.get().strip()
            self.graph.add_vertex(name)
            self.positions[name] = self._automatic_position(len(self.graph.vertices) - 1)
            self.vertex_name_var.set("")
            self._reset_algorithm_state()
            self._refresh_controls()
        except (ValueError, KeyError) as error:
            messagebox.showerror("Не удалось добавить вершину", str(error))

    def _remove_vertex(self) -> None:
        try:
            name = self.vertex_name_var.get().strip() or self.start_var.get()
            self.graph.remove_vertex(name)
            self.positions.pop(name, None)
            self._reset_algorithm_state()
            self._refresh_controls()
        except (ValueError, KeyError) as error:
            messagebox.showerror("Не удалось удалить вершину", str(error))

    def _add_edge(self) -> None:
        try:
            self.graph.add_edge(self.source_var.get(), self.target_var.get(), float(self.weight_var.get()))
            self._reset_algorithm_state()
            self._refresh_controls()
        except (ValueError, KeyError) as error:
            messagebox.showerror("Не удалось добавить ребро", str(error))

    def _remove_selected_edge(self) -> None:
        selection = self.edge_list.curselection()
        if not selection:
            messagebox.showinfo("Выберите ребро", "Сначала выберите ребро в списке.")
            return
        edge = self.graph.edges()[selection[0]]
        try:
            self.graph.remove_edge(edge.source, edge.target)
            self._reset_algorithm_state()
            self._refresh_controls()
        except KeyError as error:
            messagebox.showerror("Не удалось удалить ребро", str(error))

    def _run_algorithm(self) -> None:
        try:
            selected = self.algorithm_var.get()
            if selected == "BFS":
                self.current_result = breadth_first_search(self.graph, self.start_var.get())
            elif selected == "DFS":
                self.current_result = depth_first_search(self.graph, self.start_var.get())
            elif selected == "Дейкстра":
                self.current_result = dijkstra_shortest_paths(self.graph, self.start_var.get())
            else:
                self.current_result = kruskal_minimum_spanning_tree(self.graph)
            self.step_index = 0 if self.current_result.steps else -1
            self._show_result()
            self._draw_graph()
        except (ValueError, KeyError) as error:
            messagebox.showerror("Алгоритм не запущен", str(error))

    def _reset_algorithm_state(self) -> None:
        self.current_result = None
        self.step_index = -1
        self.auto_running = False
        if hasattr(self, "auto_button"):
            self.auto_button.configure(text="Авто")

    def _previous_step(self) -> None:
        if self.current_result and self.step_index > 0:
            self.step_index -= 1
            self._show_result()
            self._draw_graph()

    def _next_step(self) -> None:
        if self.current_result and self.step_index < len(self.current_result.steps) - 1:
            self.step_index += 1
            self._show_result()
            self._draw_graph()

    def _toggle_auto(self) -> None:
        if not self.current_result or not self.current_result.steps:
            messagebox.showinfo("Нет шагов", "Сначала запустите алгоритм.")
            return
        self.auto_running = not self.auto_running
        self.auto_button.configure(text="Стоп" if self.auto_running else "Авто")
        if self.auto_running:
            self._play_steps()

    def _play_steps(self) -> None:
        if not self.auto_running:
            return
        if self.step_index < len(self.current_result.steps) - 1:
            self._next_step()
            self.root.after(800, self._play_steps)
        else:
            self.auto_running = False
            self.auto_button.configure(text="Авто")

    def _show_result(self) -> None:
        if not self.current_result:
            self._set_result_text("Запустите один из алгоритмов, чтобы увидеть результат.")
            self.step_label.configure(text="Шаг: —")
            return

        result = self.current_result
        lines = [f"{result.name}"]
        if result.order:
            lines.append("Порядок обработки: " + " → ".join(result.order))
        if result.distances:
            distance_line = ", ".join(f"{name}: {display_distance(value)}" for name, value in sorted(result.distances.items()))
            lines.append("Расстояния: " + distance_line)
        if result.selected_edges:
            edges_text = ", ".join(f"{a}—{b} ({weight:g})" for a, b, weight in result.selected_edges)
            lines.append("Выбранные рёбра: " + edges_text)
        if result.total_weight is not None:
            lines.append(f"Суммарный вес: {result.total_weight:g}")

        if 0 <= self.step_index < len(result.steps):
            step = result.steps[self.step_index]
            lines.extend(["", f"Шаг {self.step_index + 1}/{len(result.steps)}: {step.message}"])
            self.step_label.configure(text=f"Шаг: {self.step_index + 1} из {len(result.steps)}")
        else:
            self.step_label.configure(text="Шаг: —")
        self._set_result_text("\n".join(lines))

    def _set_result_text(self, text: str) -> None:
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", text)
        self.result_text.configure(state="disabled")

    def _refresh_controls(self) -> None:
        vertices = self.graph.vertices
        self.source_box["values"] = vertices
        self.target_box["values"] = vertices
        self.start_box["values"] = vertices
        if vertices:
            if self.source_var.get() not in vertices:
                self.source_var.set(vertices[0])
            if self.target_var.get() not in vertices:
                self.target_var.set(vertices[min(1, len(vertices) - 1)])
            if self.start_var.get() not in vertices:
                self.start_var.set(vertices[0])

        self.edge_list.delete(0, "end")
        for edge in self.graph.edges():
            connector = "→" if self.graph.directed else "—"
            self.edge_list.insert("end", f"{edge.source} {connector} {edge.target}   вес: {edge.weight:g}")

        self._show_result()
        self._draw_graph()

    def _current_step(self) -> AlgorithmStep | None:
        if self.current_result and 0 <= self.step_index < len(self.current_result.steps):
            return self.current_result.steps[self.step_index]
        return None

    def _draw_graph(self) -> None:
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 720)
        height = max(self.canvas.winfo_height(), 450)
        if width <= 1:
            width, height = 850, 500
        for index, vertex in enumerate(self.graph.vertices):
            self.positions.setdefault(vertex, self._automatic_position(index, width, height))

        step = self._current_step()
        selected_edges = set()
        active_edge = None
        visited = set()
        active_vertex = None
        if step:
            selected_edges = {tuple(sorted((first, second))) for first, second, _ in step.selected_edges}
            active_edge = step.active_edge
            visited = step.visited
            active_vertex = step.active_vertex

        for edge in self.graph.edges():
            x1, y1 = self.positions[edge.source]
            x2, y2 = self.positions[edge.target]
            normalized = tuple(sorted((edge.source, edge.target)))
            colour = "#87909c"
            thickness = 2
            if normalized in selected_edges:
                colour, thickness = "#148a52", 4
            if active_edge and {edge.source, edge.target} == set(active_edge):
                colour, thickness = "#ef7d32", 4
            arrow = tk.LAST if self.graph.directed else tk.NONE
            self.canvas.create_line(x1, y1, x2, y2, fill=colour, width=thickness, arrow=arrow)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_rectangle(mx - 16, my - 11, mx + 16, my + 11, fill="#fbfcfe", outline="")
            self.canvas.create_text(mx, my, text=f"{edge.weight:g}", font=("Segoe UI", 10, "bold"), fill="#28303a")

        for vertex in self.graph.vertices:
            x, y = self.positions[vertex]
            fill = "#e8edf3"
            outline = "#34495e"
            width_line = 2
            if vertex in visited:
                fill = "#bfe6cf"
                outline = "#26734d"
            if vertex == active_vertex:
                fill = "#ffd9b8"
                outline = "#d96015"
                width_line = 4
            self.canvas.create_oval(x - self.NODE_RADIUS, y - self.NODE_RADIUS, x + self.NODE_RADIUS, y + self.NODE_RADIUS, fill=fill, outline=outline, width=width_line, tags=(f"node:{vertex}", "node"))
            self.canvas.create_text(x, y, text=vertex, font=("Segoe UI", 11, "bold"), tags=(f"node:{vertex}", "node"))


        legend = "Серый — обычное состояние   •   Зелёный — посещено/выбрано   •   Оранжевый — текущий шаг"
        self.canvas.create_text(12, 14, anchor="w", text=legend, fill="#59636f", font=("Segoe UI", 9))

        if not self.graph.vertices:
            self.canvas.create_text(width / 2, height / 2, text="Добавьте вершины, чтобы начать работу с графом.", fill="#59636f", font=("Segoe UI", 13))

    def _automatic_position(self, index: int, width: int = 850, height: int = 500) -> tuple[float, float]:
        count = max(len(self.graph.vertices), 1)
        angle = -math.pi / 2 + 2 * math.pi * index / max(count, 5)
        radius = min(width, height) * 0.31
        return width / 2 + radius * math.cos(angle), height / 2 + radius * math.sin(angle)

    def _find_vertex_at(self, x: float, y: float) -> str | None:
        for vertex, (vx, vy) in self.positions.items():
            if (x - vx) ** 2 + (y - vy) ** 2 <= self.NODE_RADIUS ** 2:
                return vertex
        return None

    def _start_drag(self, event: tk.Event) -> None:
        self.dragged_vertex = self._find_vertex_at(event.x, event.y)

    def _drag_vertex(self, event: tk.Event) -> None:
        if self.dragged_vertex:
            self.positions[self.dragged_vertex] = (event.x, event.y)
            self._draw_graph()

    def _stop_drag(self, event: tk.Event) -> None:
        self.dragged_vertex = None

    def _save_to_file(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        save_graph(path, self.graph, self.positions)
        messagebox.showinfo("Сохранение", "Граф сохранён в JSON-файл.")

    def _load_from_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            self.graph, self.positions = load_graph(path)
            self.directed_var.set(self.graph.directed)
            self._reset_algorithm_state()
            self._refresh_controls()
        except (OSError, ValueError, KeyError) as error:
            messagebox.showerror("Не удалось загрузить файл", str(error))
