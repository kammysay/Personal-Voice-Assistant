# Imports
import speech_recognition as sr # for listening to user commands
import voice # voice engine (local import)
from modules import potpourri as p
from modules import spotify as sp # play music through spotify (local import)
from modules import weather as w  # weather updates (local import)
from modules import wiki # search wikipedia (local import)

# Recognizer and Microphone
r = sr.Recognizer()
mic = sr.Microphone()

# Text to Speech engine
v = voice.Voice()

# Constants
WAKE_NAME = "delta"

# Play music on Spotify using Spotipy library
def playMusic(text):
    # Chose action based on keyword
    if "artist" in text: # Play from an artist
        sp.play_artist(v, text)
    elif "album" in text: # Play from an album
        sp.play_album(v, text)
    elif "playlist" in text:
        sp.play_playlist(v, text)
    elif "pause" in text or "stop" in text: # Pause the current track
        sp.pause()
    elif "skip" in text: # Skip the current track
        sp.skip_song()
    elif "previous" in text: # Play the previous track
        sp.prev_song()
    elif "current" in text: # Say the current track
        sp.current_song(v)
    else: # Play song
        sp.play_song(v, text)

# Get the weather report
def fetchWeather(text):
    # Chose action based on keyword
    # Using manual return statements since we use a loop instead of an elif for days_weather()
    if "today's" in text or "today" in text:
        w.todays_weather(v)
        return
    elif "tomorrow's" in text or "tomorrow" in text:
        w.tomorrows_weather(v)
        return
    
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    i = 0
    for day in weekdays:
        if weekdays[i] in text:
            w.days_weather(v, weekdays[i])
            return
        i = i + 1

    w.current_weather(v)


# Search wikipedia
def search_wiki(text):
    if "random" in text:
        wiki.random_article(v)
    else:
        wiki.search(v, text)
        

# Execute functions based on voice input
# Uses Google's voice recognition here instead of Mozilla's Deepspeech, as it take in longer
# sentences and is more accurate than Deepspeech
def inputCommand():
    v.speak("What do you need?")
    with sr.Microphone() as source:
        # audio = r.listen(source, 10, 5)
        audio = r.listen(source, phrase_time_limit=5)
        try:
            d
            text = r.recognize_google(audio)
            text = text.lower()

            print(text)
            # Function calls based on keywords
            # Online functions
            if "weather" in text:
                fetchWeather(text)
            elif "play" in text or "song" in text or "music" in text or "artist" in text or "album" in text:
                playMusic(text)
            elif "search" in text:
                search_wiki(text)
            elif "joke" in text:
                p.fetch_joke(v)
            elif "Kanye" in text:
                p.fetch_yeezy(v)
            
            # Offline functions
            elif "introduce" in text:
                p.introduction(v, WAKE_NAME)
            elif "time" in text:
                p.fetch_time(v)
            elif "today" in text:
                p.fetch_date(v)
            elif "thank" in text or "thanks" in text:
                v.speak("Yeah, whatever.")

        except sr.RequestError:
            v.speak("Sorry, something went wrong.")

        except sr.UnknownValueError:
            v.speak("Nevermind then.")