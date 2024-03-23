from pinecone import Pinecone


class Vec_DB:
    def __init__(self):
        api_key = '7f339788-9a19-440f-a013-bd2cc0cb73f1'
        pc = Pinecone(api_key=api_key)
        self.index = pc.Index("songs")

    def add_vectors(self, vectors):
        self.index.upsert(vectors=vectors)

    def get_knn(self, target, k):
        return self.index.query(
            vector=target,
            top_k=k,
            include_values=True
        )


if __name__ == "__main__":
    import numpy as np
    vec_db = Vec_DB()

    # vectors = []
    # for i in range(5):
    #     vectors.append({"id": "vec"+str(i), "values": np.random.rand(21)})
    # vec_db.add_vectors(vectors)

    # print(np.random.rand(21))
    print(vec_db.get_knn(np.random.rand(21).tolist(), 3))
