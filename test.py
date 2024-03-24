
from vec_db import Vec_DB
from preprocess import compute_user_vector_sentiments, compute_user_vector_audio


def test_sentiments():
    vec_db = Vec_DB('7f339788-9a19-440f-a013-bd2cc0cb73f1')
    print(
        vec_db.get_knn(
            compute_user_vector_sentiments('dataRecentlyPlayed.json'),
            k=5
        ))


def test_audio():
    vec_db = Vec_DB('828881e7-4432-4893-9a7a-dc8aadb53df9')
    print(
        vec_db.get_knn(
            compute_user_vector_audio('audiofeaturesrecent.json'),
            k=5
        ))


if __name__ == '__main__':
    test_sentiments()
    test_audio()
