"""
db.py - Conexión a PostgreSQL y funciones para ejecutar consultas
=================================================================

En este archivo centralicé todo lo que tiene que ver con la base de datos,
para no repetir el mismo código en cada Blueprint:

- get_db() / close_db(): abrir y cerrar la conexión.
- consultar(): para los SELECT.
- ejecutar(): para INSERT, UPDATE y DELETE.
- tiene_relacionados() y mensaje_error(): para convertir los errores de
  PostgreSQL en mensajes que el usuario entienda.

IMPORTANTE: todas las consultas usan parámetros (%s o %(nombre)s).
Nunca armo el SQL pegando texto, porque eso permitiría inyección SQL.
psycopg2 se encarga de poner los valores de forma segura.
"""
import psycopg2
from psycopg2 import errorcodes
from psycopg2.extras import RealDictCursor
from flask import g, current_app


def get_db():
    """Devuelve la conexión de la petición actual.

    Guardo la conexión en "g", que es un objeto de Flask que dura lo que
    dura una petición. Así, si en una misma página hago varias consultas,
    uso la misma conexión en lugar de abrir una nueva cada vez.
    """
    if "db" not in g:
        cfg = current_app.config
        g.db = psycopg2.connect(
            host=cfg["DB_HOST"],
            port=cfg["DB_PORT"],
            dbname=cfg["DB_NAME"],
            user=cfg["DB_USER"],
            password=cfg["DB_PASSWORD"],
        )
    return g.db


def close_db(e=None):
    """Cierra la conexión al terminar la petición (se registra en app.py)."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def consultar(sql, params=None, uno=False):
    """Ejecuta un SELECT y devuelve los resultados.

    Uso RealDictCursor para que cada fila llegue como diccionario
    (fila["nombre"]) en vez de tupla (fila[1]); así es más fácil
    usarlas en las plantillas.

    - uno=False: devuelve una lista con todas las filas.
    - uno=True:  devuelve solo la primera fila (o None si no hay).
    """
    with get_db().cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        filas = cur.fetchall()
    if uno:
        return filas[0] if filas else None
    return filas


def ejecutar(sql, params=None):
    """Ejecuta un INSERT, UPDATE o DELETE y guarda los cambios (commit).

    Si PostgreSQL devuelve un error (por ejemplo un valor duplicado),
    deshago la transacción con rollback y vuelvo a lanzar el error para
    que la ruta lo atrape y muestre un mensaje.

    Devuelve cuántas filas se afectaron. Lo uso al eliminar para saber
    si el registro existía.
    """
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            filas = cur.rowcount
        conn.commit()
        return filas
    except psycopg2.Error:
        conn.rollback()
        raise


# Mensajes personalizados para cada restricción UNIQUE de la base de datos.
# La clave es el nombre que PostgreSQL le da a la restricción.
RESTRICCIONES = {
    "duenos_documento_key": "Ya existe un dueño con ese documento.",
    "duenos_correo_key": "Ya existe un dueño con ese correo.",
    "veterinarios_documento_key": "Ya existe un veterinario con ese documento.",
    "veterinarios_correo_key": "Ya existe un veterinario con ese correo.",
    "veterinarios_tarjeta_profesional_key": "Ya existe un veterinario con esa tarjeta profesional.",
    "servicios_nombre_key": "Ya existe un servicio con ese nombre.",
    "uq_citas_vet_fecha_hora": "El veterinario ya tiene una cita en esa fecha y hora.",
}


def tiene_relacionados(e):
    """Dice si el error ocurrió porque el registro está siendo usado en otra tabla.

    Por ejemplo, al intentar borrar un dueño que tiene mascotas.
    Las llaves foráneas tienen ON DELETE RESTRICT, y según la versión
    PostgreSQL responde con el código 23001 (RESTRICT) o 23503 (FOREIGN KEY),
    así que reviso los dos.
    """
    return getattr(e, "pgcode", None) in (errorcodes.FOREIGN_KEY_VIOLATION,
                                          errorcodes.RESTRICT_VIOLATION)


def mensaje_error(e):
    """Convierte un error de PostgreSQL en un mensaje claro para el usuario."""
    # Primero miro si la restricción que falló tiene un mensaje propio
    restriccion = getattr(getattr(e, "diag", None), "constraint_name", None)
    if restriccion in RESTRICCIONES:
        return RESTRICCIONES[restriccion]

    # Si no, uso un mensaje general según el código del error
    codigo = getattr(e, "pgcode", None)
    if codigo == errorcodes.UNIQUE_VIOLATION:
        return "Ya existe un registro con ese valor (valor duplicado)."
    if tiene_relacionados(e):
        return ("No se puede completar la operación porque el registro "
                "tiene información relacionada en otra tabla.")
    if codigo == errorcodes.CHECK_VIOLATION:
        return "Algún dato no cumple las reglas de la base de datos."
    if codigo == errorcodes.NOT_NULL_VIOLATION:
        return "Falta un dato obligatorio."
    return "Ocurrió un error en la base de datos. Intente de nuevo."
