# api/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import os, numpy as np
from dotenv import load_dotenv
from fastapi import HTTPException, Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
import datetime
from bson import ObjectId


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
    

# Helper para convertir ObjectId a str en responses
def safe_doc(doc):
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

class DocumentIn(BaseModel):
    title: str
    content: str
    doc_type: Optional[str] = "product_description"
    language: Optional[str] = "es"
    related_medicamento: Optional[str] = None
    tags: Optional[List[str]] = []
    images: Optional[List[str]] = []
    metadata: Optional[dict] = {}

class DocumentOut(DocumentIn):
    _id: str

# GET all documents (paginated simple)
@app.get("/documents", response_model=List[DocumentOut])
def get_documents(limit: int = 50, skip: int = 0):
    cursor = db.documents.find().skip(int(skip)).limit(int(limit))
    docs = [safe_doc(d) for d in cursor]
    return docs

# GET document by id
@app.get("/documents/{doc_id}", response_model=DocumentOut)
def get_document_by_id(doc_id: str = Path(..., description="Document ObjectId as string")):
    from bson import ObjectId
    try:
        oid = ObjectId(doc_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid document id")
    doc = db.documents.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return safe_doc(doc)

# GET all images
@app.get("/images")
def get_images(limit: int = 50, skip: int = 0):
    cursor = db.images.find().skip(int(skip)).limit(int(limit))
    imgs = [safe_doc(i) for i in cursor]
    return imgs

# POST create document
@app.post("/documents", response_model=DocumentOut, status_code=201)
def create_document(payload: DocumentIn):
    data = payload.dict()
    data["_id"] = ObjectId()  # generate ObjectId
    data["ingest_ts"] = datetime.datetime.utcnow().isoformat()
    # Insert to DB
    db.documents.insert_one(data)
    data["_id"] = str(data["_id"])
    return data

