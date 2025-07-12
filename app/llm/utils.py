import pandas as pd

import json

def reformat_weather_data(data):
    # Convert 'date' dictionary into a pandas Series and parse timestamps
    date_series = pd.Series(data['date']).apply(lambda ts: pd.to_datetime(ts).strftime('%Y-%m-%d'))

    # Initialize the reformatted dictionary
    reformatted_data = {}

    # Loop through each index and construct the daily data
    for i, date in date_series.items():
        reformatted_data[date] = {
            "sunrise": data['sunrise'][i],
            "sunset": data['sunset'][i],
            "rain_sum": data['rain_sum'][i],
            "temperature_2m_min": data['temperature_2m_min'][i],
            "temperature_2m_max": data['temperature_2m_max'][i],
            "apparent_temperature_max": data['apparent_temperature_max'][i],
            "apparent_temperature_min": data['apparent_temperature_min'][i],
            "precipitation_sum": data['precipitation_sum'][i],
            "showers_sum": data['showers_sum'][i],
            "snowfall_sum": data['snowfall_sum'][i],
            "wind_speed_10m_max": data['wind_speed_10m_max'][i],
            "wind_direction_10m_dominant": data['wind_direction_10m_dominant'][i],
        }

    return reformatted_data