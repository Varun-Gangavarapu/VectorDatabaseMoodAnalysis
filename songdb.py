import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify client credentials
CLIENT_ID = '3a8e09e2d4344d69b2d18676ab1e2b87'
CLIENT_SECRET = '02f562a80d1b4add8de4da6b6909ac13'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# The ID of the playlist you're interested in
playlist_id = '0JiVp7Z0pYKI8diUV6HJyQ'

num = 0

def get_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

tracks = get_playlist_tracks(playlist_id)
for track in tracks:
    num=num+1
    track_name = track['track']['name']
    isrc = track['track']['external_ids']['isrc'] if 'isrc' in track['track']['external_ids'] else 'N/A'
    print(f"Track: {track_name}, ISRC: {isrc}")
    print(f"Total tracks: {num}")

