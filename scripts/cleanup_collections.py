#!/usr/bin/env python3
# scripts/cleanup_collections.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
client = MongoClient(os.getenv("MONGO_URI","mongodb://localhost:27017"))
db = client[os.getenv("DB_NAME","rag_pharmacien")]
cols = ["documents","images","medicamentos","transactions","employees"]
for c in cols:
    res = db[c].delete_many({})
    print(f"Cleared {c}: {res.deleted_count} docs")
