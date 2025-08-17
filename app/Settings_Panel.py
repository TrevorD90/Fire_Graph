import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .State import AppState
from .Data_Loader import load_csv_mapped
from .Plotter import compute_bounds

class SettingsPanel(tk.Frame):
    def __init__(self, parent, state: AppState, on_redraw):
        super().__init__(parent, bg="#f6f6f6", padx=10, pady=10, width=260)
        self.state = state
        self.on_redraw = on_redraw

        self.var_show_x1y1 = tk.BooleanVar(value=state.show_x1y1)
        self.var_show_x2y2 = tk.BooleanVar(value=state.show_x2y2)
        self.var_use_manual = tk.BooleanVar(value=state.use_manual_axes)

        ttk.Label(self, text="Settings", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))

        # CSV picker
        ttk.Button(self, text="Choose CSV…", command=self.choose_csv).pack(anchor="w", pady=4)
        self.path_lbl = ttk.Label(self, text="(no file)")
        self.path_lbl.pack(anchor="w")

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=8)

        # Toggles
        ttk.Checkbutton(self, text="Show Temp/Wind (X1–Y1)",
                        variable=self.var_show_x1y1, command=self._toggle_changed).pack(anchor="w", pady=2)
        ttk.Checkbutton(self, text="Show RH/Fuel (X2–Y2)",
                        variable=self.var_show_x2y2, command=self._toggle_changed).pack(anchor="w", pady=2)

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=8)

        # Axis & Line Values (read-only labels)
        ttk.Label(self, text="Axis & Line Values", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.labels = {
            "tmin": ttk.Label(self, text="Temp min: -"),
            "tmax": ttk.Label(self, text="Temp max: -"),
            "rhmin": ttk.Label(self, text="RH min: -"),
            "rhmax": ttk.Label(self, text="RH max: -"),
            "wmin": ttk.Label(self, text="Wind min: -"),
            "wmax": ttk.Label(self, text="Wind max: -"),
            "fmin": ttk.Label(self, text="Fuel min: -"),
            "fmax": ttk.Label(self, text="Fuel max: -"),
            "alo": ttk.Label(self, text="Axis LO: -"),
            "ahi": ttk.Label(self, text="Axis HI: -"),
        }
        for k in ["tmin","tmax","rhmin","rhmax","wmin","wmax","fmin","fmax","alo","ahi"]:
            self.labels[k].pack(anchor="w")

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=8)

        # ---- Manual axis controls ----
        ttk.Checkbutton(self, text="Manual axes (zoom/pan)",
                        variable=self.var_use_manual, command=self._manual_toggle)\
            .pack(anchor="w", pady=(0,4))

        grid = ttk.Frame(self)
        grid.pack(fill="x", pady=(0,6))
        ttk.Label(grid, text="X min").grid(row=0, column=0, sticky="w")
        ttk.Label(grid, text="X max").grid(row=0, column=1, sticky="w")
        ttk.Label(grid, text="Y min").grid(row=2, column=0, sticky="w", pady=(4,0))
        ttk.Label(grid, text="Y max").grid(row=2, column=1, sticky="w", pady=(4,0))

        self.ent_xmin = ttk.Entry(grid, width=10)
        self.ent_xmax = ttk.Entry(grid, width=10)
        self.ent_ymin = ttk.Entry(grid, width=10)
        self.ent_ymax = ttk.Entry(grid, width=10)

        self.ent_xmin.grid(row=1, column=0, padx=(0,6))
        self.ent_xmax.grid(row=1, column=1)
        self.ent_ymin.grid(row=3, column=0, padx=(0,6))
        self.ent_ymax.grid(row=3, column=1)

        btns = ttk.Frame(self)
        btns.pack(fill="x", pady=(6,2))
        ttk.Button(btns, text="Apply Axes", command=self._apply_axes).pack(side="left")
        ttk.Button(btns, text="Reset to Data", command=self._reset_axes).pack(side="left", padx=6)

        ttk.Button(self, text="Redraw", command=self._do_redraw).pack(anchor="w", pady=8)
        self.pack_propagate(False)

        # Initialize entries disabled until user toggles manual
        self._sync_manual_entries()

    def _toggle_changed(self):
        self.state.show_x1y1 = self.var_show_x1y1.get()
        self.state.show_x2y2 = self.var_show_x2y2.get()
        self._do_redraw()

    def choose_csv(self):
        p = filedialog.askopenfilename(
            title="Choose CSV",
            filetypes=[("CSV files","*.csv"), ("All files","*.*")]
        )
        if not p:
            return
        try:
            self.state.csv_path = p
            self.state.df = load_csv_mapped(p)
            compute_bounds(self.state)
            self._update_numbers()
            self.path_lbl.config(text=p)
            # When new data loads, if manual axes are ON but entries are empty,
            # prefill with computed bounds so user can tweak easily.
            if self.state.use_manual_axes:
                self._prefill_from_computed()
            self.on_redraw()
        except Exception as e:
            messagebox.showerror("Load error", str(e))

    def _manual_toggle(self):
        self.state.use_manual_axes = self.var_use_manual.get()
        if self.state.use_manual_axes and self.state.df is not None:
            self._prefill_from_computed()
        self._sync_manual_entries()
        self._do_redraw()

    def _prefill_from_computed(self):
        # Prefill entries from current computed bounds if blank
        def set_if_empty(entry, val):
            if not entry.get().strip():
                entry.delete(0, "end"); entry.insert(0, f"{val:g}")
        set_if_empty(self.ent_xmin, self.state.axis_lo)
        set_if_empty(self.ent_xmax, self.state.axis_hi)
        set_if_empty(self.ent_ymin, self.state.axis_lo)
        set_if_empty(self.ent_ymax, self.state.axis_hi)

    def _sync_manual_entries(self):
        state = "normal" if self.var_use_manual.get() else "disabled"
        for w in (self.ent_xmin, self.ent_xmax, self.ent_ymin, self.ent_ymax):
            w.config(state=state)

    def _apply_axes(self):
        if not self.state.df is not None:
            messagebox.showinfo("No data", "Choose a CSV first.")
            return
        try:
            self.state.x_min_manual = float(self.ent_xmin.get())
            self.state.x_max_manual = float(self.ent_xmax.get())
            self.state.y_min_manual = float(self.ent_ymin.get())
            self.state.y_max_manual = float(self.ent_ymax.get())
            if self.state.x_min_manual >= self.state.x_max_manual:
                raise ValueError("X min must be < X max.")
            if self.state.y_min_manual >= self.state.y_max_manual:
                raise ValueError("Y min must be < Y max.")
            self.state.use_manual_axes = True
            self.var_use_manual.set(True)
            self._do_redraw()
        except ValueError as e:
            messagebox.showwarning("Invalid axis values", str(e))

    def _reset_axes(self):
        # Back to data-driven bounds
        self.state.use_manual_axes = False
        self.var_use_manual.set(False)
        self.state.x_min_manual = self.state.x_max_manual = None
        self.state.y_min_manual = self.state.y_max_manual = None
        for w in (self.ent_xmin, self.ent_xmax, self.ent_ymin, self.ent_ymax):
            w.delete(0, "end")
        self._sync_manual_entries()
        compute_bounds(self.state)
        self._update_numbers()
        self.on_redraw()

    def _do_redraw(self):
        if self.state.df is None:
            return
        # Recompute data bounds (so Redraw reacts to new CSVs/edits),
        # but keep manual overrides if they're enabled.
        compute_bounds(self.state)
        self._update_numbers()
        self.on_redraw()

    def _update_numbers(self):
        s = self.state
        def fmt(x): return "-" if x is None else f"{x:g}"
        self.labels["tmin"].config(text=f"Temp min: {fmt(s.x1_min)}")
        self.labels["tmax"].config(text=f"Temp max: {fmt(s.x1_max)}")
        self.labels["rhmin"].config(text=f"RH min: {fmt(s.x2_min)}")
        self.labels["rhmax"].config(text=f"RH max: {fmt(s.x2_max)}")
        self.labels["wmin"].config(text=f"Wind min: {fmt(s.y1_min)}")
        self.labels["wmax"].config(text=f"Wind max: {fmt(s.y1_max)}")
        self.labels["fmin"].config(text=f"Fuel min: {fmt(s.y2_min)}")
        self.labels["fmax"].config(text=f"Fuel max: {fmt(s.y2_max)}")
        self.labels["alo"].config(text=f"Axis LO: {fmt(s.axis_lo)}")
        self.labels["ahi"].config(text=f"Axis HI: {fmt(s.axis_hi)}")
