import requests
import pandas as pd
import json

def fetch_weather_data(lat=13.7563, lon=100.5018):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "precipitation,wind_speed_10m,wind_direction_10m",
        "timezone": "Asia/Bangkok",
        "forecast_days": 2
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        df_weather = pd.DataFrame(data['hourly'])
        df_weather['time'] = pd.to_datetime(df_weather['time'])
        df_weather.set_index('time', inplace=True)
        return df_weather
    except Exception as e:
        print(f"Weather API Error: {e}")
        return None

def load_tide_data(filepath="tide_2026.json"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tide_data = json.load(f)
        df_tide = pd.DataFrame(tide_data)
        df_tide['time'] = pd.to_datetime(df_tide['time'])
        df_tide.set_index('time', inplace=True)
        return df_tide
    except FileNotFoundError:
        print(f"Tide JSON file not found: {filepath}")
        return pd.DataFrame()