#!/usr/bin/env python3
# scripts/generate_dataset_pharmacien.py
# Genera un dataset JSON con 100 documentos de texto y 50 imágenes para el dominio "pharmacien".
import json, random, uuid
from datetime import datetime, timedelta

def random_date(start_year=2019, end_year=2025):
    start = datetime(start_year,1,1)
    end = datetime(end_year,12,31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).isoformat()

topics = [
    "Analgesicos","Antibioticos","Antiinflamatorios","Antihistaminicos",
    "Dermatologicos","Cardiologicos","Gastrointestinales","Vitaminas","Respiratorios"
]

# Imagenes (50)
images = []
for i in range(1,51):
    iid = str(uuid.uuid4())
    images.append({
        "_id": iid,
        "filename": f"med_image_{i}.jpg",
        "url": f"https://picsum.photos/seed/{iid}/1024/768",
        "caption": f"Imagen de producto medicamento #{i}",
        "metadata": {"resolution":"1024x768","format":"jpeg","source":"placeholder_picsum","created_at": random_date(2019,2025)},
        "related_med_id": f"M{str(random.randint(1,120)).zfill(4)}",
        "embeddings": None
    })

# Documentos de texto (100)
text_docs = []
for i in range(1,101):
    doc_id = str(uuid.uuid4())
    med_id = f"M{str(random.randint(1,120)).zfill(4)}"
    doc_type = random.choices(
        ["product_description","clinical_note","prescription_explanation","usage_guide","pharmacy_notice"],
        weights=[40,20,20,15,5]
    )[0]
    title_map = {
        "product_description": f"Ficha técnica {med_id}",
        "clinical_note": f"Nota clínica {med_id} - Caso {i}",
        "prescription_explanation": f"Explicación de receta para {med_id}",
        "usage_guide": f"Guía de uso de {med_id}",
        "pharmacy_notice": f"Aviso de farmacia F{random.randint(1,7)}"
    }
    content_templates = {
        "product_description": (
            "Descripción del medicamento, indicaciones, dosis y precauciones. "
            "Presentación en tabletas/jarabe/crema. Mantener fuera del alcance de los niños."
        ),
        "clinical_note": (
            "Paciente presenta síntomas leves. Recomendado seguimiento clínico y revisión de interacciones."
        ),
        "prescription_explanation": (
            "Administrar 1 tableta cada 8 horas durante 7 días. No tomar con alcohol."
        ),
        "usage_guide": (
            "Lea el prospecto antes de usar. No exceder la dosis indicada. Conservar a temperatura ambiente."
        ),
        "pharmacy_notice": (
            "Horario de atención extendido esta semana por inventario. Llevar receta original para controlados."
        )
    }
    content = content_templates[doc_type] + " " + " ".join([f"detalle_{j}" for j in range(random.randint(0,20))])
    linked_images = random.sample(images, k=random.choices([0,1,2], weights=[60,30,10])[0])
    text_docs.append({
        "_id": doc_id,
        "doc_type": doc_type,
        "title": title_map[doc_type],
        "content": content,
        "language": "es",
        "related_medicamento": med_id,
        "tags": [random.choice(topics)],
        "images": [img["_id"] for img in linked_images],
        "metadata": {
            "author": random.choice(["Farmacéutico A","Sistema","Dr. X"]),
            "source": random.choice(["internal","manufacturer","doctor_note","patient_upload"]),
            "length_words": len(content.split())
        },
        "embeddings": None,
        "ingest_ts": datetime.utcnow().isoformat()
    })

dataset = {
    "generated_at": datetime.utcnow().isoformat(),
    "counts": {"text_documents": len(text_docs), "images": len(images)},
    "images": images,
    "text_documents": text_docs
}

with open("data/pharmacien_rag_dataset.json","w",encoding="utf-8") as f:
    json.dump(dataset,f,ensure_ascii=False,indent=2)

print("Dataset generado: data/pharmacien_rag_dataset.json")
