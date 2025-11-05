#!/usr/bin/env python3
# scripts/run_all.py
# Script para ejecutar todo el proceso de setup de la base de datos
import subprocess
import sys
import os

def run_script(script_name, description):
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    result = subprocess.run([sys.executable, script_name], cwd=os.path.dirname(os.path.abspath(__file__)))
    if result.returncode != 0:
        print(f"❌ Error ejecutando {script_name}")
        sys.exit(1)
    print(f"✅ {description} completado")

if __name__ == "__main__":
    print("🏥 Iniciando setup completo de la base de datos Pharmacien")
    
    # Paso 1: Limpiar colecciones
    run_script("cleanup_collections.py", "Limpiando colecciones existentes")
    
    # Paso 2: Crear índices y validadores
    run_script("create_indexes_and_validators.py", "Creando índices y validadores")
    
    # Paso 3: Generar dataset
    run_script("generate_dataset_pharmacien.py", "Generando dataset de prueba")
    
    # Paso 4: Insertar datos
    run_script("ingest_dataset.py", "Insertando datos en MongoDB")
    
    print(f"\n{'='*60}")
    print("🎉 ¡Setup completo exitoso!")
    print("📊 Tu base de datos está lista con las 7 colecciones:")
    print("   - Proveedores (20)")
    print("   - Medicamentos (50)")
    print("   - Farmacias (10)")
    print("   - Clientes (40)")
    print("   - Doctores (25)")
    print("   - Citas (60)")
    print("   - Transacciones (80)")
    print(f"   TOTAL: 285 documentos")
    print(f"{'='*60}\n")
