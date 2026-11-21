"""
app.py - Punto de entrada de la aplicación Koa Veterinaria
==========================================================

Este es el archivo que se ejecuta para iniciar la página web
(python app.py). Aquí hago tres cosas:

1. Creo la aplicación Flask y le cargo la configuración del archivo .env.
2. Registro los 5 Blueprints (uno por cada tabla de la base de datos),
   que están en la carpeta routes/, y el de la página "Conócenos".
3. Defino la página de inicio y las páginas de error.
"""
import psycopg2
from flask import Flask, render_template

from config import Config, CLINICA
from db import close_db, consultar

# Importo el Blueprint de cada tabla. Cada uno tiene sus propias rutas
# para listar, crear, editar y eliminar.
from routes.duenos import bp as duenos_bp
from routes.mascotas import bp as mascotas_bp
from routes.veterinarios import bp as veterinarios_bp
from routes.servicios import bp as servicios_bp
from routes.citas import bp as citas_bp
from routes.nosotros import bp as nosotros_bp   # página informativa "Conócenos"


def create_app():
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)

    # Cargo SECRET_KEY y los datos de conexión a PostgreSQL (ver config.py)
    app.config.from_object(Config)

    # Al terminar cada petición cierro la conexión a la base de datos
    # para no dejar conexiones abiertas.
    app.teardown_appcontext(close_db)

    # Registro un Blueprint por tabla. Así cada tabla queda en su propio
    # archivo y el código está más organizado.
    app.register_blueprint(duenos_bp)
    app.register_blueprint(mascotas_bp)
    app.register_blueprint(veterinarios_bp)
    app.register_blueprint(servicios_bp)
    app.register_blueprint(citas_bp)
    app.register_blueprint(nosotros_bp)

    @app.context_processor
    def datos_clinica():
        """Envía los datos de la clínica (dirección, teléfono, mapa) a TODAS
        las plantillas, así puedo usar {{ clinica.direccion }} en cualquiera."""
        return {"clinica": CLINICA}

    @app.route("/")
    def inicio():
        """Página de inicio: totales de cada tabla y próximas citas."""
        # Con una sola consulta cuento cuántos registros hay en cada tabla
        totales = consultar(
            """SELECT (SELECT COUNT(*) FROM duenos)       AS duenos,
                      (SELECT COUNT(*) FROM mascotas)     AS mascotas,
                      (SELECT COUNT(*) FROM veterinarios) AS veterinarios,
                      (SELECT COUNT(*) FROM servicios)    AS servicios,
                      (SELECT COUNT(*) FROM citas)        AS citas""",
            uno=True,
        )
        # Las 5 citas programadas más cercanas. Uso JOIN para mostrar
        # los nombres de la mascota, el veterinario y el servicio.
        proximas = consultar(
            """SELECT c.fecha, c.hora, m.nombre AS mascota,
                      v.nombres || ' ' || v.apellidos AS veterinario,
                      s.nombre AS servicio
               FROM citas c
               JOIN mascotas m     ON m.id_mascota = c.id_mascota
               JOIN veterinarios v ON v.id_veterinario = c.id_veterinario
               JOIN servicios s    ON s.id_servicio = c.id_servicio
               WHERE c.estado = 'Programada' AND c.fecha >= CURRENT_DATE
               ORDER BY c.fecha, c.hora
               LIMIT 5"""
        )
        return render_template("index.html", totales=totales, proximas=proximas)

    @app.errorhandler(404)
    def no_encontrado(e):
        """Se muestra cuando la página o el registro no existe."""
        return render_template("error.html", titulo="Página no encontrada",
                               mensaje="La página o el registro que busca no existe."), 404

    @app.errorhandler(psycopg2.OperationalError)
    def sin_conexion(e):
        """Se muestra si no me puedo conectar a PostgreSQL, en vez de que la app falle."""
        return render_template("error.html", titulo="Sin conexión a la base de datos",
                               mensaje="Revise que PostgreSQL esté encendido y que los datos "
                                       "del archivo .env sean correctos."), 500

    return app


# Creo la aplicación (Flask la busca con este nombre: app)
app = create_app()

if __name__ == "__main__":
    # debug=True recarga la app cuando guardo cambios y muestra los errores
    app.run(debug=True)
