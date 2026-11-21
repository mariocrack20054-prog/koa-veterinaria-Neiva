"""
routes/nosotros.py - Página "Conócenos"
=======================================

Esta página no usa la base de datos. Es una página informativa de la
clínica con:
  - una galería de fotos de pacientes con un mensaje cada una,
  - mensajes de clientes (testimonios),
  - consejos para cuidar a las mascotas,
  - la ubicación de la clínica en un mapa de Neiva.

Puse los textos en listas de Python para que la plantilla los recorra con
un for y no tener que repetir el mismo HTML muchas veces. Si quiero agregar
una foto o un mensaje, solo agrego un elemento a la lista.

La dirección y el mapa de la clínica están en config.py (CLINICA), porque
también los uso en el pie de página de todas las páginas.
"""
from flask import Blueprint, render_template

bp = Blueprint("nosotros", __name__, url_prefix="/nosotros")

# Galería: (archivo de la foto en static/img/galeria/, nombre, mensaje)
GALERIA = [
    ("g1.jpg", "Coco", "Llegó con tos y hoy vuelve a dormir tranquilo en su cama."),
    ("g2.jpg", "Simba", "Su primera vacuna fue todo un éxito. ¡Ni se dio cuenta!"),
    ("g3.jpg", "Pelusa", "También atendemos a los más pequeñitos de la casa."),
    ("g4.jpg", "Canela", "Después de su cirugía volvió a correr en la playa."),
    ("g5.jpg", "Michi", "Control al día y lista para seguir jugando."),
    ("g7.jpg", "Bolt", "Baño, corte de uñas y su mejor pinta para la foto."),
    ("g8.jpg", "Algodón", "Plan de nutrición especial para conejos."),
    ("g9.jpg", "Nieve", "Revisión de dientes y orejas: ¡todo perfecto!"),
]

# Lo que nos diferencia: (ícono de Bootstrap Icons, título, mensaje)
VALORES = [
    ("bi-heart-fill", "Atención con amor",
     "Tratamos a cada paciente como si fuera nuestro, con paciencia y cariño."),
    ("bi-clock-history", "Urgencias 24 horas",
     "Si tu mascota nos necesita a cualquier hora, aquí estamos."),
    ("bi-award-fill", "Equipo profesional",
     "Veterinarios especializados en medicina general, cirugía, dermatología y más."),
]

# Mensajes de clientes: (mensaje, nombre, mascota)
TESTIMONIOS = [
    ("Rocky tenía mucha picazón y en Koa encontraron la causa en la primera consulta. "
     "Ahora duerme tranquilo y nosotros también.", "Laura Trujillo", "dueña de Rocky"),
    ("La esterilización de Mía fue rápida y me explicaron todo el proceso. "
     "Se nota que aman a los animales.", "Martha Cabrera", "dueña de Mía"),
    ("Con el plan de nutrición Bruno bajó de peso y tiene más energía para jugar. "
     "¡Gracias a todo el equipo!", "Sebastián Guzmán", "dueño de Bruno"),
]

# Consejos de cuidado: (emoji, consejo)
CONSEJOS = [
    ("💉", "Mantén al día las vacunas y la desparasitación de tu mascota."),
    ("💧", "Deja siempre agua fresca y limpia a su alcance, sobre todo con el calor de Neiva."),
    ("🦮", "Saca a pasear a tu perro temprano o al final de la tarde para que no se queme las patas."),
    ("🦷", "Revisa sus dientes: el mal aliento puede ser señal de sarro o infección."),
    ("🩺", "Llévalo a control al menos una vez al año, aunque se vea sano."),
]


@bp.route("/")
def ver():
    """Muestra la página Conócenos con la galería, los mensajes y el mapa."""
    return render_template("nosotros.html", galeria=GALERIA, valores=VALORES,
                           testimonios=TESTIMONIOS, consejos=CONSEJOS)
