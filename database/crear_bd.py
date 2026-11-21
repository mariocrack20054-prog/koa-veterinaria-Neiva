"""
database/crear_bd.py - Crea la base de datos y carga los datos de ejemplo
=========================================================================

Hice este script para no tener que crear la base de datos a mano cada vez.
Hace tres pasos:
  1. Crea la base de datos "veterinaria" si todavía no existe.
  2. Ejecuta schema.sql (crea las 5 tablas; si ya existían las borra y
     las vuelve a crear).
  3. Ejecuta datos.sql (inserta los registros de ejemplo) y muestra
     cuántos registros quedaron en cada tabla.

Uso (desde la carpeta del proyecto, con el entorno virtual activo):
    python database/crear_bd.py

Los datos de conexión los lee del archivo .env.
"""
import os
import sys

import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Carpeta donde está este archivo (database/) y el .env que está una carpeta arriba
CARPETA = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(CARPETA, "..", ".env"))

conexion = dict(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", ""),
)
nombre_bd = os.getenv("DB_NAME", "veterinaria")

# ---- Paso 1: crear la base de datos si no existe ----
# Me conecto a la base "postgres" que siempre existe. CREATE DATABASE no se
# puede ejecutar dentro de una transacción, por eso activo autocommit.
conn = psycopg2.connect(dbname="postgres", **conexion)
conn.autocommit = True
with conn.cursor() as cur:
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (nombre_bd,))
    if cur.fetchone() is None:
        # sql.Identifier escribe el nombre de la base de datos de forma segura
        cur.execute(sql.SQL("CREATE DATABASE {} ENCODING 'UTF8'").format(sql.Identifier(nombre_bd)))
        print(f"Base de datos '{nombre_bd}' creada.")
    else:
        print(f"La base de datos '{nombre_bd}' ya existe.")
conn.close()

# ---- Pasos 2 y 3: crear las tablas y cargar los datos ----
conn = psycopg2.connect(dbname=nombre_bd, **conexion)
with conn, conn.cursor() as cur:
    for archivo in ("schema.sql", "datos.sql"):
        with open(os.path.join(CARPETA, archivo), encoding="utf-8") as f:
            cur.execute(f.read())
        print(f"Ejecutado {archivo}")
    # Muestro cuántos registros quedaron en cada tabla para comprobar
    for tabla in ("duenos", "mascotas", "veterinarios", "servicios", "citas"):
        cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(tabla)))
        print(f"  {tabla}: {cur.fetchone()[0]} registros")
conn.close()
sys.exit(0)
