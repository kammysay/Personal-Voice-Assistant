# **Personal Voice Assistant**

This voice assistant uses Mozilla's open-source speech recognition framework, [DeepSpeech](https://github.com/mozilla/DeepSpeech). DeepSpeech is run locally to detect when the user is addressing the program, and will "wake up" when it hears the wake word. After waking up, it uses Google's Cloud Speech API to decipher commands. The reason for using Google's Cloud Speech API is because it is more accurate and accounts for context clues in speech recognition, which is important for commands such as Wikipedia searches and Spotify controls.

## **List of Commands** (keyword for command in bold, any sentence with that word will work)
1. "Hey, **Delta**" - wake the voice assistant, will accept other commands after this one.

2. "**Introduce** yourself" - summarizes available commands

3. "What **time** is it?" - reports the time

4. "What is the **date**?" - reports the date

5. "Tell me a **joke**" - Tells a joke using the [Official Joke API](https://github.com/15Dkatz/official_joke_api)

6. "**Kanye** quote" - Reads a quote from Kanye West using the [kanye.rest API](https://kanye.rest/)

7. "**Define** (word)" - defines a word using [Free Dictionary API](https://dictionaryapi.dev/)

8. "What is the **weather**?" - reports the current weather in your location using OpenWeather 

9. "What is the **weather today/tomorrow/(specific day)**?" - gives the forecast for the requested day

10. "**Search** (topic)" - searches for a topic on Wikipedia and returns a brief summary

11. "**Search random**" - searches a random topic on Wikipedia and returns a brief summary

12. "**Play** (song)" - plays a song through Spotify

13. "**Play artist/album/playlist** (artist/album/playlist name)" - plays music from a specific artist or album

14. "**Current/Skip/Previous** song" - I think you get it at this point

    

## **Setup**
---
### How to Run
First, it is needed to download a voice model from Mozilla (too big to include in this repo, sadly)
- For information on how to install that, visit https://deepspeech.readthedocs.io/en/r0.9/
- Ensure that the model file ending in .pbmm and .scorer are in the Personal-Voice-Assistant directory.

To automatically run Delta on a Raspberry Pi, it is needed to setup run_assistant.sh to run at startup
- To do this, enter a terminal window, type ```sudo crontab -e```
- Scroll to the bottom of this file and add the line ```@reboot python3 (PATH TO PERSONAL VOICE ASSISTANT DIRECTORY)/Personal-Voice-Assistant/run_assistant.sh &```
- Save this file and reboot the Raspberry Pi. On startup the script should automatically run the assistant.

Alternatively, it is possible to manually start the assistant.
- Run the command ```python3 mic_vad_streaming.py -m deepspeech-0.9.3-models.pbmm -s deepspeech-0.9.3-models.scorer```.
- The program will now listen for it's wake-word, and is ready to use.

### Weather Updates
- An API key from [OpenWeatherAPI](https://openweathermap.org/api) is needed to use the weather feature.
  - In ```user.json``` add your city on the line ```"location": "City,us"```
  - In ```user.json``` copy/paste the API key into the line ```"api_key": "API KEY HERE"```

### Spotify Control
- Create a new [Spotify development project](https://developer.spotify.com/dashboard/applications) to use the Spotify feature
  - In ```user.json``` copy/paste the Client ID given by the new project into the line ```"client_id": "CLIENT ID"```
  - In ```user.json``` copy/paste the Client Secret into the line ```"client_secret": "CLIENT SECRET"```
  - In ```user.json``` add username in the line ```"username": "USERNAME"```
  - Under ```Edit settings``` on the Spotify developer project add the URL ```https://example.com/callback/``` to the ```Redirect URIs``` field

## Dependencies

---

1. ```pip3 install deepspeech```
2. ```pip3 install speechrecognition```
3. ```pip3 install pyaudio```
4. ```pip3 install pyttsx3```
5. ```pip3 install spotipy```
6. ```pip3 install wikipedia```