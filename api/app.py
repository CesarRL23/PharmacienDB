# api/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import os, numpy as np
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI","mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME","rag_pharmacien")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
model = SentenceTransformer("all-MiniLM-L6-v2")

app = FastAPI()

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/search")
def search(req: SearchRequest):
    q_emb = model.encode(req.query).tolist()
    try:
        pipeline = [
            { "$search": { "knnBeta": { "vector": q_emb, "path": "embeddings", "k": req.top_k } } },
            { "$project": { "title": 1, "content": 1, "related_medicamento": 1, "score": { "$meta": "searchScore" } } }
        ]
        results = list(db.documents.aggregate(pipeline))
        return {"source": "atlas_knn", "results": results}
    except Exception:
        # fallback brute force cosine
        docs = list(db.documents.find({"embeddings": {"$ne": None}}))
        def cos(a,b):
            a = np.array(a); b = np.array(b)
            return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-9))
        scored = [(d, cos(q_emb, d["embeddings"])) for d in docs]
        scored.sort(key=lambda x: x[1], reverse=True)
        top = [ {"_id": s[0]["_id"], "title": s[0]["title"], "score": s[1]} for s in scored[:req.top_k] ]
        return {"source":"brute_force","results": top}
