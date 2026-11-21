"""
config.py - Configuración de la aplicación
==========================================

Aquí leo los datos de conexión a la base de datos desde el archivo .env.
Lo hago así para no escribir la contraseña dentro del código: el archivo
.env no se sube a GitHub (está en .gitignore). En el repositorio solo dejo
.env.example como modelo.
"""
import os
from dotenv import load_dotenv

# load_dotenv() lee el archivo .env y guarda sus valores como variables
# de entorno, que luego leo con os.getenv().
load_dotenv()


class Config:
    # Clave que usa Flask para firmar la sesión (los mensajes flash la necesitan)
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-de-desarrollo")

    # Datos de conexión a PostgreSQL. El segundo valor es el que se usa
    # si la variable no está en el .env.
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "veterinaria")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")


# Datos de contacto y ubicación de la clínica.
# Los pongo aquí en un solo lugar porque los uso en el pie de página de
# todas las páginas y en la página "Conócenos" (app.py los envía a todas
# las plantillas con un context_processor).
# La dirección es inventada: escogí un punto en el centro de Neiva (Huila).
CLINICA = {
    "nombre": "Koa Veterinaria",
    "direccion": "Calle 15 # 8-21, Barrio Centro",
    "ciudad": "Neiva, Huila",
    "telefono": "(608) 871 4520",
    "whatsapp": "310 555 0192",
    "correo": "contacto@koaveterinaria.co",
    "horario": [
        ("Lunes a viernes", "7:00 a. m. – 7:00 p. m."),
        ("Sábados", "8:00 a. m. – 4:00 p. m."),
        ("Domingos y festivos", "9:00 a. m. – 1:00 p. m."),
        ("Urgencias", "24 horas"),
    ],
    # Coordenadas del punto en el mapa (latitud, longitud)
    "latitud": 2.9335,
    "longitud": -75.2867,
}

# Con las coordenadas armo dos enlaces de Google Maps:
#  - mapa: para mostrar el mapa dentro de la página (iframe), no necesita clave
#  - como_llegar: abre Google Maps con la ruta hasta la clínica
CLINICA["mapa"] = (f"https://maps.google.com/maps?q={CLINICA['latitud']},{CLINICA['longitud']}"
                   f"&z=16&hl=es&output=embed")
CLINICA["como_llegar"] = (f"https://www.google.com/maps/dir/?api=1&destination="
                          f"{CLINICA['latitud']},{CLINICA['longitud']}")
