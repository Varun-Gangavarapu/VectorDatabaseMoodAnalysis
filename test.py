from vec_db import Vec_DB
from preprocess import compute_user_vector_sentiments,get_top_k_sentiments
import numpy as np





def sentimentRecent():

    vec_db = Vec_DB('7f339788-9a19-440f-a013-bd2cc0cb73f1')
    user_sentiment = compute_user_vector_sentiments('dataRecentlyPlayed.json')
    user_songs = vec_db.get_knn(target=user_sentiment, k=5)




    print(get_top_k_sentiments(user_sentiment,5))
    print(user_songs)






