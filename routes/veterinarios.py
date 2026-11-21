"""
routes/veterinarios.py - CRUD de la tabla veterinarios
======================================================

Rutas para listar, crear, editar y eliminar veterinarios (prefijo
/veterinarios). Tiene la misma estructura que routes/duenos.py.
"""
import psycopg2
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

import validaciones as v
from db import consultar, ejecutar, mensaje_error, tiene_relacionados

bp = Blueprint("veterinarios", __name__, url_prefix="/veterinarios")


def leer_formulario(form):
    """Valida los datos del formulario de veterinarios y devuelve (datos, errores)."""
    errores = []
    datos = {
        "documento": v.documento(form.get("documento"), "Documento", errores),
        "nombres": v.texto(form.get("nombres"), "Nombres", errores, maximo=60),
        "apellidos": v.texto(form.get("apellidos"), "Apellidos", errores, maximo=60),
        "tarjeta_profesional": v.texto(form.get("tarjeta_profesional"), "Tarjeta profesional", errores, maximo=20),
        "especialidad": v.texto(form.get("especialidad"), "Especialidad", errores, maximo=60),
        "telefono": v.telefono(form.get("telefono"), "Teléfono", errores),
        "correo": v.correo(form.get("correo"), "Correo", errores),
    }
    return datos, errores


@bp.route("/")
def listar():
    """Muestra todos los veterinarios y cuántas citas tiene cada uno."""
    registros = consultar(
        """SELECT ve.*, COUNT(c.id_cita) AS total_citas
           FROM veterinarios ve
           LEFT JOIN citas c ON c.id_veterinario = ve.id_veterinario
           GROUP BY ve.id_veterinario
           ORDER BY ve.apellidos, ve.nombres"""
    )
    return render_template("veterinarios/listar.html", registros=registros)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    """Muestra el formulario vacío (GET) y guarda el nuevo veterinario (POST)."""
    registro = {}
    if request.method == "POST":
        datos, errores = leer_formulario(request.form)
        if not errores:
            try:
                ejecutar(
                    """INSERT INTO veterinarios (documento, nombres, apellidos, tarjeta_profesional,
                                                especialidad, telefono, correo)
                       VALUES (%(documento)s, %(nombres)s, %(apellidos)s, %(tarjeta_profesional)s,
                               %(especialidad)s, %(telefono)s, %(correo)s)""",
                    datos,
                )
                flash("Veterinario registrado correctamente.", "success")
                return redirect(url_for("veterinarios.listar"))
            except psycopg2.Error as e:
                # Documento, correo o tarjeta profesional repetidos
                errores.append(mensaje_error(e))
        for error in errores:
            flash(error, "danger")
        registro = request.form
    return render_template("veterinarios/form.html", registro=registro, titulo="Nuevo veterinario")


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    """Muestra el formulario precargado (GET) y guarda los cambios (POST)."""
    registro = consultar("SELECT * FROM veterinarios WHERE id_veterinario = %s", (id,), uno=True)
    if registro is None:
        abort(404)
    if request.method == "POST":
        datos, errores = leer_formulario(request.form)
        if not errores:
            datos["id"] = id
            try:
                ejecutar(
                    """UPDATE veterinarios
                       SET documento = %(documento)s, nombres = %(nombres)s, apellidos = %(apellidos)s,
                           tarjeta_profesional = %(tarjeta_profesional)s, especialidad = %(especialidad)s,
                           telefono = %(telefono)s, correo = %(correo)s
                       WHERE id_veterinario = %(id)s""",
                    datos,
                )
                flash("Veterinario actualizado correctamente.", "success")
                return redirect(url_for("veterinarios.listar"))
            except psycopg2.Error as e:
                errores.append(mensaje_error(e))
        for error in errores:
            flash(error, "danger")
        registro = request.form
    return render_template("veterinarios/form.html", registro=registro, titulo="Editar veterinario")


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    """Elimina un veterinario, siempre que no tenga citas."""
    try:
        if ejecutar("DELETE FROM veterinarios WHERE id_veterinario = %s", (id,)):
            flash("Veterinario eliminado correctamente.", "success")
        else:
            flash("El veterinario no existe.", "warning")
    except psycopg2.Error as e:
        if tiene_relacionados(e):
            flash("No se puede eliminar el veterinario porque tiene citas registradas.", "danger")
        else:
            flash(mensaje_error(e), "danger")
    return redirect(url_for("veterinarios.listar"))
