"""
routes/citas.py - CRUD de la tabla citas
========================================

Rutas para listar, crear, editar y eliminar citas (prefijo /citas).

La tabla citas es la tabla de "movimientos" del proyecto: tiene TRES
llaves foráneas (id_mascota, id_veterinario e id_servicio). Por eso:
  - El formulario tiene tres listas desplegables.
  - El listado hace varios JOIN para mostrar nombres en vez de ids.
  - Además se puede filtrar el listado por estado de la cita.
"""
import psycopg2
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

import validaciones as v
from db import consultar, ejecutar, mensaje_error

bp = Blueprint("citas", __name__, url_prefix="/citas")

# Estados posibles de una cita (igual que el CHECK en schema.sql)
ESTADOS = ["Programada", "Atendida", "Cancelada"]


def opciones():
    """Trae las opciones de las tres listas desplegables del formulario.

    En las tres consultas renombro la llave como "id" y el texto como
    "nombre", para que la plantilla las recorra todas de la misma forma.
    """
    return {
        # Mascota + especie + dueño, para no confundir mascotas con el mismo nombre
        "mascotas": consultar(
            """SELECT m.id_mascota AS id,
                      m.nombre || ' (' || m.especie || ') - ' || d.nombres || ' ' || d.apellidos AS nombre
               FROM mascotas m JOIN duenos d ON d.id_dueno = m.id_dueno
               ORDER BY m.nombre"""
        ),
        "veterinarios": consultar(
            """SELECT id_veterinario AS id,
                      nombres || ' ' || apellidos || ' - ' || especialidad AS nombre
               FROM veterinarios ORDER BY apellidos, nombres"""
        ),
        "servicios": consultar(
            "SELECT id_servicio AS id, nombre FROM servicios ORDER BY nombre"
        ),
    }


def leer_formulario(form, op):
    """Valida los datos de la cita y devuelve (datos, errores).

    "op" son las opciones de las listas; las uso para comprobar que la
    mascota, el veterinario y el servicio escogidos existen.
    """
    errores = []
    datos = {
        "fecha": v.fecha(form.get("fecha"), "Fecha", errores),
        "hora": v.hora(form.get("hora"), "Hora", errores),
        "motivo": v.texto(form.get("motivo"), "Motivo", errores, maximo=200),
        "estado": v.opcion(form.get("estado"), "Estado", errores, ESTADOS),
        "observaciones": v.texto(form.get("observaciones"), "Observaciones", errores,
                                 requerido=False, maximo=255),
        "id_mascota": v.llave_foranea(form.get("id_mascota"), "mascota", errores,
                                      {x["id"] for x in op["mascotas"]}),
        "id_veterinario": v.llave_foranea(form.get("id_veterinario"), "veterinario", errores,
                                          {x["id"] for x in op["veterinarios"]}),
        "id_servicio": v.llave_foranea(form.get("id_servicio"), "servicio", errores,
                                       {x["id"] for x in op["servicios"]}),
    }
    return datos, errores


@bp.route("/")
def listar():
    """Muestra las citas con los nombres de todo lo relacionado.

    Si en la URL viene ?estado=Programada (o Atendida / Cancelada), solo
    muestro las citas de ese estado.
    """
    estado = request.args.get("estado", "")
    # Uno las 4 tablas relacionadas para mostrar nombres en lugar de ids
    sql = """SELECT c.id_cita, c.fecha, c.hora, c.motivo, c.estado,
                    m.nombre AS mascota, m.especie,
                    d.nombres || ' ' || d.apellidos AS dueno,
                    ve.nombres || ' ' || ve.apellidos AS veterinario,
                    s.nombre AS servicio, s.precio
             FROM citas c
             JOIN mascotas m      ON m.id_mascota = c.id_mascota
             JOIN duenos d        ON d.id_dueno = m.id_dueno
             JOIN veterinarios ve ON ve.id_veterinario = c.id_veterinario
             JOIN servicios s     ON s.id_servicio = c.id_servicio"""
    params = None
    # Solo agrego el filtro si el estado es uno de los válidos. El valor
    # va como parámetro (%s), no pegado al texto del SQL.
    if estado in ESTADOS:
        sql += " WHERE c.estado = %s"
        params = (estado,)
    sql += " ORDER BY c.fecha DESC, c.hora DESC"
    registros = consultar(sql, params)
    return render_template("citas/listar.html", registros=registros, estados=ESTADOS, estado=estado)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    """Muestra el formulario (GET) y guarda la nueva cita (POST)."""
    op = opciones()
    registro = {"estado": "Programada"}  # por defecto una cita nueva está programada
    if request.method == "POST":
        datos, errores = leer_formulario(request.form, op)
        if not errores:
            try:
                ejecutar(
                    """INSERT INTO citas (fecha, hora, motivo, estado, observaciones,
                                         id_mascota, id_veterinario, id_servicio)
                       VALUES (%(fecha)s, %(hora)s, %(motivo)s, %(estado)s, %(observaciones)s,
                               %(id_mascota)s, %(id_veterinario)s, %(id_servicio)s)""",
                    datos,
                )
                flash("Cita registrada correctamente.", "success")
                return redirect(url_for("citas.listar"))
            except psycopg2.Error as e:
                # Por ejemplo: el veterinario ya tiene una cita a esa hora
                # (restricción UNIQUE uq_citas_vet_fecha_hora)
                errores.append(mensaje_error(e))
        for error in errores:
            flash(error, "danger")
        registro = request.form
    # **op envía mascotas, veterinarios y servicios a la plantilla
    return render_template("citas/form.html", registro=registro, titulo="Nueva cita",
                           estados=ESTADOS, **op)


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    """Muestra el formulario precargado (GET) y guarda los cambios (POST)."""
    # to_char deja la hora como "HH:MM", que es el formato del <input type="time">
    registro = consultar(
        """SELECT id_cita, fecha, to_char(hora, 'HH24:MI') AS hora, motivo, estado, observaciones,
                  id_mascota, id_veterinario, id_servicio
           FROM citas WHERE id_cita = %s""",
        (id,), uno=True,
    )
    if registro is None:
        abort(404)
    op = opciones()
    if request.method == "POST":
        datos, errores = leer_formulario(request.form, op)
        if not errores:
            datos["id"] = id
            try:
                ejecutar(
                    """UPDATE citas
                       SET fecha = %(fecha)s, hora = %(hora)s, motivo = %(motivo)s, estado = %(estado)s,
                           observaciones = %(observaciones)s, id_mascota = %(id_mascota)s,
                           id_veterinario = %(id_veterinario)s, id_servicio = %(id_servicio)s
                       WHERE id_cita = %(id)s""",
                    datos,
                )
                flash("Cita actualizada correctamente.", "success")
                return redirect(url_for("citas.listar"))
            except psycopg2.Error as e:
                errores.append(mensaje_error(e))
        for error in errores:
            flash(error, "danger")
        registro = request.form
    return render_template("citas/form.html", registro=registro, titulo="Editar cita",
                           estados=ESTADOS, **op)


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    """Elimina una cita. Ninguna tabla depende de citas, así que siempre se puede borrar."""
    try:
        if ejecutar("DELETE FROM citas WHERE id_cita = %s", (id,)):
            flash("Cita eliminada correctamente.", "success")
        else:
            flash("La cita no existe.", "warning")
    except psycopg2.Error as e:
        flash(mensaje_error(e), "danger")
    return redirect(url_for("citas.listar"))
