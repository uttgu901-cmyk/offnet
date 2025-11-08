import json
import os
from datetime import datetime

class Weather:
    """Offline weather with cached data and forecasts"""
    
    def __init__(self):
        self.cache_file = os.path.expanduser("~/.offnet/weather_cache.json")
        self._load_cache()
    
    def _load_cache(self):
        """Load weather cache"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                self.cache = json.load(f)
        else:
            self.cache = {}
    
    def _save_cache(self):
        """Save weather cache"""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get_weather(self, city: str) -> dict:
        """Get weather for city (from cache)"""
        city_lower = city.lower()
        
        if city_lower in self.cache:
            data = self.cache[city_lower]
            # Check if data is still fresh (less than 1 hour old)
            if datetime.now().timestamp() - data.get('timestamp', 0) < 3600:
                return data
        
        # Simulate weather data (in real implementation, this would fetch from API)
        weather_data = self._generate_weather_data(city)
        self.cache[city_lower] = weather_data
        self._save_cache()
        
        return weather_data
    
    def _generate_weather_data(self, city: str) -> dict:
        """Generate simulated weather data"""
        import random
        
        # Simple hash-based "random" but consistent per city
        city_hash = hash(city) % 100
        temp_base = 15 + (city_hash - 50) / 2  # Base temp between -10°C and 35°C
        
        conditions = ['sunny', 'cloudy', 'rainy', 'snowy']
        condition = conditions[city_hash % len(conditions)]
        
        return {
            'city': city,
            'temperature': round(temp_base + random.uniform(-5, 5), 1),
            'condition': condition,
            'humidity': random.randint(30, 90),
            'wind_speed': round(random.uniform(0, 15), 1),
            'timestamp': datetime.now().timestamp(),
            'forecast': self._generate_forecast(city)
        }
    
    def _generate_forecast(self, city: str) -> list:
        """Generate 5-day forecast"""
        import random
        
        forecast = []
        city_hash = hash(city) % 100
        
        for day in range(5):
            temp_base = 15 + (city_hash - 50) / 2
            conditions = ['sunny', 'cloudy', 'rainy', 'snowy']
            condition = conditions[(city_hash + day) % len(conditions)]
            
            forecast.append({
                'day': day,
                'date': (datetime.now().timestamp() + day * 86400),
                'temperature': {
                    'high': round(temp_base + random.uniform(2, 8), 1),
                    'low': round(temp_base - random.uniform(2, 8), 1)
                },
                'condition': condition,
                'precipitation': random.randint(0, 90)
            })
        
        return forecast
