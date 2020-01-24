"""
##### WEATHER #####

This module contains the WeatherGetter class for dealing with weather via the Dark Sky API.

"""

import requests


class WeatherGetter():
    def __init__(self):
        self.request_url = 'https://api.darksky.net/forecast'
        self.api_key = 'e6bfcec2ea2816540bd5b4cb01a3950e'
        
        # Chicago latitude & longitude: 41.8781° N, 87.6298° W (West Longitude represented as negative)
        self.latitude = '41.8781'
        self.longitude = '-87.6298'
        self.excludes = 'exclude=currently,minutely,daily,alerts,flags'
        self.weather_on_date = {}
            
    def get_weather(self, date_string):
        # if weather already fetched for that date, return it from object's weather_on_date dictionary
        
        weather = self.weather_on_date.get(date_string)
        if weather: return weather
        
    
        # otherwise get weather using Dark Sky API
        # Dark Sky request url - https://api.darksky.net/forecast/[key]/[latitude],[longitude],[time]
        # datetime string format - [YYYY]-[MM]-[DD]T[HH]:[MM]:[SS]
        
        url = f'{ self.request_url }/{ self.api_key }/{ self.latitude },{ self.longitude },{ date_string }T00:00:00?{ self.excludes }'
        
        response = requests.get(url) #, headers=self.headers)
        weather = response.json()
        
        self.weather_on_date[date_string] = weather
        
        return weather