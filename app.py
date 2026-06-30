"""Точка входа учебного настольного приложения."""

import tkinter as tk
from tkinter import ttk


def main() -> None:
    root = tk.Tk()
    root.title("Визуализатор алгоритмов на графах - А-03")
    root.geometry("760x420")
    root.minsize(620, 360)

    frame = ttk.Frame(root, padding=32)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="Визуализатор алгоритмов на графах",
        font=("Segoe UI", 22, "bold"),
    ).pack(anchor="w", pady=(0, 8))
    ttk.Label(
        frame,
        text="Учебная практика - вариант А-03",
        font=("Segoe UI", 12),
    ).pack(anchor="w")

    ttk.Separator(frame).pack(fill="x", pady=22)
    ttk.Label(
        frame,
        text=(
            "На этом этапе подготовлен каркас настольного приложения.\n"
            "Далее будут добавлены модель графа, алгоритмы и визуализация шагов."
        ),
        justify="left",
        font=("Segoe UI", 11),
    ).pack(anchor="w")

    root.mainloop()


if __name__ == "__main__":
    main()
