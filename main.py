from flask import Flask, redirect, request, render_template, url_for
import requests
import base64
import lyricsRecentlyPlayed
import audioFeaturesdb, test

app = Flask(__name__)

# Spotify API credentials
CLIENT_ID = '3a8e09e2d4344d69b2d18676ab1e2b87'
CLIENT_SECRET = '02f562a80d1b4add8de4da6b6909ac13'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SCOPE = 'user-read-recently-played'



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
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
            # print(recently_played_songs)
        except (ValueError, requests.exceptions.JSONDecodeError) as e:
            return f'Error: {e}'


        if recently_played_songs:
            #audioFeaturesdb.getFeaturesRecent(recently_played_songs)
            lyricsRecentlyPlayed.makeJSON(recently_played_songs)
            test.sentimentRecent()




            for song in recently_played_songs:
                track_name = song['track']['name']
                isrc = song['track']['external_ids']['isrc']

                # print(f"{track_name} - ISRC: {isrc}")
            return redirect(url_for('redirection'))
        else:
            return "No recently played songs found."

    return 'Authentication failed'

def extract_songs(query_response):
    try:
        # Assuming query_response['matches'] contains the relevant song data
        matches = query_response.get('matches', [])

        # Extract song information
        song_list = [{'title': match['metadata']['track'], 'artist': match['metadata']['artist']} for match in
                     matches]

        return song_list
    except KeyError as e:
        print(f"Error in extracting song data: {e}")
        return []

# Example usage

@app.route('/redirection')
def redirection():
    arr = test.sentimentRecent()
    print(arr)
    arrs = extract_songs(arr[0])

    return render_template('page2.html', songs_array=arrs, emotion_array=arr[1])

if __name__ == '__main__':
    app.run(debug=True)