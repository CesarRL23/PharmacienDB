#!/usr/bin/env python3
# scripts/generate_embeddings.py (opcional)
# Genera embeddings para documents usando sentence-transformers (all-MiniLM-L6-v2)
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI","mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME","rag_pharmacien")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
model = SentenceTransformer("all-MiniLM-L6-v2")

batch_size = 32
docs = list(db.documents.find({"embeddings": None}))
for i in range(0, len(docs), batch_size):
    batch = docs[i:i+batch_size]
    texts = [d["content"] for d in batch]
    vecs = model.encode(texts).tolist()
    for d, v in zip(batch, vecs):
        db.documents.update_one({"_id": d["_id"]}, {"$set": {"embeddings": v, "embedding_model": "all-MiniLM-L6-v2"}})

print("Embeddings generated and saved to documents.embeddings")
