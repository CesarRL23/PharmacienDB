#!/usr/bin/env python3
# scripts/ingest_dataset.py
# Carga pharmacien_rag_dataset.json en MongoDB
import json
import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "rag_pharmacien")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

with open("data/pharmacien_rag_dataset.json", "r", encoding="utf-8") as f:
    ds = json.load(f)

# Convert date strings back to datetime objects for citas and transacciones
for cita in ds.get("citas", []):
    if isinstance(cita["fecha"], str):
        cita["fecha"] = datetime.fromisoformat(cita["fecha"])

for trans in ds.get("transacciones", []):
    if isinstance(trans["fecha"], str):
        trans["fecha"] = datetime.fromisoformat(trans["fecha"])

# Insert data into collections
collections_data = {
    "proveedores": ds.get("proveedores", []),
    "medicamentos": ds.get("medicamentos", []),
    "farmacias": ds.get("farmacias", []),
    "clientes": ds.get("clientes", []),
    "doctores": ds.get("doctores", []),
    "citas": ds.get("citas", []),
    "transacciones": ds.get("transacciones", [])
}

print("Inserting data into MongoDB...")
for col_name, data in collections_data.items():
    if data:
        db[col_name].delete_many({})  # Clear existing data
        db[col_name].insert_many(data)
        print(f"  ✓ {col_name}: {len(data)} documentos insertados")

print("\n¡Ingesta completa!")
print(f"Total de documentos insertados: {sum(len(data) for data in collections_data.values())}")
