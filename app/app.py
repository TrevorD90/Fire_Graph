import tkinter as tk
from tkinter import ttk
from .rx_tab import build_rx_tab
from .settings_tab import build_settings_tab
from .graph_view import GraphView
from .state import AppState

def launch_app():
    root = tk.Tk()
    root.title("Rx Line Graphing App")
    root.geometry("1000x600")

    state = AppState()

    left_frame = tk.Frame(root, width=700)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right_frame = tk.Frame(root, width=300)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # Notebook Tabs
    notebook = ttk.Notebook(right_frame)
    tab_rx = ttk.Frame(notebook)
    tab_settings = ttk.Frame(notebook)
    notebook.add(tab_rx, text="Rx Lines")
    notebook.add(tab_settings, text="Settings")
    notebook.pack(fill=tk.BOTH, expand=True)

    # Graph and Tabs
    graph_view = GraphView(left_frame, state)
    state.graph = graph_view

    build_rx_tab(tab_rx, state)
    build_settings_tab(tab_settings, state)

    root.mainloop()
