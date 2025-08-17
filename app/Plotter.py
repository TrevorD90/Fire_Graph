# app/Plotter.py
import numpy as np
from matplotlib.axes import Axes
from .State import AppState

def compute_bounds(state: AppState) -> None:
    """Compute data-driven mins/maxes and a padded world range from the current df."""
    df = state.df
    if df is None or len(df) == 0:
        # Clear ranges
        state.x1_min = state.x1_max = None
        state.x2_min = state.x2_max = None
        state.y1_min = state.y1_max = None
        state.y2_min = state.y2_max = None
        state.axis_lo = state.axis_hi = None
        return

    x1_min, x1_max = df["x1"].min(), df["x1"].max()   # Temperature
    x2_min, x2_max = df["x2"].min(), df["x2"].max()   # RH
    y1_min, y1_max = df["y1"].min(), df["y1"].max()   # Wind
    y2_min, y2_max = df["y2"].min(), df["y2"].max()   # Fuel

    state.x1_min, state.x1_max = float(x1_min), float(x1_max)
    state.x2_min, state.x2_max = float(x2_min), float(x2_max)
    state.y1_min, state.y1_max = float(y1_min), float(y1_max)
    state.y2_min, state.y2_max = float(y2_min), float(y2_max)

    all_vals = [x1_min, x1_max, x2_min, x2_max, y1_min, y1_max, y2_min, y2_max]
    lo, hi = float(np.min(all_vals)), float(np.max(all_vals))
    span = max(hi - lo, 1.0)
    pad = 0.06 * span
    state.axis_lo, state.axis_hi = lo - pad, hi + pad


def draw(ax: Axes, state: AppState) -> None:
    """
    Draw the figure. Boundary lines are anchored in *world/data* coordinates,
    so zoom/pan only changes the view (Matplotlib clips the lines).
    """
    ax.clear()
    ax.set_facecolor('#4a4a4a')
    df = state.df
    if df is None or len(df) == 0:
        ax.set_title("No data loaded")
        ax.figure.canvas.draw_idle()
        return

    # --- 1) Choose VIEW limits (manual or data-driven) ---
    if state.use_manual_axes and None not in (state.x_min_manual, state.x_max_manual,
                                              state.y_min_manual, state.y_max_manual):
        ax.set_xlim(state.x_min_manual, state.x_max_manual)
        ax.set_ylim(state.y_min_manual, state.y_max_manual)
    else:
        ax.set_xlim(state.axis_lo, state.axis_hi)
        ax.set_ylim(state.axis_lo, state.axis_hi)

    ax.set_aspect("equal", adjustable="box")
    ax.set_axisbelow(True)

    # --- 2) WORLD edges for lines (fixed; DO NOT use current view limits) ---
    XW0, XW1 = state.axis_lo, state.axis_hi
    YW0, YW1 = state.axis_lo, state.axis_hi

    # --- 3) Grid (toggle) ---
    if state.show_grid:
        ax.grid(True, which="both", linestyle=":", alpha=0.35)
    else:
        ax.grid(False)

    # --- 4) Boundary lines (fixed data coords) ---
    # Temperature (X1) min/max → RH (X2) min/max, spanning full world vertical range
    ax.plot([state.x1_min, state.x2_min], [YW0, YW1],color='red', linewidth=2)                     # MIN X line
    ax.plot([state.x1_max, state.x2_max], [YW0, YW1],color='red', linewidth=2, linestyle="--")     # MAX X line

    # Wind (Y1) min/max → Fuel (Y2) min/max, spanning full world horizontal range
    ax.plot([XW0, XW1], [state.y1_min, state.y2_min],color='red', linewidth=2)                     # MIN Y line
    ax.plot([XW0, XW1], [state.y1_max, state.y2_max],color='red', linewidth=2, linestyle="--")     # MAX Y line

    # --- 5) Points (no connectors) ---
    if state.show_x1y1:
        ax.scatter(df["x1"], df["y1"], s=30, label="Temp/Wind")
    if state.show_x2y2:
        ax.scatter(df["x2"], df["y2"], s=30, label="RH/Fuel")

    # --- 6) Optional time labels (every Nth) ---
    if state.show_time_labels and state.time_label_step >= 1:
        step = int(state.time_label_step)
        # slight offset cycle to reduce overlap
        offsets = [(6, 6), (6, -6), (-6, 6), (-6, -6)]
        times = df["time"].astype(str).to_numpy()

        if state.show_x1y1:
            xs, ys = df["x1"].to_numpy(), df["y1"].to_numpy()
            for i in range(0, len(df), step):
                dx, dy = offsets[(i // step) % len(offsets)]
                ax.annotate(times[i], (xs[i], ys[i]), xytext=(dx, dy),
                            textcoords="offset points", fontsize=8,
                            bbox=dict(facecolor="white", alpha=0.6, pad=0.2))

        if state.show_x2y2:
            xs, ys = df["x2"].to_numpy(), df["y2"].to_numpy()
            for i in range(0, len(df), step):
                dx, dy = offsets[(i // step + 1) % len(offsets)]
                ax.annotate(times[i], (xs[i], ys[i]), xytext=(dx, dy),
                            textcoords="offset points", fontsize=8,
                            bbox=dict(facecolor="white", alpha=0.6, pad=0.2))

    # --- 7) Axis labels + mirrored ticks ---
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Wind Speed")

    top = ax.secondary_xaxis('top')
    top.set_xlabel("Relative Humidity")
    top.set_xticks(ax.get_xticks())
    top.set_xticklabels([f"{t:g}" for t in ax.get_xticks()])

    right = ax.secondary_yaxis('right')
    right.set_ylabel("Fuel Moisture")
    right.set_yticks(ax.get_yticks())
    right.set_yticklabels([f"{t:g}" for t in ax.get_yticks()])

    # --- 8) Legend / title ---
    ax.set_title("Inverse Min/Max — Zoom/Pan Safe — Nth Time Labels")
    from matplotlib.lines import Line2D
    legend_items = [
        Line2D([0], [0], linewidth=2, linestyle="-", label="Min boundaries"),
        Line2D([0], [0], linewidth=2, linestyle="--", label="Max boundaries"),
    ]
    ax.legend(handles=legend_items, loc="upper left")
