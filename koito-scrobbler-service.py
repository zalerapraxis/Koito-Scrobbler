import os
import time
import requests
import spotipy
import datetime
from spotipy.oauth2 import SpotifyOAuth

# Try to import config_secrets, handle if it doesn't exist
try:
    import config_secrets
except ImportError:
    config_secrets = None

def get_config_value(key, default=None):
    # Check environment variables first
    value = os.getenv(key)
    if value is not None:
        return value
    
    # Check config_secrets if available
    if config_secrets and hasattr(config_secrets, key):
        return getattr(config_secrets, key)
    
    # Return default if not found
    return default

# Load configuration
config = {
    'KOITO_ADDRESS': get_config_value('KOITO_ADDRESS'),
    'SPOTIPY_CLIENT_ID': get_config_value('SPOTIPY_CLIENT_ID'),
    'SPOTIPY_CLIENT_SECRET': get_config_value('SPOTIPY_CLIENT_SECRET'),
    'SPOTIPY_REDIRECT_URI': get_config_value('SPOTIPY_REDIRECT_URI'),
    'KOITO_API_KEY': get_config_value('KOITO_API_KEY'),
}

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config['SPOTIPY_CLIENT_ID'],
    client_secret=config['SPOTIPY_CLIENT_SECRET'],
    redirect_uri=config['SPOTIPY_REDIRECT_URI'],
    scope="user-read-currently-playing",
    cache_path=".cache",
    open_browser=False
))

def get_current_track():
    """Fetch the currently playing track from Spotify."""
    try:
        current_track = sp.current_user_playing_track()
        if current_track and current_track['is_playing']:
            track = current_track['item']
            track_info = {
                'artist': track['artists'][0]['name'],
                'track': track['name'],
                'album': track['album']['name'],
                'duration': track['duration_ms'],
                'played_at': current_track['timestamp']
            }
            return track_info
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}. HTTP Status: {e.http_status}, Code: {e.code}, Message: {e.msg}, Reason: {e.reason}", flush=True)
    return None

last_scrobbled_track = None

def scrobble_track(track_info):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Scrobbling: {track_info['artist']} - {track_info['track']}", flush=True)
    """Send the track information to Koito using the ListenBrainz API."""
    url = f"{config['KOITO_ADDRESS']}/apis/listenbrainz/1/submit-listens"
    headers = {
        'Authorization': f"Token {config['KOITO_API_KEY']}",
        'Content-Type': 'application/json'
    }
    data = {
        'listen_type': 'single',
        'payload': [{
            'listened_at': int(track_info['played_at'] / 1000),  # Convert to seconds
            'track_metadata': {
                'artist_name': track_info['artist'],
                'track_name': track_info['track'],
                'release_name': track_info['album'],
                'additional_info': {
                    'duration_ms': track_info['duration']
                }
            }
        }]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.json()

def startup_message():
    """Print startup message and check for current track."""
    print("Koito-Scrobbler Service has started successfully.", flush=True)
    koito_address = config['KOITO_ADDRESS']
    print(f"Koito Address: {koito_address}", flush=True)
    
    # Check if a track is playing
    track_info = get_current_track()
    if not track_info:
        print("No track playing - go listen to some music.", flush=True)

def main():
    global last_scrobbled_track
    startup_message()
    while True:
        try:
            track_info = get_current_track()
            if track_info:
                current_track = f"{track_info['artist']} - {track_info['track']}"
                if current_track != last_scrobbled_track:
                    scrobble_track(track_info)
                    last_scrobbled_track = current_track
        except Exception as e:
            # Log the error
            print(f"Error: {e}", flush=True)
        time.sleep(30)

if __name__ == "__main__":
    main()