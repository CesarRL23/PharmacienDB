#!/usr/bin/env python3
# scripts/generate_dataset_pharmacien.py
# Genera un dataset JSON con datos para las 7 colecciones
import json
import random
import uuid
import os
from datetime import datetime, timedelta

def random_date(start_year=2023, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def random_phone():
    return f"+52-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"


# Ciudades
ciudades = ["Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "Tijuana", "León", "Querétaro"]

# Categorías de medicamentos
categorias = [
    {"nombre": "Analgésicos", "descripcion": "Medicamentos para el dolor"},
    {"nombre": "Antibióticos", "descripcion": "Combaten infecciones bacterianas"},
    {"nombre": "Antiinflamatorios", "descripcion": "Reducen la inflamación"},
    {"nombre": "Antihistamínicos", "descripcion": "Tratan alergias"},
    {"nombre": "Dermatológicos", "descripcion": "Para la piel"},
    {"nombre": "Cardiológicos", "descripcion": "Para el corazón"},
    {"nombre": "Gastrointestinales", "descripcion": "Para el sistema digestivo"},
    {"nombre": "Vitaminas", "descripcion": "Suplementos vitamínicos"},
    {"nombre": "Respiratorios", "descripcion": "Para el sistema respiratorio"}
]

# Especialidades médicas
especialidades = [
    "Medicina General", "Pediatría", "Cardiología", "Dermatología",
    "Ginecología", "Traumatología", "Oftalmología", "Neurología"
]

# Métodos de pago
metodos_pago = ["Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito", "Transferencia", "Cheque"]

# 1. Generar Proveedores (20)
proveedores = []
nombres_proveedores = [
    "Farmacéutica Nacional", "Laboratorios del Valle", "MediSupply SA",
    "Distribuidora Salud", "Pharma Express", "Medicamentos del Norte",
    "Laboratorios Unidos", "Suministros Médicos", "Farma Distribución",
    "Productos Farmacéuticos", "Laboratorios Modernos", "Distribuidora Central",
    "Pharma Solutions", "Medicamentos Premium", "Laboratorios Avanzados",
    "Suministros Profesionales", "Farma Global", "Distribuidora Elite",
    "Laboratorios Especializados", "Medicamentos Integrales"
]

for i, nombre in enumerate(nombres_proveedores):
    prov_id = str(uuid.uuid4())
    proveedores.append({
        "_id": prov_id,
        "nombre": nombre,
        "telefono": random_phone(),
        "direccion": f"Av. Industrial {random.randint(100, 9999)}",
        "ciudad": random.choice(ciudades)
    })

# 2. Generar Medicamentos (50)
medicamentos = []
nombres_medicamentos = [
    "Paracetamol", "Ibuprofeno", "Amoxicilina", "Aspirina", "Omeprazol",
    "Loratadina", "Metformina", "Atorvastatina", "Losartán", "Diclofenaco",
    "Cetirizina", "Ranitidina", "Ciprofloxacino", "Azitromicina", "Naproxeno",
    "Clonazepam", "Alprazolam", "Fluoxetina", "Sertralina", "Enalapril",
    "Captopril", "Hidroclorotiazida", "Furosemida", "Prednisona", "Dexametasona",
    "Salbutamol", "Montelukast", "Insulina", "Glibenclamida", "Levotiroxina",
    "Vitamina C", "Vitamina D", "Complejo B", "Calcio", "Hierro",
    "Ketoconazol", "Clotrimazol", "Aciclovir", "Pantoprazol", "Esomeprazol",
    "Tramadol", "Codeína", "Morfina", "Gabapentina", "Pregabalina",
    "Warfarina", "Clopidogrel", "Simvastatina", "Amlodipino", "Carvedilol"
]

for i, nombre in enumerate(nombres_medicamentos):
    med_id = str(uuid.uuid4())
    categoria = random.choice(categorias)
    num_proveedores = random.randint(1, 3)
    provs_refs = random.sample([p["_id"] for p in proveedores], num_proveedores)
    
    medicamentos.append({
        "_id": med_id,
        "nombre": nombre,
        "precio": round(random.uniform(50.0, 1500.0), 2),
        "categoria": categoria,
        "proveedores": provs_refs
    })

# 3. Generar Empleados (30) - serán embebidos en farmacias
empleados_pool = []
nombres = ["Juan", "María", "Carlos", "Ana", "Luis", "Carmen", "José", "Laura", "Miguel", "Patricia"]
apellidos = ["García", "Rodríguez", "Martínez", "López", "González", "Pérez", "Sánchez", "Ramírez", "Torres", "Flores"]

for i in range(30):
    empleados_pool.append({
        "_id": str(uuid.uuid4()),
        "nombre": f"{random.choice(nombres)} {random.choice(apellidos)}",
        "puesto": random.choice(["Farmacéutico", "Auxiliar", "Cajero", "Gerente"]),
        "telefono": random_phone()
    })

# 4. Generar Farmacias (10)
farmacias = []
for i in range(1, 11):
    farm_id = str(uuid.uuid4())
    num_empleados = random.randint(2, 5)
    empleados_farmacia = random.sample(empleados_pool, num_empleados)
    
    num_medicamentos = random.randint(10, 25)
    meds_farmacia = random.sample([m["nombre"] for m in medicamentos], num_medicamentos)
    
    farmacias.append({
        "_id": farm_id,
        "ciudad": random.choice(ciudades),
        "direccion": f"Calle {random.randint(1, 100)} #{random.randint(100, 999)}",
        "telefono": random_phone(),
        "empleados": empleados_farmacia,
        "medicamentos": meds_farmacia
    })

# 5. Generar Clientes (40)
clientes = []
for i in range(40):
    cliente_id = str(uuid.uuid4())
    clientes.append({
        "_id": cliente_id,
        "nombre": f"{random.choice(nombres)} {random.choice(apellidos)}",
        "direccion": f"Calle {random.randint(1, 200)} #{random.randint(10, 999)}",
        "telefono": random_phone()
    })

# 6. Generar Doctores (25)
doctores = []
for i in range(25):
    doctor_id = str(uuid.uuid4())
    doctores.append({
        "_id": doctor_id,
        "nombre": random.choice(nombres),
        "apellido": random.choice(apellidos),
        "especialidad": random.choice(especialidades),
        "telefono": random_phone()
    })

# 7. Generar Citas (60)
citas = []
for i in range(60):
    cita_id = str(uuid.uuid4())
    cliente = random.choice(clientes)
    doctor = random.choice(doctores)
    
    # Receta embebida
    num_medicamentos_receta = random.randint(1, 4)
    receta = []
    for _ in range(num_medicamentos_receta):
        med = random.choice(medicamentos)
        receta.append({
            "medicamento_id": med["_id"],
            "medicamento_nombre": med["nombre"],
            "dosis": f"{random.randint(1, 3)} tableta(s) cada {random.choice([4, 6, 8, 12, 24])} horas",
            "duracion": f"{random.randint(3, 14)} días"
        })
    
    citas.append({
        "_id": cita_id,
        "fecha": random_date(2024, 2025),
        "cliente": {
            "_id": cliente["_id"],
            "nombre": cliente["nombre"],
            "telefono": cliente["telefono"]
        },
        "doctor": {
            "_id": doctor["_id"],
            "nombre": f"{doctor['nombre']} {doctor['apellido']}",
            "especialidad": doctor["especialidad"]
        },
        "receta": receta
    })

# 8. Generar Transacciones (80)
transacciones = []
for i in range(80):
    trans_id = str(uuid.uuid4())
    
    # 70% de transacciones tienen cita asociada
    cita_ref = random.choice(citas)["_id"] if random.random() < 0.7 else None
    
    # Empleado embebido
    empleado = random.choice(empleados_pool)
    empleado_embed = [{
        "_id": empleado["_id"],
        "nombre": empleado["nombre"],
        "puesto": empleado["puesto"]
    }]
    
    transacciones.append({
        "_id": trans_id,
        "fecha": random_date(2024, 2025),
        "totalpagado": round(random.uniform(100.0, 5000.0), 2),
        "metodopago": random.choice(metodos_pago),
        "empleado": empleado_embed,
        "citaref": cita_ref
    })

# Crear dataset completo
dataset = {
    "generated_at": datetime.utcnow().isoformat(),
    "counts": {
        "proveedores": len(proveedores),
        "medicamentos": len(medicamentos),
        "farmacias": len(farmacias),
        "clientes": len(clientes),
        "doctores": len(doctores),
        "citas": len(citas),
        "transacciones": len(transacciones),
        "total": len(proveedores) + len(medicamentos) + len(farmacias) + len(clientes) + len(doctores) + len(citas) + len(transacciones)
    },
    "proveedores": proveedores,
    "medicamentos": medicamentos,
    "farmacias": farmacias,
    "clientes": clientes,
    "doctores": doctores,
    "citas": citas,
    "transacciones": transacciones
}

# Guardar dataset
os.makedirs("data", exist_ok=True)
with open("data/pharmacien_rag_dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2, default=str)

print(f"Dataset generado: data/pharmacien_rag_dataset.json")
print(f"Total de documentos: {dataset['counts']['total']}")
print(f"Desglose:")
for key, value in dataset['counts'].items():
    if key != 'total':
        print(f"  - {key}: {value}")
