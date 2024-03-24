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