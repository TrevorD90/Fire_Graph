# app/Controller.py
import tkinter as tk
from tkinter import ttk, filedialog
from app.State import AppState
from app.Plot_View import PlotFrame
from app.Settings_Panel import SettingsPanel

def run_app():
    state = AppState()

    root = tk.Tk()
    root.title("Inverse Axis Plotter")
    root.geometry("1100x800")

    # Layout containers
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    # Plot + Settings
    plot_frame = PlotFrame(frame, state)
    settings_panel = SettingsPanel(
        frame,
        state,
        on_redraw=plot_frame.redraw,
        reset_view_cb=plot_frame.reset_view,
        save_png_cb=plot_frame.save_png,   # <-- wire the button
    )

    plot_frame.grid(row=0, column=0, sticky="nsew")
    settings_panel.grid(row=0, column=1, sticky="ns")

    # Menu
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Open CSV…", command=lambda: _menu_open_csv(root, state, plot_frame))
    file_menu.add_separator()
    file_menu.add_command(label="Export PNG…", command=plot_frame.save_png)  # <-- new
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)

    plot_frame.redraw()
    root.mainloop()

def _menu_open_csv(root, state: AppState, plot_frame: PlotFrame):
    from .Data_Loader import load_csv_mapped
    from .Plotter import compute_bounds
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
    # Reset to data extents on load
    state.use_manual_axes = False
    plot_frame.redraw()
