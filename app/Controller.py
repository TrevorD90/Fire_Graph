import tkinter as tk
from tkinter import ttk, filedialog
from .state import AppState
from .plot_view import PlotFrame
from .settings_panel import SettingsPanel

def run_app():
    state = AppState()

    root = tk.Tk()
    root.title("Inverse Axis Plotter")
    root.geometry("1100x800")

    # Menu (File → Open, Exit)
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Open CSV…", command=lambda: _menu_open_csv(root, state))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)

    # Layout: left plot (expands), right settings (fixed width)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    plot_frame = PlotFrame(frame, state)
    settings_panel = SettingsPanel(frame, state, on_redraw=plot_frame.redraw)

    plot_frame.grid(row=0, column=0, sticky="nsew")
    settings_panel.grid(row=0, column=1, sticky="ns")

    plot_frame.redraw()
    root.mainloop()

def _menu_open_csv(root, state: AppState):
    # forward to the settings panel’s handler if you prefer;
    # or directly choose here and trigger redraw via a custom event.
    from .data_loader import load_csv_mapped
    from .plotter import compute_bounds

    p = filedialog.askopenfilename(
        parent=root,
        title="Choose CSV",
        filetypes=[("CSV files","*.csv"), ("All files","*.*")]
    )
    if not p:
        return

    state.csv_path = p
    state.df = load_csv_mapped(p)
    compute_bounds(state)
    # notify any listeners
    root.event_generate("<<RedrawPlot>>", when="tail")
