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
    pad = 0.06 * span
    state.axis_lo, state.axis_hi = lo - pad, hi + pad

def _line_ends_for_xlines(state: AppState, y_lo: float, y_hi: float):
    """Return (y0_min, y1_min, y0_max, y1_max) for X-lines."""
    if state.use_custom_line_ends:
        y0min = state.xline_min_y0 if state.xline_min_y0 is not None else y_lo
        y1min = state.xline_min_y1 if state.xline_min_y1 is not None else y_hi
        y0max = state.xline_max_y0 if state.xline_max_y0 is not None else y_lo
        y1max = state.xline_max_y1 if state.xline_max_y1 is not None else y_hi
        return y0min, y1min, y0max, y1max
    return y_lo, y_hi, y_lo, y_hi

def _line_ends_for_ylines(state: AppState, x_lo: float, x_hi: float):
    """Return (x0_min, x1_min, x0_max, x1_max) for Y-lines."""
    if state.use_custom_line_ends:
        x0min = state.yline_min_x0 if state.yline_min_x0 is not None else x_lo
        x1min = state.yline_min_x1 if state.yline_min_x1 is not None else x_hi
        x0max = state.yline_max_x0 if state.yline_max_x0 is not None else x_lo
        x1max = state.yline_max_x1 if state.yline_max_x1 is not None else x_hi
        return x0min, x1min, x0max, x1max
    return x_lo, x_hi, x_lo, x_hi

def draw(ax: Axes, state: AppState) -> None:
    """
    Draws the plot with boundary lines that are defined in *world/data* coordinates.
    Zooming changes only the view window; lines are clipped, not recomputed.
    """
    ax.clear()
    df = state.df

    # --- 1) Set the current VIEW limits (manual or data-driven) ---
    if state.use_manual_axes and None not in (state.x_min_manual, state.x_max_manual,
                                              state.y_min_manual, state.y_max_manual):
        ax.set_xlim(state.x_min_manual, state.x_max_manual)
        ax.set_ylim(state.y_min_manual, state.y_max_manual)
    else:
        ax.set_xlim(state.axis_lo, state.axis_hi)
        ax.set_ylim(state.axis_lo, state.axis_hi)

    ax.set_aspect("equal", adjustable="box")
    ax.set_axisbelow(True)

    # --- 2) WORLD (fixed) edges for lines (do NOT use current view limits) ---
    XW0, XW1 = state.axis_lo, state.axis_hi
    YW0, YW1 = state.axis_lo, state.axis_hi

    # Optional grid
    if state.show_grid:
        ax.grid(True, which="both", linestyle=":", alpha=0.35)
    else:
        ax.grid(False)

    # --- 3) Boundary lines in world coordinates ---
    # Custom endpoints (if enabled) are treated as absolute world coords.
    # For X-lines (Temp→RH): use y0/y1; default to world vertical span
    if getattr(state, "use_custom_line_ends", False):
        y_min_y0 = state.xline_min_y0 if state.xline_min_y0 is not None else YW0
        y_min_y1 = state.xline_min_y1 if state.xline_min_y1 is not None else YW1
        y_max_y0 = state.xline_max_y0 if state.xline_max_y0 is not None else YW0
        y_max_y1 = state.xline_max_y1 if state.xline_max_y1 is not None else YW1
        x_min_x0, x_min_x1 = state.x1_min, state.x2_min
        x_max_x0, x_max_x1 = state.x1_max, state.x2_max
    else:
        # default: spans the full world vertical extent
        y_min_y0, y_min_y1 = YW0, YW1
        y_max_y0, y_max_y1 = YW0, YW1
        x_min_x0, x_min_x1 = state.x1_min, state.x2_min
        x_max_x0, x_max_x1 = state.x1_max, state.x2_max

    # For Y-lines (Wind→Fuel): use x0/x1; default to world horizontal span
    if getattr(state, "use_custom_line_ends", False):
        x_min_x0_y, x_min_x1_y = state.yline_min_x0 if state.yline_min_x0 is not None else XW0, \
                                 state.yline_min_x1 if state.yline_min_x1 is not None else XW1
        x_max_x0_y, x_max_x1_y = state.yline_max_x0 if state.yline_max_x0 is not None else XW0, \
                                 state.yline_max_x1 if state.yline_max_x1 is not None else XW1
        y_min_y, y_max_y = state.y1_min, state.y2_min
        y_min_y2, y_max_y2 = state.y1_max, state.y2_max
    else:
        x_min_x0_y, x_min_x1_y = XW0, XW1
        x_max_x0_y, x_max_x1_y = XW0, XW1
        y_min_y, y_max_y = state.y1_min, state.y2_min
        y_min_y2, y_max_y2 = state.y1_max, state.y2_max

    # Draw lines (Matplotlib will clip them to current view)
    # X-lines (Temp→RH)
    ax.plot([x_min_x0, x_min_x1], [y_min_y0, y_min_y1], linewidth=2)
    ax.plot([x_max_x0, x_max_x1], [y_max_y0, y_max_y1], linewidth=2, linestyle="--")
    # Y-lines (Wind→Fuel)
    ax.plot([x_min_x0_y, x_min_x1_y], [y_min_y, y_max_y], linewidth=2)
    ax.plot([x_max_x0_y, x_max_x1_y], [y_min_y2, y_max_y2], linewidth=2, linestyle="--")

    # --- 4) Points (no connectors) ---
    if state.show_x1y1:
        ax.scatter(df["x1"], df["y1"], s=30)
    if state.show_x2y2:
        ax.scatter(df["x2"], df["y2"], s=30)

    # --- 5) Optional time labels (still in data coords) ---
    if state.show_time_labels:
        offsets = [(6, 6), (6, -6), (-6, 6), (-6, -6)]
        step = max(1, int(state.label_every))
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

    # --- 6) Labels & mirrored ticks ---
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

    # Legend
    ax.set_title("Inverse Min/Max — Lines anchored in data coordinates (zoom-safe)")
    from matplotlib.lines import Line2D
    legend_items = [
        Line2D([0], [0], linewidth=2, linestyle="-", label="Min boundaries"),
        Line2D([0], [0], linewidth=2, linestyle="--", label="Max boundaries"),
    ]
    ax.legend(handles=legend_items, loc="upper left")
