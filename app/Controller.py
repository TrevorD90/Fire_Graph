import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .State import AppState
from .Plot_View import PlotFrame
from .Settings_Panel import SettingsPanel
from .Data_Loader import load_csv_mapped
from .Plotter import compute_bounds

def run_app():
    state = AppState()

    root = tk.Tk()
    root.title("Inverse Axis Plotter")
    root.geometry("1100x800")

    # Layout
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    plot_frame = PlotFrame(frame, state)
    settings_panel = SettingsPanel(
        frame,
        state,
        on_redraw=plot_frame.redraw,
        reset_view_cb=plot_frame.reset_view,  # keep Reset View button working
    )

    plot_frame.grid(row=0, column=0, sticky="nsew")
    settings_panel.grid(row=0, column=1, sticky="ns")

    # Menu (File → Open, Exit)
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Open CSV…", command=lambda: _menu_open_csv(root, state, plot_frame, settings_panel))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)

    plot_frame.redraw()
    root.mainloop()

def _menu_open_csv(root, state: AppState, plot_frame: PlotFrame, settings_panel: SettingsPanel):
    p = filedialog.askopenfilename(
        parent=root,
        title="Choose CSV",
        filetypes=[("CSV files","*.csv"), ("All files","*.*")]
    )
    if not p:
        return
    try:
        state.csv_path = p
        state.df = load_csv_mapped(p)
        compute_bounds(state)
    except Exception as e:
        messagebox.showerror("Load error", str(e))
        return

    # reflect in UI and redraw
    try:
        settings_panel.path_lbl.configure(text=p)
        # Optionally refresh the values readout if present
        if hasattr(settings_panel, "_update_vals_label"):
            settings_panel._update_vals_label()
    except Exception:
        pass

    plot_frame.redraw()
