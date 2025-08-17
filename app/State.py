from dataclasses import dataclass
import pandas as pd

@dataclass
class AppState:
    csv_path: str | None = None
    df: pd.DataFrame | None = None

    # Point visibility
    show_x1y1: bool = True
    show_x2y2: bool = True

    # Labels & grid
    show_time_labels: bool = False
    label_every: int = 2
    show_grid: bool = False

    # Data-driven bounds
    x1_min: float | None = None
    x1_max: float | None = None
    x2_min: float | None = None
    x2_max: float | None = None
    y1_min: float | None = None
    y1_max: float | None = None
    y2_min: float | None = None
    y2_max: float | None = None
    axis_lo: float | None = None
    axis_hi: float | None = None

    # Manual axes (zoom window)
    use_manual_axes: bool = False
    x_min_manual: float | None = None
    x_max_manual: float | None = None
    y_min_manual: float | None = None
    y_max_manual: float | None = None

    # ---- Custom boundary line endpoints (optional) ----
    # If disabled, X-lines span full current Y edges; Y-lines span full X edges.
    use_custom_line_ends: bool = False
    # X-lines (Temperature/RH): y-start/y-end for min and max lines
    xline_min_y0: float | None = None
    xline_min_y1: float | None = None
    xline_max_y0: float | None = None
    xline_max_y1: float | None = None
    # Y-lines (Wind/Fuel): x-start/x-end for min and max lines
    yline_min_x0: float | None = None
    yline_min_x1: float | None = None
    yline_max_x0: float | None = None
    yline_max_x1: float | None = None
