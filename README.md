# koa-veterinaria-Neiva

**Proyecto final de Programación Web**: aplicación web CRUD desarrollada con Flask y PostgreSQL para administrar una clínica veterinaria en Neiva, Huila.

## Integrantes

| Nombre | Codigo |
|---|---|
| Samuel Ramos Acuña | 20251233811 |
| Mario Hernan García Perdomo | 20242228996 |

**Curso:** Programación Web
**Docente:** Jose Miguel Llanos Mosquera
**Fecha de entrega:** 21 de noviembre de 2026


## Descripción del tema

**Koa Veterinaria** es una clínica veterinaria que necesita un sistema para organizar su información diaria. La aplicación permite gestionar:

| Módulo | Qué guarda |
|---|---|
| **Dueños** | Las personas responsables de las mascotas: documento, nombre, teléfono, correo y dirección. |
| **Mascotas** | Los pacientes de la clínica. Cada mascota pertenece a un dueño. |
| **Veterinarios** | Los profesionales de la clínica, con su tarjeta profesional y su especialidad. |
| **Servicios** | El catálogo de servicios (consulta, vacunación, cirugía, etc.) con su precio y duración. |
| **Citas** | La agenda de atención: une una **mascota**, un **veterinario** y un **servicio** en una fecha y hora. |

La tabla **citas** es la tabla de movimientos del proyecto, con **tres llaves foráneas** (`id_mascota`, `id_veterinario` e `id_servicio`).

### Funcionalidades

-  **CRUD completo** (listar, crear, editar y eliminar) de las 5 tablas.
-  Los listados muestran los **nombres** de los datos relacionados, no solo los ID.
-  Las llaves foráneas se escogen con **listas desplegables**.
-  **Validación de los formularios en el servidor** con mensajes claros.
-  **Manejo de errores** de la base de datos sin que la aplicación falle: valores duplicados, eliminar un registro con datos relacionados y un veterinario con dos citas a la misma hora.
-  **Confirmación antes de eliminar** (ventana modal).
-  **Consultas SQL parametrizadas** (protección contra inyección SQL).
-  Página de inicio con totales y próximas citas, y filtro de citas por estado.
-  Página **Conócenos** con galería, mensajes de clientes, consejos y la **ubicación de la clínica en un mapa de Neiva**.


## Modelo Entidad-Relación

<img width="848" height="712" alt="image" src="https://github.com/user-attachments/assets/c486642d-3448-4fbb-8224-b89219f88c24" />


**Relaciones:**

| Relación | Cardinalidad |
|---|---|
| Un **dueño** tiene muchas **mascotas** | 1 : N |
| Una **mascota** tiene muchas **citas** | 1 : N |
| Un **veterinario** atiende muchas **citas** | 1 : N |
| Un **servicio** se incluye en muchas **citas** | 1 : N |

### Documentación

| Documento | Contenido |
|---|---|
| [Diccionario de datos](docs/diccionario_datos.md) | Campos, tipos de dato y restricciones (PK, FK, NOT NULL, UNIQUE, CHECK) de cada tabla |
| [Normalización](docs/normalizacion.md) | Por qué cada tabla cumple 1FN, 2FN y 3FN |
| [Plan de pruebas](docs/plan_pruebas.md) | 18 casos de prueba con resultado y captura de evidencia |
| [Guía del código](docs/guia_del_codigo.md) | Para qué sirve cada archivo y cómo funciona la aplicación |
| [Backup de la base de datos](database/backup.sql) | Copia de seguridad generada con `pg_dump` |


## Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3 + Flask | Servidor web y rutas (un Blueprint por tabla) |
| PostgreSQL + psycopg2 | Base de datos y conexión desde Python |
| Jinja2 | Plantillas HTML con herencia (`base.html`) |
| Bootstrap 5 | Diseño de la interfaz |
| python-dotenv | Lectura de las credenciales desde `.env` |
| pytest | Pruebas automatizadas |
| Git y GitHub | Control de versiones |


## Estructura del proyecto

```
koa-veterinaria-Neiva/
├── app.py               # Punto de entrada de Flask
├── config.py            # Lectura de la configuración (.env) y datos de la clínica
├── db.py                # Conexión a PostgreSQL y manejo de errores
├── validaciones.py      # Validación de formularios en el servidor
├── routes/              # Un Blueprint por tabla
│   ├── duenos.py
│   ├── mascotas.py
│   ├── veterinarios.py
│   ├── servicios.py
│   ├── citas.py
│   └── nosotros.py      # Página Conócenos
├── templates/           # Plantillas Jinja2 (base.html + una carpeta por tabla)
├── static/              # CSS, JS e imágenes
├── database/
│   ├── schema.sql       # Creación de las 5 tablas
│   ├── datos.sql        # Carga de datos (10 o más registros por tabla)
│   ├── crear_bd.py      # Crea la base de datos y ejecuta los dos scripts
│   └── backup.sql       # Backup generado con pg_dump
├── docs/                # MER, diccionario, normalización, plan de pruebas y evidencias
├── tests/               # Pruebas automatizadas con pytest
├── requirements.txt
├── .env.example
└── .gitignore
```


## Instalación y ejecución

### Requisitos previos

- [Python 3.10 o superior](https://www.python.org/downloads/) (al instalarlo, marcar **"Add Python to PATH"**)
- [PostgreSQL](https://www.postgresql.org/download/) (con pgAdmin 4)
- [Git](https://git-scm.com/downloads)

### Paso 1. Clonar el repositorio

```powershell
git clone https://github.com/mariocrack20054-prog/koa-veterinaria-Neiva.git
cd koa-veterinaria-Neiva
```

### Paso 2. Crear el entorno virtual e instalar las dependencias

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> Si PowerShell no deja activar el entorno, ejecutar primero:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### Paso 3. Configurar la conexión a la base de datos

Copiar el archivo de ejemplo:

```powershell
copy .env.example .env
```

Abrir `.env` con el Bloc de notas y escribir la contraseña de PostgreSQL en `DB_PASSWORD`:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=veterinaria
DB_USER=postgres
DB_PASSWORD=la_contraseña_de_postgres
```

### Paso 4. Crear la base de datos

**Opción A: con el script** (crea la base de datos `veterinaria`, las tablas y los datos):

```powershell
python database/crear_bd.py
```

**Opción B: restaurando el backup en pgAdmin 4**
1. Crear una base de datos vacía llamada `veterinaria`.
2. Clic derecho sobre ella → **Query Tool** → abrir `database/backup.sql` → ejecutar (▶).

### Paso 5. Ejecutar la aplicación

```powershell
python app.py
```

Abrir en el navegador: **http://localhost:5000**

### Paso 6 (opcional). Ejecutar las pruebas automatizadas

```powershell
pytest -v
```

---

## Capturas de la aplicación

### Página de inicio
<img width="1280" height="1432" alt="inicio" src="https://github.com/user-attachments/assets/cf724248-f479-42e5-b889-eaf9c58db26a" />


### Dueños: listar y crear
<img width="1280" height="1410" alt="CP-01" src="https://github.com/user-attachments/assets/37af3380-f14d-4ba5-9558-edecf4e9a994" />


### Mascotas: listado con el nombre del dueño
<img width="1280" height="1408" alt="CP-04" src="https://github.com/user-attachments/assets/31faf4b3-a990-4d97-8a4e-de61de2892e1" />


### Mascotas: editar con el formulario precargado
<img width="1280" height="764" alt="CP-06_precargado" src="https://github.com/user-attachments/assets/c4227011-86ae-4456-9dda-390cded5f3f3" />


### Veterinarios
<img width="1280" height="1206" alt="CP-07" src="https://github.com/user-attachments/assets/01aaa3c0-2781-4fe2-a7e5-552ba45bfc81" />


### Servicios
<img width="1280" height="1202" alt="CP-10" src="https://github.com/user-attachments/assets/b4d96e4d-9043-4bf1-9e2f-367a58aca071" />


### Citas: listado con las tres llaves foráneas
<img width="1280" height="2013" alt="CP-13" src="https://github.com/user-attachments/assets/23bdf085-78e4-4449-a906-ebabc5648d74" />


### Validación de formularios en el servidor
<img width="1280" height="1315" alt="CP-15" src="https://github.com/user-attachments/assets/78b7d984-dc83-409b-aa11-5cfd2d855d17" />


### Valor duplicado
<img width="1280" height="836" alt="CP-02" src="https://github.com/user-attachments/assets/88e50aaa-f8d0-442d-ae6d-b98cb4651b91" />


### Confirmación antes de eliminar
<img width="1280" height="760" alt="CP-03_confirmacion" src="https://github.com/user-attachments/assets/22afab52-941a-477d-95bf-fef60bc51d91" />


### Error controlado al eliminar un registro relacionado
<img width="1280" height="1410" alt="CP-03" src="https://github.com/user-attachments/assets/90a599cd-2b96-402e-b145-1d48903615d7" />


### Página Conócenos y ubicación en Neiva
<img width="1280" height="3024" alt="nosotros" src="https://github.com/user-attachments/assets/1f7a45c4-1fbe-45ce-a155-238b433ad861" />



## 📍 Ubicación de la clínica

**Calle 15 # 8-21, Barrio Centro, Neiva, Huila**
Urgencias 24 horas · (608) 871 4520
