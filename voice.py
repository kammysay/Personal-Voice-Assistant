'''
The voice engine for the voice assistant
powered by the pyttsx3 library.
'''

import pyttsx3  # text to speech

class Voice():
    def __init__(self):
        # Text to Speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)

    # Make voice assistant speak
    def speak(self, phrase):
        self.engine.say(phrase)
        self.engine.runAndWait()