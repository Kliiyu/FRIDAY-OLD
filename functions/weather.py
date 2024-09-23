import requests
import sys
import json
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="config\.env")

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        wind = data['wind']
        weather = data['weather'][0]

        report = {
            'city': data['name'],
            'temperature': main['temp'],
            'pressure': main['pressure'],
            'humidity': main['humidity'],
            'weather_description': weather['description'],
            'wind_speed': wind['speed']
        }

        return report
    else:
        return f"Error: Unable to fetch weather data for {city}. HTTP Status code: {response.status_code}"
    
def main():
    api_key = os.getenv("WEATHER_API_KEY")
    
    city = ""
    if len(sys.argv) < 2:
        city = "Stavanger"
    else:
        city = sys.argv[1]

    weather_report = get_weather(api_key, city)

    if isinstance(weather_report, dict):
        print(f"Weather report for {weather_report['city']}:")
        print(f"Temperature: {weather_report['temperature']}°C")
        print(f"Pressure: {weather_report['pressure']} hPa")
        print(f"Humidity: {weather_report['humidity']}%")
        print(f"Weather: {weather_report['weather_description']}")
        print(f"Wind Speed: {weather_report['wind_speed']} m/s")
    else:
        print(weather_report)

if __name__ == "__main__":
    main()