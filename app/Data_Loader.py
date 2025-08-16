import re
import pandas as pd

def _norm(s: str) -> str:
    """Normalize header: lower, strip, remove non-alnum except %."""
    return re.sub(r"[^a-z0-9%]+", "", str(s).lower().strip())

def _find_col(df: pd.DataFrame, candidates) -> str | None:
    """Find a column by normalized name or prefix match."""
    canon = {_norm(c): c for c in df.columns}
    for wanted in candidates:
        w = _norm(wanted)
        if w in canon:
            return canon[w]
    for k, orig in canon.items():
        if any(k.startswith(_norm(w)) for w in candidates):
            return orig
    return None

def load_csv_mapped(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Map your headers → canonical names
    col_time = _find_col(df, ["time", "timestamp", "date/time"])
    col_temp = _find_col(df, ["temperature", "temp", "temperaturef", "temperature°f"])
    col_wind = _find_col(df, ["windspeed", "wind speed", "wind(mph)", "wind"])
    col_rh   = _find_col(df, ["relativehumidity", "relative humidity", "rh", "relativehumidity%"])
    col_fm   = _find_col(df, ["fuelmoisture", "fuel moisture", "fm"])

    missing = []
    if not col_time: missing.append("Time")
    if not col_temp: missing.append("Temperature")
    if not col_wind: missing.append("Wind Speed")
    if not col_rh:   missing.append("Relative Humidity")
    if not col_fm:   missing.append("Fuel Moisture")
    if missing:
        raise ValueError(
            "Missing required columns (case-insensitive): " + ", ".join(missing) +
            f"\nFound: {list(df.columns)}"
        )

    df = df.rename(columns={
        col_time: "time",
        col_temp: "x1",   # Temperature → X1
        col_wind: "y1",   # Wind Speed → Y1
        col_rh:   "x2",   # Relative Humidity → X2
        col_fm:   "y2",   # Fuel Moisture → Y2
    })
    for c in ["x1", "y1", "x2", "y2"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["x1", "y1", "x2", "y2"])
    return df[["time", "x1", "y1", "x2", "y2"]]
