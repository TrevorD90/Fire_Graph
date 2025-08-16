import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .state import AppState
from .data_loader import load_csv_mapped
from .plotter import compute_bounds

class SettingsPanel(tk.Frame):
    def __init__(self, parent, state: AppState, on_redraw):
        super().__init__(parent, bg="#f6f6f6", padx=10, pady=10, width=260)
        self.state = state
        self.on_redraw = on_redraw

        self.var_show_x1y1 = tk.BooleanVar(value=state.show_x1y1)
        self.var_show_x2y2 = tk.BooleanVar(value=state.show_x2y2)

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

        # Numbers section
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

        ttk.Button(self, text="Redraw", command=self._do_redraw).pack(anchor="w", pady=4)
        self.pack_propagate(False)

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
            self.on_redraw()
        except Exception as e:
            messagebox.showerror("Load error", str(e))

    def _do_redraw(self):
        if self.state.df is None:
            return
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
