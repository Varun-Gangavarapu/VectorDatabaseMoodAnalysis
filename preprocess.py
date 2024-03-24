import numpy as np
from vec_db import Vec_DB
import json


def batchify(array, batch_size=100):
    batches = []
    for i in range(0, len(array), batch_size):
        batches.append(array[i:i+batch_size])
    return batches


def get_sentiment_values(dat, preprocess=True):
    if preprocess:
        # Filter out the entry with label 'neutral'
        filtered_data = [item for item in dat if item['label'] != 'neutral']

        # Sort the filtered data alphabetically by the 'label' field
        sorted_data = sorted(filtered_data, key=lambda x: x['label'])
    else:
        sorted_data = dat

    # Extract just the values (scores)
    values = [item['score'] for item in sorted_data]
    N = len(values)

    # Takes an input of 6 emotions and turns it into 21
    for i in range(N):
        for j in range(i + 1, N):
            values.append(0.5 * (values[i] + values[j]))

    # Calculate the magnitude of the vector
    magnitude = np.linalg.norm(values)

    # Check if the magnitude is not zero to avoid division by zero
    if magnitude != 0:
        # Normalize the vector by dividing each element by the magnitude
        normalized_vector = values / magnitude
    else:
        # If the magnitude is zero, return the original vector (to avoid division by zero)
        normalized_vector = values

    return normalized_vector


def get_audio_feature_values(dat):
    audio_features = []
    for key, value in dat.items():
        audio_features.append(float(value))
    return audio_features


def compute_user_vector_sentiments(file_path):
    # Open the JSON file and read its content
    with open(file_path, 'r') as file:
        # Parse the JSON content into a Python object
        json_data = json.load(file)

    songs = json_data['songs']
    batches = batchify(songs)

    score_map = {'anger': 0.0, 'disgust': 0.0, 'fear': 0.0,
                 'joy': 0.0, 'sadness': 0.0, 'surprise': 0.0}

    for batch in batches:
        for song in batch:
            for item in song['sentiment']:
                if item['label'] == 'neutral':
                    continue
                score_map[item['label']] += item['score']

    aggregate_sentiment = [{'label': 'anger', 'score': score_map['anger']},
                           {'label': 'disgust', 'score': score_map['disgust']},
                           {'label': 'fear', 'score': score_map['fear']},
                           {'label': 'joy', 'score': score_map['joy']},
                           {'label': 'sadness', 'score': score_map['sadness']},
                           {'label': 'surprise', 'score': score_map['surprise']}]

    return get_sentiment_values(aggregate_sentiment, preprocess=False).tolist()


def compute_user_vector_audio(file_path):
    # Open the JSON file and read its content
    with open(file_path, 'r') as file:
        # Parse the JSON content into a Python object
        json_data = json.load(file)

    songs = json_data['songs']
    batches = batchify(songs)

    score_map = {"acousticness": 0.0,
                 "danceability": 0.0,
                 "energy": 0.0,
                 "instrumentalness": 0.0,
                 "liveness": 0.0,
                 "loudness": 0.0,
                 "speechiness": 0.0,
                 "tempo": 0.0,
                 "valence": 0.0}


sentiments = [
    "Anger",
    "Disgust",
    "Fear",
    "Joy",
    "Sadness",
    "Surprise",
    "Hatred",
    "Terror",
    "Rage",
    "Bitterness",
    "Fury",
    "Horrified",
    "Confusion",
    "Despise",
    "Revulsion",
    "Diabolical",
    "Sorrow",
    "Shock",
    "Ambivalence",
    "Elation",
    "Grief"
]

audio_features = [
    "acousticness",
    "danceability",
    "energy",
    "instrumentalness",
    "liveness",
    "loudness",
    "speechiness",
    "tempo",
    "valence"
]


def print_results(input):
    map = {}
    for i in range(len(input)):
        map[sentiments[i]] = input[i]

    # Sort the dictionary by values
    sorted_mapping = sorted(map.items(), key=lambda x: -x[1])

    # Print the labels and values sorted by values
    for label, value in sorted_mapping:
        print(f"{label}: {value}")


def view_sorted(input_string):
    # Split the string by commas and convert each substring into a float
    values = [float(x.strip()) for x in input_string.split(',')]

    # Divide each value by the sum of all values, multiply by 100, and store the result
    scaled_values = [(val / sum(values)) * 100 for val in values]

    # Zip the values and scaled values, sort by scaled values, and print the sorted results
    sorted_results = sorted(zip(values, scaled_values), key=lambda x: -x[1])
    for val, scaled_val in sorted_results:
        print(f"{val:.2f} ({scaled_val:.2f}%)")
def get_top_k_sentiments(values, k):
    map = {}
    for i in range(len(values)):
        map[sentiments[i]] = values[i]

    # Sort the dictionary by values
    sorted_mapping = sorted(map.items(), key=lambda x: -x[1])

    # Print the labels and values sorted by values
    i = 0
    top_k_sentiments = []
    for label, value in sorted_mapping:
        top_k_sentiments.append(label)
        i += 1
        if i == k:
            break
    return top_k_sentiments


def get_string(arr):
    s = ""
    for item in arr:
        s += str(item) + ","
    return s


if __name__ == "__main__":
    # print(sum_batch(data))

    # print_results(
    #     get_values(sum_batch(data))
    # )

    vec_db = Vec_DB('7f339788-9a19-440f-a013-bd2cc0cb73f1')
    # print(vec_db.get_knn(
    #     target=compute_user_vector_sentiments('dataRecentlyPlayed.json'), k=5
    # ))
    vec_db.index.query(
        vector=compute_user_vector_sentiments('dataRecentlyPlayed.json'),
        top_k=5,
    )

    # view_sorted('0.121713251, 0.102738664, 0.0947829857, 0.0133372182, 0.588854134, 0.044840876, 0.112225957, 0.108248115, 0.0675252303, 0.355283707, 0.0832770616, 0.0987608209, 0.0580379404, 0.345796406, 0.0737897679, 0.0540601, 0.341818571, 0.0698119327, 0.301095694, 0.0290890466, 0.316847533')
