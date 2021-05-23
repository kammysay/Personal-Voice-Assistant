'''
A collection of functions used to search Wikipedia
using the Wikipedia library.
'''

import wikipedia as wiki

# Find informatiom about a given topic
def search(voice, text):
    text = text.replace("search ", "")
    result = wiki.summary(text, sentences=3, auto_suggest=True, redirect=True)

    voice.speak(result)