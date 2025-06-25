import time
import requests
import spotipy
import datetime
from spotipy.oauth2 import SpotifyOAuth
from config_secrets import KOITO_ADDRESS, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, KOITO_API_KEY

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-read-currently-playing",
    cache_path=".cache_service"
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
        print(f"Spotify API error: {e}. Response: {e.response.text if e.response else 'No response'}")
    return None

last_scrobbled_track = None

def scrobble_track(track_info):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Scrobbling: {track_info['artist']} - {track_info['track']}")
    """Send the track information to Koito using the ListenBrainz API."""
    url = f"{KOITO_ADDRESS}/apis/listenbrainz/1/submit-listens"
    headers = {
        'Authorization': f'Token {KOITO_API_KEY}',
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

def main():
    global last_scrobbled_track
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
            print(f"Error: {e}")
        time.sleep(30)

if __name__ == "__main__":
    main()