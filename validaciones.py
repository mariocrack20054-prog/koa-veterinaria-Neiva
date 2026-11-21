"""
validaciones.py - Validación de los formularios en el servidor
==============================================================

Aunque el navegador puede validar algunos campos, eso se puede saltar
fácilmente, así que valido todo otra vez aquí en Python antes de guardar.

Todas las funciones trabajan igual:
  - Reciben el valor que llegó del formulario, el nombre del campo
    (para el mensaje) y la lista "errores".
  - Si el dato está mal, agregan un mensaje a "errores".
  - Devuelven el valor limpio y convertido (texto sin espacios, número,
    fecha, etc.) o None si estaba vacío o era inválido.

Ejemplo de uso en una ruta:
    errores = []
    nombre = texto(form.get("nombre"), "Nombre", errores)
    if errores:  -> muestro los mensajes y no guardo nada
"""
import re
from datetime import date, datetime

# Expresiones regulares para revisar el formato de algunos datos
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")   # algo@dominio.com
PATRON_DOCUMENTO = re.compile(r"^[0-9]{6,15}$")              # solo números, 6 a 15
PATRON_TELEFONO = re.compile(r"^[0-9+ ]{7,15}$")             # números, + y espacios


def texto(valor, campo, errores, requerido=True, maximo=100):
    """Valida un texto: le quita los espacios y revisa que no sea muy largo."""
    valor = (valor or "").strip()
    if not valor:
        if requerido:
            errores.append(f"El campo {campo} es obligatorio.")
        return None
    if len(valor) > maximo:
        errores.append(f"El campo {campo} admite máximo {maximo} caracteres.")
    return valor


def correo(valor, campo, errores):
    """Valida un correo electrónico y lo guarda en minúsculas."""
    valor = texto(valor, campo, errores)
    if valor and not PATRON_CORREO.match(valor):
        errores.append(f"El campo {campo} no tiene un formato de correo válido.")
    return valor.lower() if valor else valor


def documento(valor, campo, errores):
    """Valida un documento de identidad: solo dígitos, entre 6 y 15."""
    valor = texto(valor, campo, errores, maximo=15)
    if valor and not PATRON_DOCUMENTO.match(valor):
        errores.append(f"El campo {campo} debe tener entre 6 y 15 dígitos.")
    return valor


def telefono(valor, campo, errores):
    """Valida un número de teléfono."""
    valor = texto(valor, campo, errores, maximo=15)
    if valor and not PATRON_TELEFONO.match(valor):
        errores.append(f"El campo {campo} debe tener entre 7 y 15 dígitos.")
    return valor


def numero(valor, campo, errores, requerido=True, minimo=None, maximo=None, entero=False):
    """Convierte el texto a número (entero o decimal) y revisa el rango.

    Cambio la coma por punto para aceptar "3,5" y "3.5".
    """
    valor = (valor or "").strip().replace(",", ".")
    if not valor:
        if requerido:
            errores.append(f"El campo {campo} es obligatorio.")
        return None
    try:
        n = int(valor) if entero else float(valor)
    except ValueError:
        tipo = "un número entero" if entero else "un número"
        errores.append(f"El campo {campo} debe ser {tipo}.")
        return None
    if minimo is not None and n < minimo:
        errores.append(f"El campo {campo} debe ser mayor o igual a {minimo}.")
    if maximo is not None and n > maximo:
        errores.append(f"El campo {campo} debe ser menor o igual a {maximo}.")
    return n


def fecha(valor, campo, errores, requerido=True, no_futura=False):
    """Convierte el texto "AAAA-MM-DD" en una fecha de Python.

    Con no_futura=True no permito fechas después de hoy
    (lo uso para la fecha de nacimiento de las mascotas).
    """
    valor = (valor or "").strip()
    if not valor:
        if requerido:
            errores.append(f"El campo {campo} es obligatorio.")
        return None
    try:
        f = datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError:
        errores.append(f"El campo {campo} no es una fecha válida.")
        return None
    if no_futura and f > date.today():
        errores.append(f"El campo {campo} no puede ser una fecha futura.")
    return f


def hora(valor, campo, errores):
    """Convierte el texto "HH:MM" en una hora de Python."""
    valor = (valor or "").strip()
    if not valor:
        errores.append(f"El campo {campo} es obligatorio.")
        return None
    try:
        return datetime.strptime(valor[:5], "%H:%M").time()
    except ValueError:
        errores.append(f"El campo {campo} no es una hora válida.")
        return None


def opcion(valor, campo, errores, opciones):
    """Revisa que el valor escogido esté dentro de las opciones permitidas.

    Lo uso para especie, sexo y estado, por si alguien modifica el HTML
    y envía un valor que no existe.
    """
    valor = (valor or "").strip()
    if valor not in opciones:
        errores.append(f"Seleccione un valor válido para {campo}.")
        return None
    return valor


def llave_foranea(valor, campo, errores, ids_validos):
    """Valida el id escogido en una lista desplegable (llave foránea).

    Reviso que sea un número y que ese id exista en la tabla relacionada
    (ids_validos es el conjunto de ids que sí existen).
    """
    try:
        n = int(valor)
    except (TypeError, ValueError):
        errores.append(f"Seleccione un(a) {campo}.")
        return None
    if n not in ids_validos:
        errores.append(f"El/la {campo} seleccionado(a) no existe.")
        return None
    return n
