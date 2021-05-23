'''
A collection of functions used to report the weather in a location
using the free version of the OpenWeather API
'''

# imports
import requests # for reaching API
import json # parse user.json
from datetime import datetime
from collections import deque

# Open user.json
user_file = open("user.json")
user = json.load(user_file)

# Accessing current weather version of API to extract latitude and longitude of city
# Building URL
user_link = "https://api.openweathermap.org/data/2.5/weather?q="
user_location = user['weather']['location']
user_key = user['weather']['api_key']
user_url = user_link + user_location + "&APPID=" + user_key
req = requests.get(user_url)
# Extract latitude and longitude, city name
lat = req.json()['coord']['lat']
lon = req.json()['coord']['lon']
city = req.json()['name']

# Fetch the weather from API
def fetch_weather():
    # Building URL for request
    link = "https://api.openweathermap.org/data/2.5/onecall?"
    coords = "lat=" + str(lat) + "&lon=" + str(lon)
    exclude = "&exclude=minutely,hourly,alerts"
    units = "&units=imperial"
    key = "&appid=" + user_key
    url = link + coords + exclude + units + key
    return requests.get(url)


# Extract & report weather forecast for a specified day
def extract_weather(voice, day_index, day):
    weather = fetch_weather()

    min_temp = weather.json()['daily'][day_index]['temp']['min']
    max_temp = weather.json()['daily'][day_index]['temp']['max']
    day_temp = weather.json()['daily'][day_index]['temp']['day']
    desc = weather.json()['daily'][day_index]['weather'][0]['description']

    phrase = day + ", in " + city + ", you can expect " + str(desc) + ". There will be a minn of " + str(int(min_temp)) + " degrees and a max of " + str(int(max_temp)) + " degrees. During the day you can expect it to be around " + str(int(day_temp)) + " degrees"
    voice.speak(phrase)


# Report the current weather
def current_weather(voice):
    weather = fetch_weather()

    temp = weather.json()['current']['temp']
    feels_like = weather.json()['current']['feels_like']
    desc = weather.json()['current']['weather'][0]['description']

    phrase = "Currently, in " + city + ", it is " + str(int(temp)) + " degrees, with a real feel of " + str(int(feels_like)) + " degrees. You can expect " + desc
    voice.speak(phrase)


# Report today's weather forecast
def todays_weather(voice):
    extract_weather(voice, 0, "Today")


# Report tomorrow's weather forecast
def tomorrows_weather(voice):
    extract_weather(voice, 1, "Tomorrow")


# Report the weather on a specific day
def days_weather(voice, day):
    # List of days in the week
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Get the index of the current day
    today_index = datetime.today().weekday()

    # Shift list so that current day is the 0th element
    weekdays = deque(weekdays)
    weekdays.rotate(-today_index)
    weekdays = list(weekdays)

    # Get the index of the requested day
    day_index = weekdays.index(day)

    extract_weather(voice, day_index, weekdays[day_index])