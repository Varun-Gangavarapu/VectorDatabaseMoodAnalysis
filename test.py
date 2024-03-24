from vec_db import Vec_DB
from preprocess import compute_user_vector_sentiments
import numpy as np

if __name__ == '__main__':
    vec_db = Vec_DB('7f339788-9a19-440f-a013-bd2cc0cb73f1')
    print(
        vec_db.get_knn(
            compute_user_vector_sentiments('dataRecentlyPlayed.json'),
            k=5
        ))
