#!/usr/bin/env python3
# scripts/create_indexes_and_validators.py
from pymongo import MongoClient, ASCENDING, TEXT
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "rag_pharmacien")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


# Farmacias validator
farmacias_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["ciudad", "direccion", "telefono"],
        "properties": {
            "ciudad": {"bsonType": "string"},
            "direccion": {"bsonType": "string"},
            "telefono": {"bsonType": "string"},
            "empleados": {"bsonType": "array"},
            "medicamentos": {"bsonType": "array"}
        }
    }
}

# Medicamentos validator
medicamentos_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nombre", "precio", "categoria"],
        "properties": {
            "nombre": {"bsonType": "string"},
            "precio": {"bsonType": "double"},
            "categoria": {"bsonType": "object"},
            "proveedores": {"bsonType": "array"}
        }
    }
}

# Clientes validator
clientes_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nombre", "direccion", "telefono"],
        "properties": {
            "nombre": {"bsonType": "string"},
            "direccion": {"bsonType": "string"},
            "telefono": {"bsonType": "string"}
        }
    }
}

# Proveedores validator
proveedores_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nombre", "telefono", "direccion", "ciudad"],
        "properties": {
            "nombre": {"bsonType": "string"},
            "telefono": {"bsonType": "string"},
            "direccion": {"bsonType": "string"},
            "ciudad": {"bsonType": "string"}
        }
    }
}

# Doctores validator
doctores_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nombre", "apellido", "especialidad", "telefono"],
        "properties": {
            "nombre": {"bsonType": "string"},
            "apellido": {"bsonType": "string"},
            "especialidad": {"bsonType": "string"},
            "telefono": {"bsonType": "string"}
        }
    }
}

# Citas validator
citas_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["fecha", "cliente", "doctor"],
        "properties": {
            "fecha": {"bsonType": "date"},
            "cliente": {"bsonType": "object"},
            "doctor": {"bsonType": "object"},
            "receta": {"bsonType": "array"}
        }
    }
}

# Transacciones validator
transacciones_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["fecha", "totalpagado", "metodopago"],
        "properties": {
            "fecha": {"bsonType": "date"},
            "totalpagado": {"bsonType": "double"},
            "metodopago": {"bsonType": "string"},
            "empleado": {"bsonType": "array"},
            "citaref": {"bsonType": ["string", "null"]}
        }
    }
}

# Create collections with validators
collections_config = {
    "farmacias": farmacias_validator,
    "medicamentos": medicamentos_validator,
    "clientes": clientes_validator,
    "proveedores": proveedores_validator,
    "doctores": doctores_validator,
    "citas": citas_validator,
    "transacciones": transacciones_validator
}

for col_name, validator in collections_config.items():
    try:
        db.create_collection(col_name, validator=validator)
        print(f"Created collection: {col_name}")
    except Exception as e:
        print(f"{col_name} collection exists or validator already set: {e}")

print("\nCreating indexes...")

# Farmacias indexes
db.farmacias.create_index([("ciudad", ASCENDING)])
db.farmacias.create_index([("ciudad", TEXT), ("direccion", TEXT)])

# Medicamentos indexes
db.medicamentos.create_index([("nombre", TEXT)])
db.medicamentos.create_index([("categoria.nombre", ASCENDING)])
db.medicamentos.create_index([("precio", ASCENDING)])

# Clientes indexes
db.clientes.create_index([("nombre", TEXT)])
db.clientes.create_index([("telefono", ASCENDING)])

# Proveedores indexes
db.proveedores.create_index([("nombre", TEXT)])
db.proveedores.create_index([("ciudad", ASCENDING)])

# Doctores indexes
db.doctores.create_index([("especialidad", ASCENDING)])
db.doctores.create_index([("nombre", TEXT), ("apellido", TEXT)])

# Citas indexes
db.citas.create_index([("fecha", ASCENDING)])
db.citas.create_index([("cliente._id", ASCENDING)])
db.citas.create_index([("doctor._id", ASCENDING)])

# Transacciones indexes
db.transacciones.create_index([("fecha", ASCENDING)])
db.transacciones.create_index([("citaref", ASCENDING)])
db.transacciones.create_index([("metodopago", ASCENDING)])

print("All indexes created successfully!")
