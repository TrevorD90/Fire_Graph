import tkinter as tk

def build_rx_tab(frame, state):
    units = ["Temp", "RH", "Wind", "Fuel"]

    for unit in units:
        min_var = tk.StringVar()
        max_var = tk.StringVar()

        # Trigger replot on value change
        min_var.trace_add("write", lambda *_, u=unit: on_update(state))
        max_var.trace_add("write", lambda *_, u=unit: on_update(state))

        state.rx_vars[unit] = (min_var, max_var)

        row = tk.Frame(frame)
        row.pack(pady=5, padx=10, anchor='w')

        tk.Label(row, text=f"{unit} Min:").pack(side=tk.LEFT)
        tk.Entry(row, width=5, textvariable=min_var).pack(side=tk.LEFT)

        tk.Label(row, text=f"{unit} Max:").pack(side=tk.LEFT)
        tk.Entry(row, width=5, textvariable=max_var).pack(side=tk.LEFT)

def on_update(state):
    if state.graph:
        state.graph.plot_data()
