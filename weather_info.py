import requests
from datetime import datetime


def weather_info(text):
    parameters = {
        'appid': 'd5fbd0ac1714c5756709f2a13b939dba',
        'units': 'metric',
        'lang': 'ru'
    }
    parameters['q'] = text
    weather = requests.get('https://api.openweathermap.org/data/2.5/weather', params=parameters).json()
    name = weather['name']
    temp = weather['main']['temp']
    description = weather['weather'][0]['description']
    wind_speed = weather['wind']['speed']
    timezone = weather['timezone']
    sunrise = datetime.utcfromtimestamp(weather['sys']['sunrise'] + timezone).strftime('%H:%M:%S  %d.%m.%Y')
    sunset = datetime.utcfromtimestamp(weather['sys']['sunset'] + timezone).strftime('%H:%M:%S  %d.%m.%Y')
    return  f"""
🏙 Погода в городе  {name}
📍 Сейчас: {description}
🌡 Температура:{temp}°C
💨 Ветер: {wind_speed} м/с
🌅 Рассвет: {sunrise}
🌇 Закат: {sunset}
"""