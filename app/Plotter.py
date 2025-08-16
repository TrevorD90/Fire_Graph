from __future__ import annotations
import numpy as np
from matplotlib.axes import Axes
from .state import AppState

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
    ax.clear()
    df = state.df

    ax.set_xlim(state.axis_lo, state.axis_hi)
    ax.set_ylim(state.axis_lo, state.axis_hi)
    ax.set_aspect("equal", adjustable="box")

    # ---- 8 boundary lines (only axis connectors) ----
    # X1 (Temp) → X2 (RH)
    ax.plot([state.x1_min, state.x2_min], [state.axis_lo, state.axis_hi], linewidth=2)
    ax.plot([state.x1_max, state.x2_max], [state.axis_lo, state.axis_hi], linewidth=2, linestyle="--")
    # Y1 (Wind) → Y2 (Fuel)
    ax.plot([state.axis_lo, state.axis_hi], [state.y1_min, state.y2_min], linewidth=2)
    ax.plot([state.axis_lo, state.axis_hi], [state.y1_max, state.y2_max], linewidth=2, linestyle="--")

    # ---- Annotate min/max values at edges ----
    box = dict(facecolor="white", alpha=0.7, pad=0.2)
    ax.annotate(f"Temp min = {state.x1_min:g}", (state.x1_min, state.axis_lo), xytext=(0, -12),
                textcoords="offset points", ha="center", va="top", fontsize=9, bbox=box)
    ax.annotate(f"Temp max = {state.x1_max:g}", (state.x1_max, state.axis_lo), xytext=(0, -12),
                textcoords="offset points", ha="center", va="top", fontsize=9, bbox=box)
    ax.annotate(f"RH min = {state.x2_min:g}", (state.x2_min, state.axis_hi), xytext=(0, 12),
                textcoords="offset points", ha="center", va="bottom", fontsize=9, bbox=box)
    ax.annotate(f"RH max = {state.x2_max:g}", (state.x2_max, state.axis_hi), xytext=(0, 12),
                textcoords="offset points", ha="center", va="bottom", fontsize=9, bbox=box)

    ax.annotate(f"Wind min = {state.y1_min:g}", (state.axis_lo, state.y1_min), xytext=(-12, 0),
                textcoords="offset points", ha="right", va="center", fontsize=9, bbox=box)
    ax.annotate(f"Wind max = {state.y1_max:g}", (state.axis_lo, state.y1_max), xytext=(-12, 0),
                textcoords="offset points", ha="right", va="center", fontsize=9, bbox=box)
    ax.annotate(f"Fuel min = {state.y2_min:g}", (state.axis_hi, state.y2_min), xytext=(12, 0),
                textcoords="offset points", ha="left", va="center", fontsize=9, bbox=box)
    ax.annotate(f"Fuel max = {state.y2_max:g}", (state.axis_hi, state.y2_max), xytext=(12, 0),
                textcoords="offset points", ha="left", va="center", fontsize=9, bbox=box)

    # ---- Points (no connectors) ----
    if state.show_x1y1:
        ax.scatter(df["x1"], df["y1"], s=30)  # Temp vs Wind
    if state.show_x2y2:
        ax.scatter(df["x2"], df["y2"], s=30)  # RH vs Fuel

    # ---- Labels / title ----
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Wind Speed")
    ax.annotate("Relative Humidity", xy=(0.5, 1.02), xycoords="axes fraction",
                ha="center", va="bottom")
    ax.annotate("Fuel Moisture", xy=(1.02, 0.5), xycoords="axes fraction",
                ha="left", va="center", rotation=-90)
    ax.set_title("Inverse Min/Max Connections — Toggle Points, Redraw to Update")

    # boundary legend
    from matplotlib.lines import Line2D
    legend_items = [
        Line2D([0], [0], linewidth=2, linestyle="-", label="Min boundaries"),
        Line2D([0], [0], linewidth=2, linestyle="--", label="Max boundaries"),
    ]
    ax.legend(handles=legend_items, loc="upper left")
