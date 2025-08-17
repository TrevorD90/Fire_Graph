# app/State.py
from dataclasses import dataclass
import pandas as pd

@dataclass
class AppState:
    # Data
    csv_path: str | None = None
    df: pd.DataFrame | None = None

    # Point visibility
    show_x1y1: bool = True   # Temperature vs Wind Speed
    show_x2y2: bool = True   # Relative Humidity vs Fuel Moisture

    # Grid & time labels
    show_grid: bool = False
    show_time_labels: bool = False
    time_label_step: int = 1  # show every Nth time label (1 = every point)

    # Data-driven bounds (computed from CSV; also used as "world" coords)
    x1_min: float | None = None   # Temperature min
    x1_max: float | None = None   # Temperature max
    x2_min: float | None = None   # RH min
    x2_max: float | None = None   # RH max
    y1_min: float | None = None   # Wind min
    y1_max: float | None = None   # Wind max
    y2_min: float | None = None   # Fuel min
    y2_max: float | None = None   # Fuel max
    axis_lo: float | None = None  # world min (padding included)
    axis_hi: float | None = None  # world max (padding included)

    # Manual axes (typed zoom box)
    use_manual_axes: bool = False
    x_min_manual: float | None = None
    x_max_manual: float | None = None
    y_min_manual: float | None = None
    y_max_manual: float | None = None
