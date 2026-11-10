import requests
from django.conf import settings


def get_weather(city: str):
    if not settings.OPENWEATHER_API_KEY:
        return {'error': 'API key not set'}

    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': settings.OPENWEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru',
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            'city': data.get('name'),
            'temp': data['main']['temp'],
            'description': data['weather'][0]['description'],
        }
    except requests.RequestException as e:
        return {'error': str(e)}