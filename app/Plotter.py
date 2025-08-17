from __future__ import annotations
import numpy as np
from matplotlib.axes import Axes
from .State import AppState

def compute_bounds(state: AppState) -> None:
    df = state.df
    x1_min, x1_max = df["x1"].min(), df["x1"].max()
    x2_min, x2_max = df["x2"].min(), df["x2"].max()
    y1_min, y1_max = df["y1"].min(), df["y1"].max()
    y2_min, y2_max = df["y2"].min(), df["y2"].max()

    state.x1_min, state.x1_max = float(x1_min), float(x1_max)
    state.x2_min, state.x2_max = float(x2_min), float(x2_max)
    state.y1_min, state.y1_max = float(y1_min), float(y1_max)
    state.y2_min, state.y2_max = float(y2_min), float(y2_max)

    all_vals = [x1_min, x1_max, x2_min, x2_max, y1_min, y1_max, y2_min, y2_max]
    lo, hi = float(np.min(all_vals)), float(np.max(all_vals))
    span = max(hi - lo, 1.0)
    pad = max(1e-6, 0.06 * span)
    state.axis_lo, state.axis_hi = lo - pad, hi + pad

def draw(ax: Axes, state: AppState) -> None:
    """Draw figure; top/right show full tick scale mirrored from bottom/left.
       Uses manual axis ranges if enabled."""
    ax.clear()
    df = state.df

    # ---- choose axis limits ----
    if state.use_manual_axes and None not in (state.x_min_manual, state.x_max_manual,
                                              state.y_min_manual, state.y_max_manual):
        x_lo, x_hi = float(state.x_min_manual), float(state.x_max_manual)
        y_lo, y_hi = float(state.y_min_manual), float(state.y_max_manual)
    else:
        x_lo = y_lo = state.axis_lo
        x_hi = y_hi = state.axis_hi

    # Limits & aspect
    ax.set_xlim(x_lo, x_hi)
    ax.set_ylim(y_lo, y_hi)
    ax.set_aspect("equal", adjustable="box")

    # ---- Boundary lines (axis connectors only) ----
    # X1 (Temp) → X2 (RH)
    ax.plot([state.x1_min, state.x2_min], [y_lo, y_hi], linewidth=2)
    ax.plot([state.x1_max, state.x2_max], [y_lo, y_hi], linewidth=2, linestyle="--")
    # Y1 (Wind) → Y2 (Fuel)
    ax.plot([x_lo, x_hi], [state.y1_min, state.y2_min], linewidth=2)
    ax.plot([x_lo, x_hi], [state.y1_max, state.y2_max], linewidth=2, linestyle="--")

    # ---- Points (no connectors) ----
    if state.show_x1y1:
        ax.scatter(df["x1"], df["y1"], s=30)
    if state.show_x2y2:
        ax.scatter(df["x2"], df["y2"], s=30)

    # ---- Axis labels ----
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Wind Speed")

    # Bottom/left ticks: let Matplotlib decide for current limits
    # Then mirror to top/right so they show a full grid as well.
    top = ax.secondary_xaxis('top')
    top.set_xlabel("Relative Humidity")
    top.set_xticks(ax.get_xticks())
    top.set_xticklabels([f"{t:g}" for t in ax.get_xticks()])

    right = ax.secondary_yaxis('right')
    right.set_ylabel("Fuel Moisture")
    right.set_yticks(ax.get_yticks())
    right.set_yticklabels([f"{t:g}" for t in ax.get_yticks()])

    # Title & legend
    ax.set_title("Inverse Min/Max Connections — Full Ticks on X2/Y2 (Zoomable)")
    from matplotlib.lines import Line2D
    legend_items = [
        Line2D([0], [0], linewidth=2, linestyle="-", label="Min boundaries"),
        Line2D([0], [0], linewidth=2, linestyle="--", label="Max boundaries"),
    ]
    ax.legend(handles=legend_items, loc="upper left")
