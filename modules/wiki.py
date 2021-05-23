'''
A collection of functions used to search Wikipedia
using the Wikipedia library.
'''

# Imports
import wikipedia as wiki
import warnings

# Ignore warnings from wikipedia library
warnings.catch_warnings()
warnings.simplefilter("ignore")

# Find informatiom about a given topic
def search(voice, text):
    text = text.replace("search ", "")

    try:
        result = wiki.summary(text, sentences=3, auto_suggest=True, redirect=True)
        voice.speak(result)

    except wiki.PageError:
        # No page found
        voice.speak("I could not find an article titled " + text)

    except wiki.DisambiguationError as e:
        # If multiple articles have the same name, read the most relevant one
        may_refer_to = e.args[1]

        article = may_refer_to[0]
        article = article.replace("(", "")
        article = article.replace(")", "")
        result = wiki.summary(article, sentences=3, auto_suggest=True, redirect=True)
        print(result)
        voice.speak(result)
        
    except wiki.WikipediaException:
        # If something else happened
        voice.speak("Something happened on Wikipedia's end, no article returned.")

def random_article(voice):
    page = wiki.random(pages=1)

    try:
        result = wiki.summary(page, sentences=3, auto_suggest=True, redirect=True)
        voice.speak("Article title " + page + ". Article summary:        " + result)

    except wiki.PageError:
        # If there was an error with finding the random article
        print(result)
        voice.speak("Something went wrong, I could not find a random article.")

    except wiki.WikipediaException:
        # If something else happened
        voice.speak("Something happened on Wikipedia's end, no article returned.")