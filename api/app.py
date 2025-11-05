# api/app.py
from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "rag_pharmacien")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

app = FastAPI(title="Pharmacien API", version="2.0")

# Helper para convertir ObjectId a str
def safe_doc(doc):
    if not doc:
        return None
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


# Proveedores
class ProveedorIn(BaseModel):
    nombre: str
    telefono: str
    direccion: str
    ciudad: str

class ProveedorOut(ProveedorIn):
    _id: str

# Medicamentos
class CategoriaEmbed(BaseModel):
    nombre: str
    descripcion: str

class MedicamentoIn(BaseModel):
    nombre: str
    precio: float
    categoria: CategoriaEmbed
    proveedores: List[str] = []

class MedicamentoOut(MedicamentoIn):
    _id: str

# Clientes
class ClienteIn(BaseModel):
    nombre: str
    direccion: str
    telefono: str

class ClienteOut(ClienteIn):
    _id: str

# Doctores
class DoctorIn(BaseModel):
    nombre: str
    apellido: str
    especialidad: str
    telefono: str

class DoctorOut(DoctorIn):
    _id: str

# Farmacias
class EmpleadoEmbed(BaseModel):
    _id: str
    nombre: str
    puesto: str
    telefono: str

class FarmaciaIn(BaseModel):
    ciudad: str
    direccion: str
    telefono: str
    empleados: List[EmpleadoEmbed] = []
    medicamentos: List[str] = []

class FarmaciaOut(FarmaciaIn):
    _id: str

# Citas
class ClienteRef(BaseModel):
    _id: str
    nombre: str
    telefono: str

class DoctorRef(BaseModel):
    _id: str
    nombre: str
    especialidad: str

class RecetaEmbed(BaseModel):
    medicamento_id: str
    medicamento_nombre: str
    dosis: str
    duracion: str

class CitaIn(BaseModel):
    fecha: datetime
    cliente: ClienteRef
    doctor: DoctorRef
    receta: List[RecetaEmbed] = []

class CitaOut(CitaIn):
    _id: str

# Transacciones
class TransaccionIn(BaseModel):
    fecha: datetime
    totalpagado: float
    metodopago: str
    empleado: List[EmpleadoEmbed]
    citaref: Optional[str] = None

class TransaccionOut(TransaccionIn):
    _id: str


# ============ PROVEEDORES ============
@app.get("/proveedores", response_model=List[ProveedorOut])
def get_proveedores(limit: int = Query(50, le=100), skip: int = 0):
    cursor = db.proveedores.find().skip(skip).limit(limit)
    return [safe_doc(d) for d in cursor]

@app.get("/proveedores/{id}", response_model=ProveedorOut)
def get_proveedor(id: str):
    doc = db.proveedores.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return safe_doc(doc)

@app.post("/proveedores", response_model=ProveedorOut, status_code=201)
def create_proveedor(payload: ProveedorIn):
    import uuid
    data = payload.dict()
    data["_id"] = str(uuid.uuid4())
    db.proveedores.insert_one(data)
    return data

# ============ MEDICAMENTOS ============
@app.get("/medicamentos", response_model=List[MedicamentoOut])
def get_medicamentos(limit: int = Query(50, le=100), skip: int = 0):
    cursor = db.medicamentos.find().skip(skip).limit(limit)
    return [safe_doc(d) for d in cursor]

@app.get("/medicamentos/{id}", response_model=MedicamentoOut)
def get_medicamento(id: str):
    doc = db.medicamentos.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")
    return safe_doc(doc)

@app.post("/medicamentos", response_model=MedicamentoOut, status_code=201)
def create_medicamento(payload: MedicamentoIn):
    import uuid
    data = payload.dict()
    data["_id"] = str(uuid.uuid4())
    db.medicamentos.insert_one(data)
    return data

# ============ CLIENTES ============
@app.get("/clientes", response_model=List[ClienteOut])
def get_clientes(limit: int = Query(50, le=100), skip: int = 0):
    cursor = db.clientes.find().skip(skip).limit(limit)
    return [safe_doc(d) for d in cursor]

@app.get("/clientes/{id}", response_model=ClienteOut)
def get_cliente(id: str):
    doc = db.clientes.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return safe_doc(doc)

@app.post("/clientes", response_model=ClienteOut, status_code=201)
def create_cliente(payload: ClienteIn):
    import uuid
    data = payload.dict()
    data["_id"] = str(uuid.uuid4())
    db.clientes.insert_one(data)
    return data

# ============ DOCTORES ============
@app.get("/doctores", response_model=List[DoctorOut])
def get_doctores(limit: int = Query(50, le=100), skip: int = 0):
    cursor = db.doctores.find().skip(skip).limit(limit)
    return [safe_doc(d) for d in cursor]

@app.get("/doctores/{id}", response_model=DoctorOut)
def get_doctor(id: str):
    doc = db.doctores.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    return safe_doc(doc)

@app.post("/doctores", response_model=DoctorOut, status_code=201)
def create_doctor(payload: DoctorIn):
    import uuid
    data = payload.dict()
    data["_id"] = str(uuid.uuid4())
    db.doctores.insert_one(data)
    return data

# ============ FARMACIAS ============
@app.get("/farmacias", response_model=List[FarmaciaOut])
def get_farmacias(limit: int = Query(50, le=100), skip: int = 0):
    cursor = db.farmacias.find().skip(skip).limit(limit)
    return [safe_doc(d) for d in cursor]

@app.get("/farmacias/{id}", response_model=FarmaciaOut)
def get_farmacia(id: str):
    doc = db.farmacias.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Farmacia no encontrada")
    return safe_doc(doc)

@app.post("/farmacias", response_model=FarmaciaOut, status_code=201)
def create_farmacia(payload: FarmaciaIn):
    import uuid
    data = payload.dict()
    data["_id"] = str(uuid.uuid4())
    db.farmacias.insert_one(data)
    return data

# ============ CITAS ============
@app.get("/citas", response_model=List[CitaOut])
def get_citas(limit: int = Query(50, le=100), skip: int = 0):
    cursor = db.citas.find().skip(skip).limit(limit)
    return [safe_doc(d) for d in cursor]

@app.get("/citas/{id}", response_model=CitaOut)
def get_cita(id: str):
    doc = db.citas.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return safe_doc(doc)

@app.post("/citas", response_model=CitaOut, status_code=201)
def create_cita(payload: CitaIn):
    import uuid
    data = payload.dict()
    data["_id"] = str(uuid.uuid4())
    db.citas.insert_one(data)
    return data

# ============ TRANSACCIONES ============
@app.get("/transacciones", response_model=List[TransaccionOut])
def get_transacciones(limit: int = Query(50, le=100), skip: int = 0):
    cursor = db.transacciones.find().skip(skip).limit(limit)
    return [safe_doc(d) for d in cursor]

@app.get("/transacciones/{id}", response_model=TransaccionOut)
def get_transaccion(id: str):
    doc = db.transacciones.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return safe_doc(doc)

@app.post("/transacciones", response_model=TransaccionOut, status_code=201)
def create_transaccion(payload: TransaccionIn):
    import uuid
    data = payload.dict()
    data["_id"] = str(uuid.uuid4())
    db.transacciones.insert_one(data)
    return data

# ============ STATS ============
@app.get("/stats")
def get_stats():
    return {
        "proveedores": db.proveedores.count_documents({}),
        "medicamentos": db.medicamentos.count_documents({}),
        "farmacias": db.farmacias.count_documents({}),
        "clientes": db.clientes.count_documents({}),
        "doctores": db.doctores.count_documents({}),
        "citas": db.citas.count_documents({}),
        "transacciones": db.transacciones.count_documents({})
    }
