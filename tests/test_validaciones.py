"""
tests/test_validaciones.py - Pruebas automatizadas con pytest
=============================================================

Aquí pruebo las funciones de validaciones.py de forma automática.
Cada función que empieza por "test_" es una prueba: le paso un dato
(válido o inválido) y con assert reviso que el resultado y los mensajes
de error sean los esperados.

No necesitan la base de datos. Se ejecutan con:  pytest -v
"""
import os
import sys
from datetime import date, timedelta

# Agrego la carpeta del proyecto al path para poder importar validaciones.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import validaciones as v  # noqa: E402


def test_texto_obligatorio_vacio():
    errores = []
    assert v.texto("   ", "Nombre", errores) is None
    assert errores == ["El campo Nombre es obligatorio."]


def test_texto_opcional_vacio_no_genera_error():
    errores = []
    assert v.texto("", "Raza", errores, requerido=False) is None
    assert errores == []


def test_texto_demasiado_largo():
    errores = []
    v.texto("a" * 61, "Nombres", errores, maximo=60)
    assert len(errores) == 1


def test_correo_valido_se_guarda_en_minusculas():
    errores = []
    assert v.correo("Ana.Perez@Gmail.com", "Correo", errores) == "ana.perez@gmail.com"
    assert errores == []


def test_correo_invalido():
    errores = []
    v.correo("ana.perez-gmail.com", "Correo", errores)
    assert "formato de correo" in errores[0]


def test_documento_con_letras():
    errores = []
    v.documento("10AB2233", "Documento", errores)
    assert len(errores) == 1


def test_numero_negativo():
    errores = []
    v.numero("-5", "Precio", errores, minimo=0)
    assert len(errores) == 1


def test_numero_no_numerico():
    errores = []
    assert v.numero("abc", "Precio", errores) is None
    assert len(errores) == 1


def test_numero_entero_valido():
    errores = []
    assert v.numero("30", "Duración", errores, entero=True) == 30
    assert errores == []


def test_fecha_futura_no_permitida():
    errores = []
    manana = (date.today() + timedelta(days=1)).isoformat()
    v.fecha(manana, "Fecha de nacimiento", errores, no_futura=True)
    assert "futura" in errores[0]


def test_hora_valida():
    errores = []
    assert v.hora("14:30", "Hora", errores).strftime("%H:%M") == "14:30"
    assert errores == []


def test_opcion_invalida():
    errores = []
    v.opcion("Dinosaurio", "Especie", errores, ["Perro", "Gato"])
    assert len(errores) == 1


def test_llave_foranea_inexistente():
    errores = []
    assert v.llave_foranea("99", "dueño", errores, {1, 2, 3}) is None
    assert "no existe" in errores[0]


def test_llave_foranea_valida():
    errores = []
    assert v.llave_foranea("2", "dueño", errores, {1, 2, 3}) == 2
    assert errores == []
