import openmeteo_requests
import requests
import pandas as pd
import requests_cache
from retry_requests import retry

from utils import reformat_weather_data


def get_weather_forecast(city: str, country_code: str):
    """
    Busca as coordenadas (latitude e longitude) para uma cidade e país
    usando a API de geocodificação e, em seguida, obtém a previsão do tempo.

    Args:
        city (str): O nome da cidade.
        country_code (str): O código do país no formato ISO 3166-1 alpha-2.

    Returns:
        dict: Um dicionário com os dados da previsão do tempo ou None se a cidade não for encontrada.
    """
    # Configura a sessão para a chamada da API de geocodificação com cache e retentativas
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "countryCode": country_code,
        "count": 1,
        "language": "pt",
        "format": "json"
    }

    try:
        response = retry_session.get(geocoding_url, params=params)
        response.raise_for_status()  # Lança uma exceção para respostas com erro (4xx ou 5xx)
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            location = data["results"][0]
            lat = location["latitude"]
            long = location["longitude"]
            # Chama a função interna para obter a previsão do tempo
            return reformat_weather_data(_get_weather_forecast(lat, long))
        else:
            print(f"Erro: Cidade '{city}' com código de país '{country_code}' não encontrada.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao chamar a API de geocodificação: {e}")
        return None

def _get_weather_forecast(lat: float, long: float):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, #-26.9194,
        "longitude": long, #-49.0661,
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