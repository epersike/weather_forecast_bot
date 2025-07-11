import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

def get_weather_forecast():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -26.9194,
        "longitude": -49.0661,
        "daily": ["sunset", "sunrise", "rain_sum", "temperature_2m_min", "temperature_2m_max", "apparent_temperature_max", "apparent_temperature_min", "precipitation_sum", "showers_sum", "snowfall_sum", "wind_speed_10m_max", "wind_direction_10m_dominant"],
        "timezone": "America/Sao_Paulo"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_sunset = daily.Variables(0).ValuesInt64AsNumpy()
    daily_sunrise = daily.Variables(1).ValuesInt64AsNumpy()
    daily_rain_sum = daily.Variables(2).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(3).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(4).ValuesAsNumpy()
    daily_apparent_temperature_max = daily.Variables(5).ValuesAsNumpy()
    daily_apparent_temperature_min = daily.Variables(6).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(7).ValuesAsNumpy()
    daily_showers_sum = daily.Variables(8).ValuesAsNumpy()
    daily_snowfall_sum = daily.Variables(9).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(10).ValuesAsNumpy()
    daily_wind_direction_10m_dominant = daily.Variables(11).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}

    daily_data["sunset"] = daily_sunset
    daily_data["sunrise"] = daily_sunrise
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
    daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["showers_sum"] = daily_showers_sum
    daily_data["snowfall_sum"] = daily_snowfall_sum
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant

    daily_dataframe = pd.DataFrame(data = daily_data)
    dict_daily_forecast = daily_dataframe.to_dict()
    return dict_daily_forecast