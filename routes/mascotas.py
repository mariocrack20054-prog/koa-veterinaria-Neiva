"""
routes/mascotas.py - CRUD de la tabla mascotas
==============================================

Rutas para listar, crear, editar y eliminar mascotas (prefijo /mascotas).

Diferencia con duenos.py: cada mascota tiene una llave foránea (id_dueno).
Por eso:
  - En el formulario muestro una lista desplegable con los dueños.
  - En el listado uso un JOIN para mostrar el nombre del dueño y no su id.
"""
import psycopg2
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

import validaciones as v
from db import consultar, ejecutar, mensaje_error, tiene_relacionados

bp = Blueprint("mascotas", __name__, url_prefix="/mascotas")

# Valores permitidos (deben coincidir con los CHECK de la tabla en schema.sql)
ESPECIES = ["Perro", "Gato", "Ave", "Conejo", "Reptil", "Otro"]
SEXOS = {"M": "Macho", "H": "Hembra"}  # en la BD guardo la letra, en pantalla el texto


def lista_duenos():
    """Devuelve los dueños para llenar la lista desplegable del formulario.

    Junto nombre, apellido y documento en un solo texto con || para que
    sea fácil reconocer a cada dueño.
    """
    return consultar(
        """SELECT id_dueno, nombres || ' ' || apellidos || ' (' || documento || ')' AS nombre
           FROM duenos ORDER BY apellidos, nombres"""
    )


def leer_formulario(form, duenos):
    """Valida los datos de la mascota y devuelve (datos, errores).

    Recibe la lista de dueños para comprobar que el id_dueno escogido existe.
    """
    errores = []
    datos = {
        "nombre": v.texto(form.get("nombre"), "Nombre", errores, maximo=50),
        "especie": v.opcion(form.get("especie"), "Especie", errores, ESPECIES),
        "raza": v.texto(form.get("raza"), "Raza", errores, requerido=False, maximo=50),
        "sexo": v.opcion(form.get("sexo"), "Sexo", errores, SEXOS.keys()),
        "fecha_nacimiento": v.fecha(form.get("fecha_nacimiento"), "Fecha de nacimiento", errores,
                                    requerido=False, no_futura=True),
        "peso_kg": v.numero(form.get("peso_kg"), "Peso (kg)", errores, requerido=False,
                            minimo=0.01, maximo=9999),
        "id_dueno": v.llave_foranea(form.get("id_dueno"), "dueño", errores,
                                    {d["id_dueno"] for d in duenos}),
    }
    return datos, errores


@bp.route("/")
def listar():
    """Muestra todas las mascotas con el nombre de su dueño (JOIN)."""
    registros = consultar(
        """SELECT m.*, d.nombres || ' ' || d.apellidos AS dueno
           FROM mascotas m
           JOIN duenos d ON d.id_dueno = m.id_dueno
           ORDER BY m.nombre"""
    )
    return render_template("mascotas/listar.html", registros=registros, sexos=SEXOS)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    """Muestra el formulario con la lista de dueños (GET) y guarda la mascota (POST)."""
    duenos = lista_duenos()
    registro = {}
    if request.method == "POST":
        datos, errores = leer_formulario(request.form, duenos)
        if not errores:
            try:
                ejecutar(
                    """INSERT INTO mascotas (nombre, especie, raza, sexo, fecha_nacimiento, peso_kg, id_dueno)
                       VALUES (%(nombre)s, %(especie)s, %(raza)s, %(sexo)s,
                               %(fecha_nacimiento)s, %(peso_kg)s, %(id_dueno)s)""",
                    datos,
                )
                flash("Mascota registrada correctamente.", "success")
                return redirect(url_for("mascotas.listar"))
            except psycopg2.Error as e:
                errores.append(mensaje_error(e))
        for error in errores:
            flash(error, "danger")
        registro = request.form
    return render_template("mascotas/form.html", registro=registro, titulo="Nueva mascota",
                           duenos=duenos, especies=ESPECIES, sexos=SEXOS)


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    """Muestra el formulario precargado (GET) y guarda los cambios (POST)."""
    registro = consultar("SELECT * FROM mascotas WHERE id_mascota = %s", (id,), uno=True)
    if registro is None:
        abort(404)
    duenos = lista_duenos()
    if request.method == "POST":
        datos, errores = leer_formulario(request.form, duenos)
        if not errores:
            datos["id"] = id
            try:
                ejecutar(
                    """UPDATE mascotas
                       SET nombre = %(nombre)s, especie = %(especie)s, raza = %(raza)s, sexo = %(sexo)s,
                           fecha_nacimiento = %(fecha_nacimiento)s, peso_kg = %(peso_kg)s,
                           id_dueno = %(id_dueno)s
                       WHERE id_mascota = %(id)s""",
                    datos,
                )
                flash("Mascota actualizada correctamente.", "success")
                return redirect(url_for("mascotas.listar"))
            except psycopg2.Error as e:
                errores.append(mensaje_error(e))
        for error in errores:
            flash(error, "danger")
        registro = request.form
    return render_template("mascotas/form.html", registro=registro, titulo="Editar mascota",
                           duenos=duenos, especies=ESPECIES, sexos=SEXOS)


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    """Elimina una mascota, siempre que no tenga citas."""
    try:
        if ejecutar("DELETE FROM mascotas WHERE id_mascota = %s", (id,)):
            flash("Mascota eliminada correctamente.", "success")
        else:
            flash("La mascota no existe.", "warning")
    except psycopg2.Error as e:
        if tiene_relacionados(e):
            flash("No se puede eliminar la mascota porque tiene citas registradas.", "danger")
        else:
            flash(mensaje_error(e), "danger")
    return redirect(url_for("mascotas.listar"))
