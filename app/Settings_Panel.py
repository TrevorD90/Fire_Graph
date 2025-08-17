# app/Settings_Panel.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .State import AppState
from .Data_Loader import load_csv_mapped
from .Plotter import compute_bounds

class SettingsPanel(tk.Frame):
    def __init__(self, parent, state: AppState, on_redraw, reset_view_cb=None):
        super().__init__(parent, bg="#f6f6f6", padx=10, pady=10, width=320)
        self.state = state
        self.on_redraw = on_redraw
        self.reset_view_cb = reset_view_cb

        # toggles
        self.var_show_x1y1 = tk.BooleanVar(value=state.show_x1y1)
        self.var_show_x2y2 = tk.BooleanVar(value=state.show_x2y2)
        self.var_show_time = tk.BooleanVar(value=state.show_time_labels)
        self.var_show_grid = tk.BooleanVar(value=state.show_grid)
        self.var_use_manual = tk.BooleanVar(value=state.use_manual_axes)

        ttk.Label(self, text="Settings", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))

        # file chooser
        ttk.Button(self, text="Choose CSV…", command=self.choose_csv).pack(anchor="w", pady=4)
        self.path_lbl = ttk.Label(self, text="(no file)")
        self.path_lbl.pack(anchor="w")

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=8)

        # toggles
        ttk.Checkbutton(self, text="Show Temp/Wind (X1–Y1)",
                        variable=self.var_show_x1y1, command=self._toggle_points).pack(anchor="w")
        ttk.Checkbutton(self, text="Show RH/Fuel (X2–Y2)",
                        variable=self.var_show_x2y2, command=self._toggle_points).pack(anchor="w")
        ttk.Checkbutton(self, text="Show time labels",
                        variable=self.var_show_time, command=self._toggle_time).pack(anchor="w")
        ttk.Checkbutton(self, text="Show grid",
                        variable=self.var_show_grid, command=self._toggle_grid).pack(anchor="w")

        # -------- Zoom / Axis ranges (manual) --------
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=8)
        ttk.Checkbutton(self, text="Manual axes (type to zoom)",
                        variable=self.var_use_manual, command=self._manual_toggle).pack(anchor="w")

        axes = ttk.Frame(self); axes.pack(fill="x", pady=(4,6))
        ttk.Label(axes, text="X min").grid(row=0, column=0, sticky="w")
        ttk.Label(axes, text="X max").grid(row=0, column=1, sticky="w")
        ttk.Label(axes, text="Y min").grid(row=2, column=0, sticky="w", pady=(4,0))
        ttk.Label(axes, text="Y max").grid(row=2, column=1, sticky="w", pady=(4,0))

        # entries for manual axes (we will prefill from CSV extents)
        self.ent_xmin = ttk.Entry(axes, width=12); self.ent_xmin.grid(row=1, column=0, padx=(0,6))
        self.ent_xmax = ttk.Entry(axes, width=12); self.ent_xmax.grid(row=1, column=1)
        self.ent_ymin = ttk.Entry(axes, width=12); self.ent_ymin.grid(row=3, column=0, padx=(0,6))
        self.ent_ymax = ttk.Entry(axes, width=12); self.ent_ymax.grid(row=3, column=1)

        btns_axes = ttk.Frame(self); btns_axes.pack(fill="x")
        ttk.Button(btns_axes, text="Apply Axes", command=self._apply_axes).pack(side="left")
        ttk.Button(btns_axes, text="Reset Axes", command=self._reset_axes).pack(side="left", padx=6)

        # -------- Boundary Line Values (separate) --------
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(self, text="Boundary Line Values", font=("Segoe UI", 10, "bold")).pack(anchor="w")

        lines = ttk.Frame(self); lines.pack(fill="x", pady=(6,0))
        # Temperature (X1)
        ttk.Label(lines, text="Temperature (X1)  min / max").grid(row=0, column=0, sticky="w")
        self.ent_temp_min = ttk.Entry(lines, width=10); self.ent_temp_min.grid(row=0, column=1, padx=(8,6))
        self.ent_temp_max = ttk.Entry(lines, width=10); self.ent_temp_max.grid(row=0, column=2)
        # Relative Humidity (X2)
        ttk.Label(lines, text="Relative Humidity (X2)  min / max").grid(row=1, column=0, sticky="w", pady=(4,0))
        self.ent_rh_min = ttk.Entry(lines, width=10); self.ent_rh_min.grid(row=1, column=1, padx=(8,6), pady=(4,0))
        self.ent_rh_max = ttk.Entry(lines, width=10); self.ent_rh_max.grid(row=1, column=2, pady=(4,0))
        # Wind Speed (Y1)
        ttk.Label(lines, text="Wind Speed (Y1)  min / max").grid(row=2, column=0, sticky="w", pady=(4,0))
        self.ent_wind_min = ttk.Entry(lines, width=10); self.ent_wind_min.grid(row=2, column=1, padx=(8,6), pady=(4,0))
        self.ent_wind_max = ttk.Entry(lines, width=10); self.ent_wind_max.grid(row=2, column=2, pady=(4,0))
        # Fuel Moisture (Y2)
        ttk.Label(lines, text="Fuel Moisture (Y2)  min / max").grid(row=3, column=0, sticky="w", pady=(4,0))
        self.ent_fuel_min = ttk.Entry(lines, width=10); self.ent_fuel_min.grid(row=3, column=1, padx=(8,6), pady=(4,0))
        self.ent_fuel_max = ttk.Entry(lines, width=10); self.ent_fuel_max.grid(row=3, column=2, pady=(4,0))

        btns_lines = ttk.Frame(self); btns_lines.pack(fill="x", pady=(6,2))
        ttk.Button(btns_lines, text="Apply Lines", command=self._apply_lines).pack(side="left")
        ttk.Button(btns_lines, text="Reset Lines to CSV", command=self._reset_lines_to_csv).pack(side="left", padx=6)

        # bottom buttons
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=8)
        btnrow = ttk.Frame(self); btnrow.pack(fill="x", pady=(8, 2))
        ttk.Button(btnrow, text="Redraw", command=self.on_redraw).pack(side="left")
        if self.reset_view_cb:
            ttk.Button(btnrow, text="Reset View", command=self.reset_view_cb).pack(side="left", padx=6)

        self.pack_propagate(False)
        self._prefill_from_state()
        self._sync_manual_entries()

    # ---------- helpers ----------
    def _prefill_from_state(self):
        """Fill manual axes & line boxes from current state (CSV extents by default)."""
        s = self.state
        # manual axes boxes default to CSV extents (so points are visible)
        def put(entry, val):
            entry.delete(0, "end")
            entry.insert(0, "" if val is None else f"{val:g}")
        # if manual axes already set, show those; else use data extents
        x_min = s.x_min_manual if s.use_manual_axes and s.x_min_manual is not None else s.axis_lo
        x_max = s.x_max_manual if s.use_manual_axes and s.x_max_manual is not None else s.axis_hi
        y_min = s.y_min_manual if s.use_manual_axes and s.y_min_manual is not None else s.axis_lo
        y_max = s.y_max_manual if s.use_manual_axes and s.y_max_manual is not None else s.axis_hi
        put(self.ent_xmin, x_min); put(self.ent_xmax, x_max)
        put(self.ent_ymin, y_min); put(self.ent_ymax, y_max)

        # boundary lines default to CSV min/max
        put(self.ent_temp_min, s.x1_min); put(self.ent_temp_max, s.x1_max)
        put(self.ent_rh_min,   s.x2_min); put(self.ent_rh_max,   s.x2_max)
        put(self.ent_wind_min, s.y1_min); put(self.ent_wind_max, s.y1_max)
        put(self.ent_fuel_min, s.y2_min); put(self.ent_fuel_max, s.y2_max)

    # ---------- event handlers ----------
    def choose_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not path: return
        try:
            df = load_csv_mapped(path)
        except Exception as e:
            messagebox.showerror("Load error", str(e)); return
        self.state.csv_path = path
        self.state.df = df
        compute_bounds(self.state)
        self.path_lbl.configure(text=path)
        # Reset view to data extents by default when a new file loads
        self.state.use_manual_axes = False
        self._prefill_from_state()
        self.on_redraw()

    def _toggle_points(self):
        self.state.show_x1y1 = self.var_show_x1y1.get()
        self.state.show_x2y2 = self.var_show_x2y2.get()
        self.on_redraw()

    def _toggle_time(self):
        self.state.show_time_labels = self.var_show_time.get()
        self.on_redraw()

    def _toggle_grid(self):
        self.state.show_grid = self.var_show_grid.get()
        self.on_redraw()

    # ---- manual axes
    def _manual_toggle(self):
        self.state.use_manual_axes = self.var_use_manual.get()
        self._sync_manual_entries()
        # when turning ON, ensure the boxes are filled (from CSV extents if blank)
        if self.state.use_manual_axes:
            self._prefill_from_state()
        self.on_redraw()

    def _apply_axes(self):
        # Only apply if manual is ON
        if not self.var_use_manual.get():
            messagebox.showinfo("Manual axes", "Turn on 'Manual axes' to apply typed limits.")
            return
        try:
            xmin = float(self.ent_xmin.get()); xmax = float(self.ent_xmax.get())
            ymin = float(self.ent_ymin.get()); ymax = float(self.ent_ymax.get())
            if xmin >= xmax: raise ValueError("X min must be < X max.")
            if ymin >= ymax: raise ValueError("Y min must be < Y max.")
        except ValueError as e:
            messagebox.showwarning("Invalid axes", str(e)); return
        self.state.x_min_manual, self.state.x_max_manual = xmin, xmax
        self.state.y_min_manual, self.state.y_max_manual = ymin, ymax
        self.state.use_manual_axes = True
        self.var_use_manual.set(True)
        self.on_redraw()

    def _reset_axes(self):
        self.state.use_manual_axes = False
        self.var_use_manual.set(False)
        self.state.x_min_manual = self.state.x_max_manual = None
        self.state.y_min_manual = self.state.y_max_manual = None
        self._prefill_from_state()
        self.on_redraw()

    def _sync_manual_entries(self):
        state = "normal" if self.var_use_manual.get() else "disabled"
        for w in (self.ent_xmin, self.ent_xmax, self.ent_ymin, self.ent_ymax):
            w.config(state=state)

    # ---- boundary lines
    def _apply_lines(self):
        def parse(entry):
            txt = entry.get().strip()
            return None if txt == "" else float(txt)
        try:
            self.state.x1_min = parse(self.ent_temp_min)
            self.state.x1_max = parse(self.ent_temp_max)
            self.state.x2_min = parse(self.ent_rh_min)
            self.state.x2_max = parse(self.ent_rh_max)
            self.state.y1_min = parse(self.ent_wind_min)
            self.state.y1_max = parse(self.ent_wind_max)
            self.state.y2_min = parse(self.ent_fuel_min)
            self.state.y2_max = parse(self.ent_fuel_max)
        except ValueError as e:
            messagebox.showwarning("Invalid line values", str(e)); return
        self.on_redraw()

    def _reset_lines_to_csv(self):
        # Restore line values to CSV-derived min/max
        compute_bounds(self.state)
        self._prefill_from_state()
        self.on_redraw()
