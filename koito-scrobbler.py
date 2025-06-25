import datetime
import os
from dateutil import parser
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from config_secrets import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, KOITO_API_KEY, KOITO_ADDRESS

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-read-currently-playing user-read-recently-played",
                                               cache_path=".cache"))

def get_recently_played_tracks():
    """Fetch the recently played tracks from Spotify."""
    try:
        recently_played = sp.current_user_recently_played(limit=50)
        tracks_info = []
        for item in recently_played['items']:
            track = item['track']
            track_info = {
                'artist': track['artists'][0]['name'],
                'track': track['name'],
                'album': track['album']['name'],
                'duration': track['duration_ms'],
                'played_at': item['played_at']
            }
            tracks_info.append(track_info)
        return tracks_info
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}. Response: {e.response.text if e.response else 'No response'}")
    return []

def scrobble_to_koito(track_info):
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
            'listened_at': int(parser.isoparse(track_info['played_at']).timestamp()),  # Convert to seconds
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
    tracks_info = get_recently_played_tracks()
    if tracks_info:
        for track_info in tracks_info:
            status_code, response = scrobble_to_koito(track_info)
            if status_code == 200:
                print("Scrobble successful:", response)
            else:
                print(f"Scrobble failed with status code {status_code}: {response}")
    else:
        print("No recently played tracks available to scrobble.")

if __name__ == "__main__":
    main()