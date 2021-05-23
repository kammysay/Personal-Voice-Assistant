'''
A collection of mostly unrelated functions
'''

# Imports
import datetime
import requests

# Give a brief overview of functionality
def introduction(voice, name):
    phrase = "Hello, I'm " + name + ". I can tell you the date and time, the weather, control spotify or even search wikipedia for you. See GitHub for a full list of instructions"
    voice.speak(phrase)


# Fetch the current time
def fetch_time(voice):
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

    voice.speak(phrase)


# Fetch today's date
def fetch_date(voice):
    date = datetime.date.today().strftime("%B, %d, %Y")
    voice.speak("Today is " + date)


# Fetch a joke from Official Joke API
def fetch_joke(voice):
    url = "https://official-joke-api.appspot.com/random_joke"
    req = requests.get(url)

    setup = req.json()['setup'] + "             " # Empty string is for timing
    punchline = req.json()['punchline']

    voice.speak(setup)
    voice.speak(punchline)


# Fetch a Kanye quote
def fetch_yeezy(voice):
    url = "https://api.kanye.rest/"
    req = requests.get(url)

    voice.speak(req.json()['quote'] + ".          Kanye West") # Empty string is for timing


# Define a word using free dictionary api
def define_word(voice, text):
    # Building URL
    text = text.replace("define ", "")
    text = text.replace(" ", "")
    url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
    req = requests.get(url)

    # Determine if there multiple definitions
    entries = req.json()[0]['meanings']
    if len(entries) > 1:
        voice.speak("Multiple definitions found.")

    # For each part of report possible definitions
    i = 0
    for entry in entries:
        part_of_speech = req.json()[0]['meanings'][i]['partOfSpeech']
        phrase = "As a " + part_of_speech + ", " + text + " can mean "

        # Report each definition
        definitions = req.json()[0]['meanings'][i]['definitions']
        definition_count = len(definitions)
        j = 0
        for definition in definitions:
            phrase = phrase + req.json()[0]['meanings'][i]['definitions'][j]['definition']
            if j < definition_count - 1:
                phrase = phrase + " or "
            j = j + 1
        i = i + 1
        
        voice.speak(phrase)