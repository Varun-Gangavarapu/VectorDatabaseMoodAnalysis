from pinecone import Pinecone

class Vec_DB:
    # Default api key is for Lyrics
    def __init__(self, api_key):
        # api key for audio similarity vector db
        pc = Pinecone(api_key=api_key)
        self.index = pc.Index("songs")

    def add_vectors(self, vectors):
        self.index.upsert(vectors=vectors)

    def get_knn(self, target, k):
        return self.index.query(
            vector=target,
            top_k=k,
            include_values=False,
            include_metadata=True
        )


if __name__ == "__main__":
    vec_db = Vec_DB()

    # vectors = []
    # for i in range(5):
    #     vectors.append(
    #         {"id": "vec"+str(i), "values": np.random.rand(21), "metadata": {"name": "happy"}})
    # vec_db.add_vectors(vectors)

    # print(np.random.rand(21))
    # print(vec_db.get_knn(np.random.rand(21).tolist(), 3))
