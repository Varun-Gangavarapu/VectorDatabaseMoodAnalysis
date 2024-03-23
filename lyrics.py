import requests
from transformers import pipeline
import json

# example call: base_url + lyrics_matcher + format_url + artist_search_parameter + artist_variable + track_search_parameter + track_variable + api_key
# example json print: print(json.dumps(api_call, sort_keys=True, indent=2))
base_url = "https://api.musixmatch.com/ws/1.1/"
apikey = "&apikey=82af858c39c7035647e9a896acf1a389"
# isrc = input("Enter the ISRC: ")
classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)


def getSentiment(isrc):
    api_call = base_url + 'matcher.lyrics.get?track_isrc=' + isrc + apikey
    request = requests.get(api_call)
    print(request)
    data = request.json()
    data = data['message']['body']
    print("API Call: " + api_call)
    print()
    print()
    result = data['lyrics']['lyrics_body']
    result = result[:511]
    emotions = classifier(result)[0]
    print('\n'.join('{}: {}'.format(*k) for k in enumerate(emotions)))


