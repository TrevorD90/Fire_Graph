# app/Data_Loader.py
import os
import pandas as pd

def load_csv_mapped(path: str) -> pd.DataFrame:
    """
    Load a CSV and normalize column names to match the expected schema:
      - Temperature   -> x1
      - Wind Speed    -> y1
      - Relative Humidity -> x2
      - Fuel Moisture -> y2
      - Time          -> time
    Case- and space-insensitive.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found at: {path}")

    df = pd.read_csv(path)

    # Normalize headers
    lower_cols = {c.lower().strip(): c for c in df.columns}

    # Define required logical names and their canonical mappings
    mapping = {
        "time": ["time", "timestamp"],
        "x1": ["temperature", "temp", "x1"],
        "y1": ["wind speed", "windspeed", "wind", "y1"],
        "x2": ["relative humidity", "humidity", "rh", "x2"],
        "y2": ["fuel moisture", "moisture", "y2"],
    }

    rename_map = {}
    missing = []
    for canonical, options in mapping.items():
        found = None
        for opt in options:
            if opt in lower_cols:
                found = lower_cols[opt]
                break
        if found:
            rename_map[found] = canonical
        else:
            missing.append(canonical)

    if missing:
        raise ValueError(
            f"CSV must contain columns for {missing}. Found columns: {list(df.columns)}"
        )

    df = df.rename(columns=rename_map)
    return df
