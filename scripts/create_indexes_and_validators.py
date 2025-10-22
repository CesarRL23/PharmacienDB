#!/usr/bin/env python3
# scripts/create_indexes_and_validators.py
from pymongo import MongoClient, TEXT, ASCENDING
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI","mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME","rag_pharmacien")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Validator
validator = {
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["title","content","language","ingest_ts"],
    "properties": {
      "title": {"bsonType":"string"},
      "content": {"bsonType":"string"},
      "language": {"enum":["es","en"]},
      "images": {"bsonType":["array","null"]},
      "embeddings": {"bsonType":["array","null"], "items": {"bsonType":"double"}}
    }
  }
}

try:
    db.create_collection("documents", validator=validator)
except Exception as e:
    print("documents collection exists or validator may already be set:", e)

# Indexes
db.documents.create_index([("title", TEXT), ("content", TEXT)], name="textIdx_docs")
db.documents.create_index([("related_medicamento", ASCENDING)])
db.images.create_index([("related_med_id", ASCENDING)])
print("Indexes created.")
