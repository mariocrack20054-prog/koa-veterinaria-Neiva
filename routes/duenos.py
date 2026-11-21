"""
routes/duenos.py - CRUD de la tabla duenos
==========================================

Blueprint con las rutas para listar, crear, editar y eliminar dueños.
Todas las URL de este archivo empiezan por /duenos (url_prefix).

Este es el Blueprint más sencillo porque la tabla duenos no tiene llaves
foráneas. Los otros cuatro siguen exactamente la misma estructura.
"""
import psycopg2
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

import validaciones as v
from db import consultar, ejecutar, mensaje_error, tiene_relacionados

# "duenos" es el nombre del Blueprint; lo uso en url_for("duenos.listar")
bp = Blueprint("duenos", __name__, url_prefix="/duenos")


def leer_formulario(form):
    """Toma los datos del formulario, los valida y devuelve (datos, errores).

    "datos" es un diccionario con los valores ya limpios, listo para
    pasarlo a la consulta SQL. "errores" es una lista de mensajes; si está
    vacía, todo está bien.
    """
    errores = []
    datos = {
        "documento": v.documento(form.get("documento"), "Documento", errores),
        "nombres": v.texto(form.get("nombres"), "Nombres", errores, maximo=60),
        "apellidos": v.texto(form.get("apellidos"), "Apellidos", errores, maximo=60),
        "telefono": v.telefono(form.get("telefono"), "Teléfono", errores),
        "correo": v.correo(form.get("correo"), "Correo", errores),
        "direccion": v.texto(form.get("direccion"), "Dirección", errores, requerido=False, maximo=120),
    }
    return datos, errores


@bp.route("/")
def listar():
    """Muestra todos los dueños con la cantidad de mascotas de cada uno."""
    # LEFT JOIN para que también salgan los dueños que no tienen mascotas
    # (en ese caso COUNT da 0).
    registros = consultar(
        """SELECT d.*, COUNT(m.id_mascota) AS total_mascotas
           FROM duenos d
           LEFT JOIN mascotas m ON m.id_dueno = d.id_dueno
           GROUP BY d.id_dueno
           ORDER BY d.apellidos, d.nombres"""
    )
    return render_template("duenos/listar.html", registros=registros)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    """GET: muestra el formulario vacío. POST: valida y guarda el dueño."""
    registro = {}
    if request.method == "POST":
        datos, errores = leer_formulario(request.form)
        if not errores:
            try:
                # Consulta parametrizada: %(documento)s se reemplaza de forma
                # segura con datos["documento"], y así con cada campo.
                ejecutar(
                    """INSERT INTO duenos (documento, nombres, apellidos, telefono, correo, direccion)
                       VALUES (%(documento)s, %(nombres)s, %(apellidos)s, %(telefono)s, %(correo)s, %(direccion)s)""",
                    datos,
                )
                flash("Dueño registrado correctamente.", "success")
                # Después de guardar redirijo al listado (patrón Post/Redirect/Get)
                return redirect(url_for("duenos.listar"))
            except psycopg2.Error as e:
                # Por ejemplo: documento o correo repetido (UNIQUE)
                errores.append(mensaje_error(e))
        # Si hubo errores los muestro y vuelvo a mostrar lo que escribió el usuario
        for error in errores:
            flash(error, "danger")
        registro = request.form
    return render_template("duenos/form.html", registro=registro, titulo="Nuevo dueño")


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    """GET: formulario precargado con los datos actuales. POST: guarda los cambios."""
    registro = consultar("SELECT * FROM duenos WHERE id_dueno = %s", (id,), uno=True)
    if registro is None:
        abort(404)  # el id no existe -> página de error 404
    if request.method == "POST":
        datos, errores = leer_formulario(request.form)
        if not errores:
            datos["id"] = id
            try:
                ejecutar(
                    """UPDATE duenos
                       SET documento = %(documento)s, nombres = %(nombres)s, apellidos = %(apellidos)s,
                           telefono = %(telefono)s, correo = %(correo)s, direccion = %(direccion)s
                       WHERE id_dueno = %(id)s""",
                    datos,
                )
                flash("Dueño actualizado correctamente.", "success")
                return redirect(url_for("duenos.listar"))
            except psycopg2.Error as e:
                errores.append(mensaje_error(e))
        for error in errores:
            flash(error, "danger")
        registro = request.form
    return render_template("duenos/form.html", registro=registro, titulo="Editar dueño")


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    """Elimina un dueño. Solo acepta POST (viene del modal de confirmación)."""
    try:
        # ejecutar() devuelve cuántas filas borró: 0 significa que no existía
        if ejecutar("DELETE FROM duenos WHERE id_dueno = %s", (id,)):
            flash("Dueño eliminado correctamente.", "success")
        else:
            flash("El dueño no existe.", "warning")
    except psycopg2.Error as e:
        # Si el dueño tiene mascotas, la llave foránea no deja borrarlo
        if tiene_relacionados(e):
            flash("No se puede eliminar el dueño porque tiene mascotas registradas.", "danger")
        else:
            flash(mensaje_error(e), "danger")
    return redirect(url_for("duenos.listar"))
