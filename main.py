# Imports
import speech_recognition as sr # for listening to user commands
import pyttsx3  # for text to speech
import datetime # date and time
import spotipy  # play music through spotify
from spotipy.oauth2 import SpotifyOAuth
import spotify as sp # play music through spotify (local file)
import json
import requests # for API calls

# Recognizer and Microphone
r = sr.Recognizer()
mic = sr.Microphone()

# Text to Speech engine
engine = pyttsx3.init()

# Constants
WAKE_NAME = "jack"

# Importing data from user.json
user_file = open("user.json")
user = json.load(user_file)

# Make voice assistant speak
def speak(phrase):
    engine.say(phrase)
    engine.runAndWait()


# Give a brief overview of functionality
def introduction():
    speak("Hello, I'm Jack. I can tell you the date and time, give weather updates and control spotify for you. I can even tell you a joke.")


# Fetch the current time
def fetchTime():
    # Getting hour and minute
    time = datetime.datetime.now().strftime("%H %M")
    numbers = time.split()
    hour = int(numbers[0])
    minute = numbers[1]
    partofday = "a m" # AM or PM

    # Converting to 12 hour format
    if hour > 12:
        hour = hour - 12
        partofday = "pm"

    # TTS pronounces 6:04 as "six zero four" instead of "six oh four". Fixing that here.
    if minute[0] == '0' and minute[1] != '0':
        minute = "oh" + minute[1]

    # If the minute is 00
    if minute[0] == '0' and minute[1] == '0':
        phrase = "It is currently " + str(hour) + " " + partofday
    else:
        phrase = "It is currently" + str(hour) + " " + minute + " " + partofday

    speak(phrase)


# Fetch today's date
def fetchDate():
    date = datetime.date.today().strftime("%B, %d, %Y")
    phrase = "Today is " + date
    speak(phrase)


# Fetch a joke from Official Joke API
def fetchJoke():
    url = "https://official-joke-api.appspot.com/random_joke"
    req = requests.get(url)

    setup = req.json()['setup'] + "             " # Empty string is for timing
    punchline = req.json()['punchline']

    speak(setup)
    speak(punchline)


# Get the weather using the OpenWeatherAPI (free version)
def fetchWeather():
    # Building URL
    LINK = "https://api.openweathermap.org/data/2.5/weather?q="
    location = user['weather']['location']
    api_key = user['weather']['api_key']
    url = LINK + location + api_key
    req = requests.get(url) # holds the response from the API

    # Extracting relevant parts of request
    location = req.json()['name']
    temp = 1.8 * (req.json()['main']['temp'] - 273) + 32 # Converting Kelvin to Fahrenheit
    feels_like = 1.8 * (req.json()['main']['feels_like'] - 273) + 32
    desc = req.json()['weather'][0]['description']
    
    # Putting forecast together, making hector speak
    phrase = "Right now, in " + location + ", it is " + str(int(temp)) + " degrees, with a real feel of " + str(int(feels_like)) + " degrees. You can expect " + desc
    speak(phrase)


# Play music on Spotify using Spotipy library
def playMusic(text):
    # Chose action based on keyword
    if "artist" in text: # Play from an artist
        speak(sp.play_artist(text))
    elif "album" in text: # Play from an album
        speak(sp.play_album(text))
    elif "pause" in text: # Pause the current track
        sp.pause()
    elif "skip" in text: # Skip the current track
        sp.skip_song()
    elif "previous" in text: # Play the previous track
        sp.prev_song()
    elif "current" in text: # Say the current track
        phrase = sp.current_song()
        speak(phrase)
    else: # Play song
        speak(sp.play_song(text))
        

# Execute functions based on voice input
def inputCommand():
    speak("What do you need?")
    with sr.Microphone() as source:
        # audio = r.listen(source, 10, 5)
        audio = r.listen(source, phrase_time_limit=5)
        try:
            # text = r.recognize_sphinx(audio)
            text = r.recognize_google(audio)
            # Function calls based on keywords
            # Online functions
            if "weather" in text:
                fetchWeather()
            elif "play" in text or "song" in text:
                playMusic(text)
            elif "joke" in text:
                fetchJoke()
            
            # Offline functions
            elif "introduce" in text:
                introduction()
            elif "time" in text:
                fetchTime()
            elif "today" in text:
                fetchDate()
            elif "thank" in text or "thanks" in text:
                speak("Correct.")

        except sr.RequestError:
            speak("Sorry, something went wrong.")

        except sr.UnknownValueError:
            speak("Nevermind then.")

# Main program loop, waiting for activation here
while True:
    with sr.Microphone() as source:
        print("Say: Hey, Jack.")

        # Listen to microphone
        audio = r.listen(source, phrase_time_limit=2) # Setting phrase time limit to a short interval since it only listens for one keyword
        try:
            # Using the sphinx engine here because it doesn't need an internet connection
            text = r.recognize_sphinx(audio)
            print(text)
            if WAKE_NAME in text:
                inputCommand()

        except sr.UnknownValueError: # If the API couldn't decipher anything being said/if nothing is said
            pass