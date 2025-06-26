# Koito Scrobbler Service

## Introduction
This is a Python script that calls Spotify's API to fetch the currently playing track and scrobble it to a [Koito](https://github.com/gabehf/Koito) instance. This service runs continuously, checking for the currently playing track every 30 seconds.

koito-scrobbler.py just sort of shotguns tracks up to the Koito instance, and was more a PoC than anything. koito-scrobbler-service.py is intended to be run as a background service.

Set up your environment variables:
   - `SPOTIPY_CLIENT_ID`
   - `SPOTIPY_CLIENT_SECRET`
   - `SPOTIPY_REDIRECT_URI`
   - `KOITO_API_KEY`
   - `KOITO_ADDRESS`


Run the script using Python:
```bash
python koito-scrobbler-service.py
```

For running in Docker, You'll need to run the script locally to authenticate and get the `.cache` file, copy that over to your volume mount. I couldn't get fully headless authentication working and I'm too lazy to keep trying.  

