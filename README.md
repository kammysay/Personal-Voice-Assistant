# **Personal Voice Assistant**

This is my remake of Amazon Alexa/Google Assistant. 

## **List of Commands** (keyword for command in bold, any sentence with that word will work)
1. "Hey, **Jack**" - wake the voice assistant, will accept other commands after this one.

2. "**Introduce** yourself" - summarizes available commands

3. "What **time** is it?" - reports the time

4. "What is the **date**?" - reports the date

5. "Tell me a **joke**" - Tells a joke using the [Official Joke API](https://github.com/15Dkatz/official_joke_api)

6. "What is the **weather**?" - reports the weather in your location using OpenWeather 

7. "**Play** (song)" - plays a song through Spotify

8. "**Play artist** (artist name)" - plays music from a specific artist

9. "**Play album** (album name)" - plays music from an album

10. "**Current/Skip/Previous** song" - I think you get it at this point

    

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