# Guía del código · Koa Veterinaria 🐾

En este documento explico para qué sirve el proyecto, cómo está organizado el código y cómo funciona cada parte.

## 1. ¿Para qué sirve la aplicación?

**Koa Veterinaria** es una aplicación web para administrar la información de una clínica veterinaria. Permite registrar:

| Módulo | Para qué sirve |
|---|---|
| **Dueños** | Las personas responsables de las mascotas (documento, nombre, teléfono, correo, dirección). |
| **Mascotas** | Los pacientes de la clínica. Cada mascota pertenece a un dueño. |
| **Veterinarios** | Los profesionales que atienden, con su tarjeta profesional y especialidad. |
| **Servicios** | El catálogo de lo que ofrece la clínica (consulta, vacunación, cirugía…), con precio y duración. |
| **Citas** | La agenda: une una mascota con un veterinario y un servicio en una fecha y hora. |
| **Conócenos** | Página informativa: galería de pacientes, mensajes de clientes, consejos y la ubicación de la clínica en el mapa. |

En cada módulo se puede **listar, crear, editar y eliminar** (CRUD).

## 2. Tecnologías que usé

- **Python 3 + Flask:** el servidor web. Recibe las peticiones del navegador y responde con páginas HTML.
- **PostgreSQL:** la base de datos donde se guarda todo.
- **psycopg2:** la librería que conecta Python con PostgreSQL.
- **Jinja2:** el motor de plantillas de Flask. Con él armo el HTML con los datos de la base de datos.
- **Bootstrap 5:** el framework de CSS para el diseño (tablas, formularios, menú, ventanas modales).
- **python-dotenv:** lee el archivo `.env` con la contraseña de la base de datos.
- **pytest:** las pruebas automatizadas.

## 3. Estructura de carpetas

```
proyecto/
├── app.py              → Arranca la aplicación y registra los Blueprints
├── config.py           → Lee la configuración del archivo .env
├── db.py               → Conexión a PostgreSQL y manejo de errores
├── validaciones.py     → Funciones para validar los formularios
├── routes/             → Un Blueprint (archivo) por cada tabla
│   ├── duenos.py
│   ├── mascotas.py
│   ├── veterinarios.py
│   ├── servicios.py
│   ├── citas.py
│   └── nosotros.py     → Página Conócenos (no usa la base de datos)
├── templates/          → Plantillas HTML (Jinja2)
│   ├── base.html       → Plantilla madre: menú, mensajes, pie de página
│   ├── _macros.html    → Piezas reutilizables (banner, botones)
│   ├── index.html      → Página de inicio
│   ├── error.html      → Página de error
│   ├── nosotros.html   → Página Conócenos
│   └── <tabla>/        → listar.html y form.html de cada tabla
├── static/
│   ├── css/estilos.css → Colores y diseño propio
│   ├── js/app.js       → Script de la ventana de confirmación
│   └── img/            → Fotos de la página (img/galeria/ para Conócenos)
├── database/
│   ├── schema.sql      → Crea las 5 tablas
│   ├── datos.sql       → Datos de ejemplo
│   ├── crear_bd.py     → Crea la base de datos y ejecuta los dos scripts
│   └── backup.sql      → Copia de seguridad hecha con pg_dump
├── docs/               → MER, diccionario de datos, pruebas y esta guía
└── tests/              → Pruebas automatizadas con pytest
```

## 4. ¿Qué pasa cuando alguien usa la página?

Ejemplo: el usuario llena el formulario de **Nuevo dueño** y presiona **Guardar**.

```
Navegador ──POST /duenos/nuevo──▶ Flask (app.py)
                                     │
                                     ▼
                     routes/duenos.py → crear()
                                     │
              1. leer_formulario() valida los datos (validaciones.py)
              2. Si hay errores → flash() con los mensajes y vuelve al formulario
              3. Si todo está bien → ejecutar("INSERT ...") en db.py
              4. Si PostgreSQL da error (ej. correo repetido) → mensaje_error()
              5. Si se guardó → flash("Dueño registrado") y redirect al listado
                                     │
                                     ▼
              render_template("duenos/listar.html") ──▶ HTML al navegador
```

## 5. Explicación de cada archivo

### `app.py`
Es el punto de entrada. Crea la aplicación con `create_app()`, carga la configuración, registra los 5 Blueprints y define:
- `/` (función `inicio`): cuenta los registros de cada tabla y muestra las próximas 5 citas.
- La página de error **404** y la página de **sin conexión** a la base de datos.

### `config.py`
Lee el archivo `.env` y guarda los datos de conexión en la clase `Config`. Así la contraseña no queda escrita en el código ni se sube a GitHub.

También tiene el diccionario `CLINICA` con la dirección, el teléfono, el horario y las coordenadas de la clínica. Con las coordenadas armo dos enlaces de Google Maps: el del mapa que se muestra dentro de la página y el del botón **Cómo llegar**. En `app.py` uso un `context_processor` para enviar `clinica` a todas las plantillas, por eso la dirección sale en el pie de página de todas las páginas.

### `db.py`
Tiene todo lo de la base de datos para no repetir código:

| Función | Qué hace |
|---|---|
| `get_db()` | Abre la conexión (una por petición, guardada en `g`). |
| `close_db()` | Cierra la conexión al terminar la petición. |
| `consultar(sql, params, uno)` | Ejecuta un `SELECT` y devuelve las filas como diccionarios. |
| `ejecutar(sql, params)` | Ejecuta `INSERT`, `UPDATE` o `DELETE`, hace `commit` y, si falla, `rollback`. |
| `tiene_relacionados(e)` | Dice si el error es porque el registro se usa en otra tabla. |
| `mensaje_error(e)` | Convierte el error de PostgreSQL en un mensaje entendible. |

### `validaciones.py`
Funciones que revisan cada dato del formulario **en el servidor**: `texto`, `correo`, `documento`, `telefono`, `numero`, `fecha`, `hora`, `opcion` y `llave_foranea`. Todas reciben la lista `errores` y le agregan un mensaje si el dato está mal.

### `routes/` (Blueprints)
Hice un archivo por tabla y **todos tienen la misma estructura**:

| Función | Ruta | Método | Qué hace |
|---|---|---|---|
| `leer_formulario()` | — | — | Valida el formulario y devuelve `(datos, errores)`. |
| `listar()` | `/tabla/` | GET | Muestra todos los registros. |
| `crear()` | `/tabla/nuevo` | GET / POST | Muestra el formulario vacío / guarda el registro. |
| `editar(id)` | `/tabla/<id>/editar` | GET / POST | Muestra el formulario precargado / guarda los cambios. |
| `eliminar(id)` | `/tabla/<id>/eliminar` | POST | Borra el registro (después de confirmar). |

Lo particular de cada uno:
- **duenos.py:** el más sencillo, sin llaves foráneas. En el listado cuento las mascotas de cada dueño.
- **mascotas.py:** tiene la llave foránea `id_dueno`, que se escoge en una lista desplegable (`lista_duenos()`). El listado usa `JOIN` para mostrar el nombre del dueño.
- **veterinarios.py** y **servicios.py:** como dueños, contando las citas de cada uno.
- **nosotros.py:** la página Conócenos. No usa la base de datos: los textos de la galería, los valores, los mensajes de clientes y los consejos están en listas de Python, y la plantilla las recorre con un `for`. Para agregar una foto o un mensaje solo agrego un elemento a la lista.
- **citas.py:** la tabla con **3 llaves foráneas**. La función `opciones()` llena las 3 listas desplegables, el listado une 5 tablas con `JOIN` y se puede filtrar por estado.

### `templates/`
- **base.html:** la plantilla madre. Las demás la heredan con `{% extends "base.html" %}` y solo llenan el bloque `contenido`. Tiene el menú, los mensajes `flash`, el pie de página y el modal para confirmar al eliminar.
- **_macros.html:** macros (como funciones, pero de HTML): `banner` (encabezado con foto), `acciones` (botones editar y eliminar) y `botones_form` (guardar y cancelar).
- **listar.html** de cada tabla: la tabla HTML con los registros.
- **form.html** de cada tabla: un solo formulario que sirve para **crear** y para **editar**.

### `static/`
- **css/estilos.css:** la paleta de colores y el diseño. Los colores están en variables (`--verde`, `--coral`, `--arena`…) al inicio del archivo, para cambiarlos en un solo lugar.
- **js/app.js:** cuando se presiona un botón de eliminar, le pasa al modal la URL y el nombre del registro.
- **img/:** fotos de Unsplash para la portada y los banners.

### `database/`
- **schema.sql:** crea las tablas con PK, FK, `NOT NULL`, `UNIQUE` y `CHECK`.
- **datos.sql:** inserta los datos de ejemplo.
- **crear_bd.py:** crea la base de datos y ejecuta los dos scripts.
- **backup.sql:** copia de seguridad generada con `pg_dump`.

## 6. Decisiones importantes

**Seguridad contra inyección SQL.** Nunca armo el SQL pegando texto. Siempre uso parámetros:

```python
consultar("SELECT * FROM duenos WHERE id_dueno = %s", (id,))
```

psycopg2 pone el valor de forma segura, así que aunque alguien escriba código SQL en un formulario, se guarda como texto normal.

**Validación doble.** Valido en Python (`validaciones.py`) y además la base de datos tiene sus propias reglas (`CHECK`, `UNIQUE`, `NOT NULL`). Si algo pasa la primera validación pero falla en la base de datos, lo atrapo con `try/except` y muestro un mensaje.

**Manejo de errores sin que la app falle.**

| Situación | Qué pasa |
|---|---|
| Dato inválido (correo mal escrito, número negativo…) | Mensaje de validación y el formulario conserva lo escrito. |
| Valor duplicado (correo, documento, tarjeta profesional) | Mensaje "Ya existe…". |
| Eliminar un dueño con mascotas (o un veterinario o servicio con citas) | Mensaje "No se puede eliminar…" (por `ON DELETE RESTRICT`). |
| Veterinario con dos citas a la misma hora | Mensaje "El veterinario ya tiene una cita…". |
| Registro que no existe | Página 404. |
| PostgreSQL apagado o contraseña incorrecta | Página "Sin conexión a la base de datos". |

**Post/Redirect/Get.** Después de guardar o eliminar redirijo al listado. Así, si el usuario recarga la página, el formulario no se envía otra vez.

**Llaves foráneas con listas desplegables.** El usuario nunca escribe un id: lo escoge de una lista. En el servidor reviso además que el id exista (`llave_foranea()`).

**Credenciales en `.env`.** La contraseña está en `.env`, que no se sube a GitHub. En el repositorio solo está `.env.example` como modelo.

## 7. Diseño

Escogí una paleta suave para transmitir calma y confianza:

| Color | Código | Dónde lo uso |
|---|---|---|
| Verde salvia | `#3d7a6e` | Color principal: menú activo, botones Guardar, títulos |
| Verde oscuro | `#24524a` | Pie de página, degradados de las fotos |
| Menta | `#e3f1ec` | Encabezados de tablas, contadores, botón editar |
| Coral | `#ef8a6f` | Botones importantes (Nuevo, Agendar cita, Eliminar) |
| Arena | `#f8f4ee` | Fondo de la página |

Las letras son **Fredoka** (títulos) y **Nunito** (texto), de Google Fonts. Las fotos llevan encima un degradado verde para que el texto blanco se lea bien.
