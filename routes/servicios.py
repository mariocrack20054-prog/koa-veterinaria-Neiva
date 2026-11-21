"""
routes/servicios.py - CRUD de la tabla servicios
================================================

Rutas para listar, crear, editar y eliminar los servicios que ofrece la
clínica (prefijo /servicios). Misma estructura que routes/duenos.py.
"""
import psycopg2
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

import validaciones as v
from db import consultar, ejecutar, mensaje_error, tiene_relacionados

bp = Blueprint("servicios", __name__, url_prefix="/servicios")


def leer_formulario(form):
    """Valida los datos del servicio y devuelve (datos, errores).

    El precio no puede ser negativo y la duración debe estar entre
    5 y 480 minutos (8 horas), igual que el CHECK de la base de datos.
    """
    errores = []
    datos = {
        "nombre": v.texto(form.get("nombre"), "Nombre", errores, maximo=80),
        "descripcion": v.texto(form.get("descripcion"), "Descripción", errores, requerido=False, maximo=255),
        "precio": v.numero(form.get("precio"), "Precio", errores, minimo=0, maximo=99999999),
        "duracion_min": v.numero(form.get("duracion_min"), "Duración (min)", errores,
                                 minimo=5, maximo=480, entero=True),
    }
    return datos, errores


@bp.route("/")
def listar():
    """Muestra el catálogo de servicios y cuántas citas usan cada uno."""
    registros = consultar(
        """SELECT s.*, COUNT(c.id_cita) AS total_citas
           FROM servicios s
           LEFT JOIN citas c ON c.id_servicio = s.id_servicio
           GROUP BY s.id_servicio
           ORDER BY s.nombre"""
    )
    return render_template("servicios/listar.html", registros=registros)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    """Muestra el formulario vacío (GET) y guarda el nuevo servicio (POST)."""
    registro = {}
    if request.method == "POST":
        datos, errores = leer_formulario(request.form)
        if not errores:
            try:
                ejecutar(
                    """INSERT INTO servicios (nombre, descripcion, precio, duracion_min)
                       VALUES (%(nombre)s, %(descripcion)s, %(precio)s, %(duracion_min)s)""",
                    datos,
                )
                flash("Servicio registrado correctamente.", "success")
                return redirect(url_for("servicios.listar"))
            except psycopg2.Error as e:
                # Por ejemplo: ya existe un servicio con ese nombre
                errores.append(mensaje_error(e))
        for error in errores:
            flash(error, "danger")
        registro = request.form
    return render_template("servicios/form.html", registro=registro, titulo="Nuevo servicio")


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    """Muestra el formulario precargado (GET) y guarda los cambios (POST)."""
    registro = consultar("SELECT * FROM servicios WHERE id_servicio = %s", (id,), uno=True)
    if registro is None:
        abort(404)
    if request.method == "POST":
        datos, errores = leer_formulario(request.form)
        if not errores:
            datos["id"] = id
            try:
                ejecutar(
                    """UPDATE servicios
                       SET nombre = %(nombre)s, descripcion = %(descripcion)s,
                           precio = %(precio)s, duracion_min = %(duracion_min)s
                       WHERE id_servicio = %(id)s""",
                    datos,
                )
                flash("Servicio actualizado correctamente.", "success")
                return redirect(url_for("servicios.listar"))
            except psycopg2.Error as e:
                errores.append(mensaje_error(e))
        for error in errores:
            flash(error, "danger")
        registro = request.form
    return render_template("servicios/form.html", registro=registro, titulo="Editar servicio")


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    """Elimina un servicio, siempre que ninguna cita lo use."""
    try:
        if ejecutar("DELETE FROM servicios WHERE id_servicio = %s", (id,)):
            flash("Servicio eliminado correctamente.", "success")
        else:
            flash("El servicio no existe.", "warning")
    except psycopg2.Error as e:
        if tiene_relacionados(e):
            flash("No se puede eliminar el servicio porque está asociado a citas.", "danger")
        else:
            flash(mensaje_error(e), "danger")
    return redirect(url_for("servicios.listar"))
