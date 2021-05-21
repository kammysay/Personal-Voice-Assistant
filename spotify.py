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
def listDevices():
    devs = sp.devices()
    pp.pprint(devs)


# Add recommended songs to queue based on URI
def queue_recommended(uri, limit):
    # Find recommended songs
    queue = sp.recommendations(seed_tracks=[uri], limit=limit)

    # Add recommended songs to queue (can only add one at a time)
    i = 0
    while i < limit:
        try:
            track_uri = queue['tracks'][i]['uri']
            sp.add_to_queue(track_uri, device_id=device_id)
            i = i + 1
        except:
            pass


# Play a song on Spotify using Spotipy library
def play_song(text):
    # Building the search term
    text = text.replace("play ", "") # Removing the voice activation keyword
    new_text = text.replace(" ", "+")

    # Search for song
    songs = sp.search(q=new_text, type='track', limit=1)

    try:
        # Play requested song
        uri = songs['tracks']['items'][0]['uri']
        sp.start_playback(device_id=device_id, uris=[uri])

        # Add similar songs to queue
        queue_recommended(uri, 20)

        return ""
    except spotipy.exceptions.SpotifyException:
        return "I could not find an active device."
    except IndexError:
        return "I was unable to find the song ", text


# Play an album on Spotify
def play_album(text):
    # Building the search term
    text = text.replace("play ", "")  # Removing the voice activation keyword
    text = text.replace("album ", "") # Removing the album keyword
    new_text = text.replace(" ", "+")

    # Search for album
    albums = sp.search(q=new_text, type='album', limit=1)

    try:
        # Play requested album
        uri = albums['albums']['items'][0]['uri']
        sp.start_playback(device_id=device_id, context_uri=uri)
        return ""
    except spotipy.exceptions.SpotifyException:
        return "I could not find an active device."
    except:
        return "I was unable to find the album ", text


# Play from an artist on Spotify
def play_artist(text):
    # Building the search term
    text = text.replace("play ", "")  # Removing the voice activation keyword
    text = text.replace("artist ", "") # Removing the artist keyword
    new_text = text.replace(" ", "+")

    # Search for artist
    artists = sp.search(q=new_text, type='artist', limit=1)

    try:
        # Play requested artist
        uri = artists['artists']['items'][0]['uri']
        sp.start_playback(device_id=device_id, context_uri=uri)
        return ""
    except spotipy.exceptions.SpotifyException:
        return "I could not find an active device."
    except:
        return "I was unable to find the artist ", text


# Return the current song and artist
def current_song():
    try:
        # Call spotify API and check what song user is currently playing
        current = sp.current_playback(market=None, additional_types=None)

        # Extracting song title and artist name from current
        song = current['item']['name']
        artist = current['item']['album']['artists'][0]['name']

        # Building phrase
        phrase = "The current song is " + song + ", by " + artist
        return phrase
    except:
        return "You are not currently playing any music."


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