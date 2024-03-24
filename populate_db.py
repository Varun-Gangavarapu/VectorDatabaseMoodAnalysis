import json
from vec_db import Vec_DB
from preprocess import get_sentiment_values, get_audio_feature_values


def batchify(array, batch_size=100):
    batches = []
    for i in range(0, len(array), batch_size):
        batches.append(array[i:i+batch_size])
    return batches


def populate_sentiments_db(file_path):
    # Create a Vec_DB to connect to Pinecone
    vec_db = Vec_DB()

    # Open the JSON file and read its content
    with open(file_path, 'r') as file:
        # Parse the JSON content into a Python object
        json_data = json.load(file)

    songs = json_data['songs']
    batches = batchify(songs)

    for batch in batches:
        vectors = []
        for song in batch:
            values = get_sentiment_values(song['sentiment'])
            vectors.append(
                {"id": song['id'], "values": values, "metadata": song['metadata']})
        vec_db.add_vectors(vectors)


def populate_features_db(file_path):
    # Create a Vec_DB to connect to Pinecone
    vec_db = Vec_DB()

    # Open the JSON file and read its content
    with open(file_path, 'r') as file:
        # Parse the JSON content into a Python object
        json_data = json.load(file)

    songs = json_data['songs']
    batches = batchify(songs)

    for batch in batches:
        vectors = []
        for song in batch:
            values = get_audio_feature_values(song['features'])
            vectors.append(
                {"id": song['isrc'], "values": values, "metadata": {
                    "name": song['track_name'], "artist": song['artist']
                }})
        vec_db.add_vectors(vectors)


if __name__ == "__main__":
    populate_features_db('audiofeaturesdata.json')
