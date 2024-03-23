import requests


CLIENT_ID = '3a8e09e2d4344d69b2d18676ab1e2b87'
CLIENT_SECRET='02f562a80d1b4add8de4da6b6909ac13'

def get_access_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_response_data = auth_response.json()
    return auth_response_data.get('access_token', None)
