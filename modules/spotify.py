'''
A collection of functions used to control Spotify
using the Spotipy library
'''

# Imports
import spotipy  # play music through spotify
from spotipy.oauth2 import SpotifyOAuth
import json
import pprint
pp = pprint.PrettyPrinter()

# Importing data from user.json
user_file = open("user.json")
user = json.load(user_file)

# Variables for SpotifyOAuth
client_id = user['spotify']['client_id']
client_secret = user['spotify']['client_secret']
scope = "user-read-currently-playing user-read-playback-position user-modify-playback-state user-read-playback-state"
username = user['spotify']['username']
redirect_uri = "https://example.com/callback/" # This is just a bogus link

device_id = "" # need to add this manually rn

# Spotify object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
client_id=client_id, client_secret=client_secret, scope=scope, username=username, redirect_uri=redirect_uri))

# List available devices
def list_devices():
    devs = sp.devices()
    pp.pprint(devs)


# Play a song on Spotify, play similar songs afterwards
def play_song(voice, text):
    # Building the search term
    text = text.replace("play ", "") # Removing the voice activation keyword
    new_text = text.replace(" ", "+")

    # Search for song
    song = sp.search(q=new_text, type='track', limit=1)

    try:
        # Get song uri song
        song_uri = song['tracks']['items'][0]['uri']
        # Get artist uri for recommendations()
        artist_uri = song['tracks']['items'][0]['artists'][0]['uri']
        # Find similar songs to play afterwards
        queue = sp.recommendations(seed_artists=[artist_uri],seed_tracks=[song_uri], limit=20)

        # Add recommended songs to queue (can only add one at a time)
        uris = [song_uri]
        i = 0
        while i < 20:
            try:# Add recommened song to queue
                uris.append(queue['tracks'][i]['uri'])
                i = i + 1
            except:
                break
        
        sp.start_playback(device_id=device_id, uris=uris, offset={"uri": song_uri})

    except spotipy.exceptions.SpotifyException:
        voice.speak("I could not find an active device")
    except IndexError:
        phrase = "I was unable to find the song " + text
        voice.speak(phrase)


# Play an album on Spotify
def play_album(voice, text):
    # Building the search term
    text = text.replace("play ", "")  # Removing the voice activation keyword
    text = text.replace("album ", "") # Removing the album keyword
    new_text = text.replace(" ", "+")

    # Search for album
    albums = sp.search(q=new_text, type='album', limit=1)

    try:
        # Play requested album
        uri = albums['albums']['items'][0]['uri']

        # Start album from beginning (not shuffled)
        sp.shuffle(state=False)
        sp.start_playback(device_id=device_id, context_uri=uri)

    except spotipy.exceptions.SpotifyException:
        voice.speak("I could not find an active device.")
    except:
        phrase = "I was unable to find the album " + text
        voice.speak(phrase)


# Play from an artist on Spotify
def play_artist(voice, text):
    # Building the search term
    text = text.replace("play ", "")  # Removing the voice activation keyword
    text = text.replace("artist ", "") # Removing the artist keyword
    new_text = text.replace(" ", "+")

    # Search for artist
    artists = sp.search(q=new_text, type='artist', limit=1)

    try:
        # Play requested artist
        uri = artists['artists']['items'][0]['uri']

        sp.shuffle(state=True)
        sp.start_playback(device_id=device_id, context_uri=uri)

    except spotipy.exceptions.SpotifyException:
        voice.speak("I could not find an active device.")
    except:
        phrase = "I was unable to find the artist " + text
        voice.speak(phrase)


# Play a playlist on spotify
def play_playlist(voice, text):
    # Building search term
    text = text.replace("play ", "") # Removing voice activation keyword
    text = text.replace("playlist ", "") # Removing playlist keyword
    new_text = text.replace(" ", "+")

    playlists = sp.search(q=new_text, type='playlist', limit=1)

    try:
        # Play requested artist
        uri = playlists['playlists']['items'][0]['uri']

        sp.shuffle(state=True)
        sp.start_playback(device_id=device_id, context_uri=uri)

    except spotipy.exceptions.SpotifyException:
        voice.speak("I could not find an active device.")
    except:
        phrase = "I was unable to find the playlist " + text
        voice.speak(phrase)


# Return the current song and artist
def current_song(voice):
    try:
        # Call spotify API and check what song user is currently playing
        current = sp.current_playback(market=None, additional_types=None)

        # Extracting song title and artist name from current
        song = current['item']['name']
        artist = current['item']['album']['artists'][0]['name']

        # Building phrase
        phrase = "The current song is " + song + ", by " + artist
        voice.speak(phrase)
    except:
        voice.speak("You are not currently playing any music.")


# Pause the user's currently playing song
def pause():
    try:
        sp.pause_playback()
    except:
        pass


# Skip to the next song in user's queue
def skip_song():
    try:
        sp.next_track()
    except:
        pass


# Go back to previous song
def prev_song():
    try:
        sp.previous_track()
    except:
        pass