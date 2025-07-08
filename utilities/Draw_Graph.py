import matplotlib.pyplot as plt
import os

def set_axis(axis_settings: dict):
    fig, axis = plt.subplots(figsize=(12, 9))

    # RH on top X-axis
    axis_rh = axis.twiny()
    axis_rh.set_xlabel("Relative Humidity")
    axis_rh.set_xlim(axis_settings["rh_min"] - axis_settings["x_padding"],
                     axis_settings["rh_max"] + axis_settings["x_padding"])

    # Fuel Moisture on right Y-axis
    axis_fuel = axis.twinx()
    axis_fuel.set_ylabel("Fuel Moisture")
    axis_fuel.set_ylim(axis_settings["fuel_min"] - axis_settings["y_padding"],
                       axis_settings["fuel_max"] + axis_settings["y_padding"])

    # Main axes
    axis.set_xlabel("Temperature")
    axis.set_ylabel("Wind Speed")
    axis.set_xlim(axis_settings["temp_min"] - axis_settings["x_padding"],
                  axis_settings["temp_max"] + axis_settings["x_padding"])
    axis.set_ylim(axis_settings["wind_min"] - axis_settings["y_padding"],
                  axis_settings["wind_max"] + axis_settings["y_padding"])

    axis.grid(True)
    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/grid.png", dpi=300)
