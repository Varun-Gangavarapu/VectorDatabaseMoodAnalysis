from flask import Flask, redirect, request
import requests
import base64
import lyricsRecentlyPlayed
import audioFeaturesdb, test

app = Flask(__name__)

# Spotify API credentials
CLIENT_ID = '3a8e09e2d4344d69b2d18676ab1e2b87'
CLIENT_SECRET = '02f562a80d1b4add8de4da6b6909ac13'
REDIRECT_URI = 'http://localhost:5000/callback'
SCOPE = 'user-read-recently-played'



# @app.route('/')
# def home():
#     return 'Welcome to the Spotify API!'

@app.route('/')
def login():
    auth_url = 'https://accounts.spotify.com/authorize'
    payload = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE
    }
    res = requests.get(auth_url, params=payload)
    return redirect(res.url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        # Step 3: Request access token
        token_url = 'https://accounts.spotify.com/api/token'
        auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode())
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        }
        headers = {
            'Authorization': f'Basic {auth_header.decode()}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        res = requests.post(token_url, data=payload, headers=headers)

        if res.status_code not in range(200, 299):
            return f'Error: {res.status_code} - {res.text}'

        try:
            access_token = res.json().get('access_token')
        except (ValueError, requests.exceptions.JSONDecodeError) as e:
            return f'Error: {e}'

        recently_played_url = 'https://api.spotify.com/v1/me/player/recently-played'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        res = requests.get(recently_played_url, headers=headers)

        if res.status_code not in range(200, 299):
            return f'Error: {res.status_code} - {res.text}'

        try:
            recently_played_songs = res.json().get('items')
            print(recently_played_songs)
        except (ValueError, requests.exceptions.JSONDecodeError) as e:
            return f'Error: {e}'


        if recently_played_songs:
            #audioFeaturesdb.getFeaturesRecent(recently_played_songs)
            lyricsRecentlyPlayed.makeJSON(recently_played_songs)
            test.sentimentRecent()




            for song in recently_played_songs:
                track_name = song['track']['name']
                isrc = song['track']['external_ids']['isrc']

                print(f"{track_name} - ISRC: {isrc}")
            return "Check the terminal"
        else:
            return "No recently played songs found."

    return 'Authentication failed'

if __name__ == '__main__':
    app.run(debug=True)