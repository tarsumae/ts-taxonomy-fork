import os
import pandas as pd
import numpy as np
import openai
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class TSClassifier:
    def __init__(self, taxonomy_csv="ts_taxonomy.csv", embedding_model="text-embedding-ada-002"):
        df = pd.read_csv(taxonomy_csv)
        df = df[df["is_active"] == True]
        self.codes = df["ts_code"].tolist()
        self.paths = df["ts_path_kr"].tolist()
        self.embedding_model = embedding_model
        self.path_embeddings = self._get_embeddings(self.paths)

    def _get_embeddings(self, texts, batch_size=16):
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            resp = openai.Embedding.create(input=batch, model=self.embedding_model)
            embeddings.extend([item["embedding"] for item in resp["data"]])
        return np.array(embeddings)

    def classify(self, keywords):
        query = " ".join(keywords)
        resp = openai.Embedding.create(input=[query], model=self.embedding_model)
        query_emb = np.array(resp["data"][0]["embedding"])
        sims = self._cosine_similarity(query_emb, self.path_embeddings)
        top_idx = sims.argsort()[-3:][::-1]
        return [(self.codes[i], float(sims[i])) for i in top_idx]

    def _cosine_similarity(self, vec, mat):
        dot = mat.dot(vec)
        norm_mat = np.linalg.norm(mat, axis=1)
        norm_vec = np.linalg.norm(vec)
        return dot / (norm_mat * norm_vec + 1e-10)
