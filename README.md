# Koito Scrobbler Service

## Introduction
This is a Python script that calls Spotify's API to fetch the currently playing track and scrobble it to a Koito instance. This service runs continuously, checking for the currently playing track every 30 seconds.

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