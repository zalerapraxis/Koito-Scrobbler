# Koito Scrobbler Service

## Introduction
This is a Python script that calls Spotify's API to fetch the currently playing track and scrobble it to a [Koito](https://github.com/gabehf/Koito) instance. This service runs continuously, checking for the currently playing track every 30 seconds.

Set up your environment variables in `config_secrets.py`:
   - `KOITO_ADDRESS`
   - `SPOTIPY_CLIENT_ID`
   - `SPOTIPY_CLIENT_SECRET`
   - `SPOTIPY_REDIRECT_URI`
   - `KOITO_API_KEY`


Run the script using Python:
```bash
python koito-scrobbler-service.py
```


koito-scrobbler.py just sort of shotguns tracks up to the Koito instance, and was more a PoC than anything. koito-scrobbler-service.py is intended to be run as a background service.
