import tkinter as tk
from tkinter import filedialog
import pandas as pd

def build_settings_tab(frame, state):
    tk.Button(frame, text="Load CSV File", command=lambda: load_data(state)).pack(pady=10)

    axis_names = {
        "Bottom X": "Temperature",
        "Top X": "RH",
        "Left Y": "Wind",
        "Right Y": "Fuel"
    }

    for label, key in axis_names.items():
        var = tk.StringVar()
        state.axis_labels[key] = var

        row = tk.Frame(frame)
        row.pack(pady=4, padx=10, anchor='w')
        tk.Label(row, text=label + ":").pack(side=tk.LEFT)
        tk.Entry(row, width=15, textvariable=var).pack(side=tk.LEFT)

        var.trace_add("write", lambda *_, k=key: on_update(state))

def load_data(state):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    try:
        state.data = pd.read_csv(file_path)
        state.graph.plot_data()
    except Exception as e:
        print(f"Failed to load CSV: {e}")

def on_update(state):
    if state.graph:
        state.graph.plot_data()
