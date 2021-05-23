# **Personal Voice Assistant**

This is Delta, my remake of Amazon Alexa/Google Assistant. 

## **List of Commands** (keyword for command in bold, any sentence with that word will work)
1. "Hey, **Delta**" - wake the voice assistant, will accept other commands after this one.

2. "**Introduce** yourself" - summarizes available commands

3. "What **time** is it?" - reports the time

4. "What is the **date**?" - reports the date

5. "Tell me a **joke**" - Tells a joke using the [Official Joke API](https://github.com/15Dkatz/official_joke_api)

6. "**Kanye** quote" - Reads a quote from Kanye West using the [kanye.rest API](https://kanye.rest/)

7. "What is the **weather**?" - reports the current weather in your location using OpenWeather 

8. "What is the **weather today/tomorrow/(specific day)**?" - gives the forecast for the requested day

9. "**Search** (topic)" - searches for a topic on Wikipedia and returns a brief summary

10. "**Play** (song)" - plays a song through Spotify

11. "**Play artist/album** (artist/album name)" - plays music from a specific artist or album

12. "**Current/Skip/Previous** song" - I think you get it at this point

    

## **Setup**

---

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