import pandas as pd


def get_prescription_parameters() -> dict:
    rx_map = {}
    rx_map["min_temp"] = 60
    rx_map["max_temp"] = 80
    rx_map["min_rh"] = 65
    rx_map["max_rh"] = 35
    rx_map["min_wind"] = 0
    rx_map["max_wind"] = 12
    rx_map["min_fuel"] = 15
    rx_map["max_fuel"] = 8

    return rx_map

def set_axis_parameters(resourceData: pd.DataFrame) -> dict:
    axis_map = {}
    axis_map["temp_min"] = resourceData['Temp'].min()
    axis_map["temp_max"] = resourceData['Temp'].max()
    axis_map["rh_min"] = resourceData['RH'].min()
    axis_map["rh_max"] = resourceData['RH'].max()
    axis_map["wind_min"] = resourceData['Wind'].min()
    axis_map["wind_max"] = resourceData['Wind'].max()
    axis_map["fuel_min"] = resourceData['Fuel Moisture'].min()
    axis_map["fuel_max"] = resourceData['Fuel Moisture'].max()
    axis_map["x_padding"] = (axis_map["temp_max"] - axis_map["temp_min"]) * 0.1
    axis_map["y_padding"] = (axis_map["wind_max"] - axis_map["wind_min"]) * 0.1
    return axis_map