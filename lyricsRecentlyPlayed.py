import requests, json
from transformers import pipeline
from songdb import tracks
import json

# example call: base_url + lyrics_matcher + format_url + artist_search_parameter + artist_variable + track_search_parameter + track_variable + api_key
# example json print: print(json.dumps(api_call, sort_keys=True, indent=2))
base_url = "https://api.musixmatch.com/ws/1.1/"
apikey = "&apikey=b99e94132c7cf2395c5f59e187cdd976"
# isrc = input("Enter the ISRC: ")
classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)


def getSentiment(isrc):
    api_call = base_url + 'matcher.lyrics.get?track_isrc=' + isrc + apikey
    request = requests.get(api_call)

    data = request.json()
    data = data['message']['body']

    try:
        result = data['lyrics']['lyrics_body']
    except TypeError:
        print("invlaid isrc")
        return

    result = result[:511]
    emotions = classifier(result)[0]
    return emotions

def makeJSON(tracks):
    songs = []
    for track in tracks:
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        isrc = track['track']['external_ids']['isrc'] if 'isrc' in track['track']['external_ids'] else 'N/A'

        metadata = {"track": track_name, "artist": artist_name}
        song_info = {"id": isrc, "metadata": metadata, "sentiment": getSentiment(isrc)}

        if(getSentiment(isrc) != None):
            songs.append(song_info)


    data = {"songs": songs}
    with open('dataRecentlyPlayed.json', 'w') as outfile:
            json.dump(data, outfile)

















