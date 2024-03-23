import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

CLIENT_ID = '3a8e09e2d4344d69b2d18676ab1e2b87'
CLIENT_SECRET = '02f562a80d1b4add8de4da6b6909ac13'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_id = '0JiVp7Z0pYKI8diUV6HJyQ'

results = sp.playlist_items(playlist_id)
tracks = results['items']
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

data = []
for item in tracks:
    track = item['track']
    track_id = track['id']
    track_name = track['name']
    isrc = track['external_ids'].get('isrc')
    artist = track['artists'][0]['name']  # Assuming first artist for simplicity

    features = sp.audio_features([track_id])[0]  # Fetching audio features

    data.append({
        "track_name": track_name,
        "isrc": isrc,
        "artist": artist,
        "features": {
            "acousticness": features['acousticness'],
            "danceability": features['danceability'],
            "energy": features['energy'],
            "instrumentalness": features['instrumentalness'],
            "liveness": features['liveness'],
            "loudness": features['loudness'],
            "speechiness": features['speechiness'],
            "tempo": features['tempo'],
            "valence": features['valence']
        }
    })

with open('audiofeaturesdata.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)



