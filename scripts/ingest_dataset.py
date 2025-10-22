#!/usr/bin/env python3
# scripts/ingest_dataset.py
# Carga pharmacien_rag_dataset.json en MongoDB (colecciones: documents, images, plus optional others)
import json, os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI","mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME","rag_pharmacien")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

with open("data/pharmacien_rag_dataset.json","r",encoding="utf-8") as f:
    ds = json.load(f)

if "images" in ds:
    db.images.delete_many({})
    db.images.insert_many(ds["images"])
if "text_documents" in ds:
    db.documents.delete_many({})
    db.documents.insert_many(ds["text_documents"])

print("Ingest complete. Counts: images=", db.images.count_documents({}), " documents=", db.documents.count_documents({}))
