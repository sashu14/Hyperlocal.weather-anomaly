import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import numpy as np

load_dotenv()

class WeatherDataHandler:
    def __init__(self, api_key=None, city="New York"):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.city = city
        self.base_url = "http://api.openweathermap.org/data/2.5/"
        
    def get_lat_lon(self):
        """Fetch coordinates for the given city."""
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={self.city}&limit=1&appid={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
        except Exception as e:
            print(f"Error fetching coordinates: {e}")
        return None, None

    def fetch_live_data(self):
        """Fetch current weather data."""
        if not self.api_key:
            return self._generate_mock_live_data()
        
        url = f"{self.base_url}weather?q={self.city}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return {
                'timestamp': datetime.fromtimestamp(data['dt']),
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed']
            }
        except Exception as e:
            print(f"Error fetching live data: {e}")
            return self._generate_mock_live_data()

    def fetch_historical_data(self, days=7):
        """
        Fetch historical data. Note: OpenWeatherMap free tier has limited historical data.
        If API key is missing or limit reached, returns synthetic data for development.
        """
        if not self.api_key:
            return self._generate_mock_historical_data(days)
        
        # Free tier only allows 5 days / 3 hours forecast. 
        # For actual historical data, high-tier subscription is needed.
        # We'll use the forecast API to get 'pseudo-historical' data or mock it.
        return self._generate_mock_historical_data(days)

    def _generate_mock_live_data(self):
        return {
            'timestamp': datetime.now(),
            'temp': 20 + np.random.normal(0, 5),
            'humidity': 50 + np.random.normal(0, 10),
            'pressure': 1013 + np.random.normal(0, 5),
            'wind_speed': 5 + np.random.normal(0, 2)
        }

    def _generate_mock_historical_data(self, days=7):
        dates = pd.date_range(end=datetime.now(), periods=24*days, freq='h')
        data = {
            'timestamp': dates,
            'temp': 20 + 10 * np.sin(np.arange(len(dates)) * 2 * np.pi / 24) + np.random.normal(0, 2, len(dates)),
            'humidity': 50 + 20 * np.cos(np.arange(len(dates)) * 2 * np.pi / 24) + np.random.normal(0, 5, len(dates)),
            'pressure': 1013 + np.random.normal(0, 3, len(dates)),
            'wind_speed': 5 + np.random.normal(0, 1, len(dates))
        }
        # Inject some anomalies
        df = pd.DataFrame(data)
        num_anomalies = 5
        for _ in range(num_anomalies):
            idx = np.random.randint(0, len(df))
            df.loc[idx, 'temp'] += 15 # Heat spike
            df.loc[idx+1, 'humidity'] -= 30 # Humidity drop
            
        return df
