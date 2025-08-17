from dataclasses import dataclass
import pandas as pd

@dataclass
class AppState:
    # current CSV & data
    csv_path: str | None = None
    df: pd.DataFrame | None = None

    # which point sets to show
    show_x1y1: bool = True   # Temperature vs Wind Speed
    show_x2y2: bool = True   # Relative Humidity vs Fuel Moisture

    # computed bounds (from data)
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

    # ---- manual axis overrides (for zoom/pan) ----
    use_manual_axes: bool = False
    x_min_manual: float | None = None
    x_max_manual: float | None = None
    y_min_manual: float | None = None
    y_max_manual: float | None = None
