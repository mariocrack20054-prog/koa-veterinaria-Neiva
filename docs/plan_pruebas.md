# Plan de pruebas funcionales · Koa Veterinaria

**Fecha de ejecución:** 20/11/2026  
**Entorno:** Windows 11, Python 3.12, Flask 3.1, PostgreSQL 18, navegador Microsoft Edge  
**Datos iniciales:** base de datos recién cargada con `database/schema.sql` y `database/datos.sql`

Cada caso tiene su captura de pantalla en la carpeta [`evidencias/`](evidencias/). En los casos de eliminación también hay una captura de la ventana de confirmación (`*_confirmacion.png`).

## Resumen

- Casos ejecutados: **18** (mínimo exigido: 15, 3 por tabla)
- Casos que cumplen: **18**

| Tabla | Casos |
|---|---|
| duenos | CP-01, CP-02, CP-03, CP-18 |
| mascotas | CP-04, CP-05, CP-06 |
| veterinarios | CP-07, CP-08, CP-09 |
| servicios | CP-10, CP-11, CP-12 |
| citas | CP-13, CP-14, CP-15, CP-16, CP-17 |

## Casos de prueba

| ID | Tabla | Operación | Datos de entrada | Resultado esperado | Resultado obtenido | Estado | Evidencia |
|---|---|---|---|---|---|---|---|
| CP-01 | duenos | Crear | Documento 1075123123, Ana Sofía Pérez Losada, correo ana.perez@gmail.com | Se guarda y aparece en el listado | Dueño registrado correctamente. | Cumple ✓ | [captura](evidencias/CP-01.png) |
| CP-02 | duenos | Crear (duplicado) | Correo ya registrado: carlos.perdomo@gmail.com | Mensaje de valor duplicado, no se guarda | Ya existe un dueño con ese correo. | Cumple ✓ | [captura](evidencias/CP-02.png) |
| CP-03 | duenos | Eliminar (con relacionados) | Dueño Carlos Andrés Perdomo (tiene 2 mascotas) | Pide confirmación y muestra: no se puede eliminar | No se puede eliminar el dueño porque tiene mascotas registradas. | Cumple ✓ | [captura](evidencias/CP-03.png) · [confirmación](evidencias/CP-03_confirmacion.png) |
| CP-04 | mascotas | Crear | Firulais, Perro, Macho, dueño elegido en lista desplegable (Camilo Ortiz) | Se guarda y el listado muestra el nombre del dueño | Mascota registrada correctamente. | Cumple ✓ | [captura](evidencias/CP-04.png) |
| CP-05 | mascotas | Crear (datos inválidos) | Sin nombre, especie, sexo ni dueño; peso -3; fecha 2030-01-01 | Mensajes de validación por cada campo, no se guarda | El campo Nombre es obligatorio. / Seleccione un valor válido para Especie. / Seleccione un valor válido para Sexo. / El campo Fecha de nacimiento no puede ser una fecha futura. / El campo Peso (kg) debe ser mayor o igual a 0.01. / Seleccione un(a) dueño. | Cumple ✓ | [captura](evidencias/CP-05.png) |
| CP-06 | mascotas | Editar | Mascota Lola: peso 3.10 → 3.5 (formulario precargado) | Se actualiza y el listado muestra 3.50 kg | Mascota actualizada correctamente. | Cumple ✓ | [captura](evidencias/CP-06.png) · [form precargado](evidencias/CP-06_precargado.png) |
| CP-07 | veterinarios | Listar | Abrir el menú Veterinarios | Tabla con los 10 veterinarios y su número de citas | (sin mensaje) | Cumple ✓ | [captura](evidencias/CP-07.png) |
| CP-08 | veterinarios | Crear (duplicado) | Tarjeta profesional TP-10234 (ya existe) | Mensaje de valor duplicado, no se guarda | Ya existe un veterinario con esa tarjeta profesional. | Cumple ✓ | [captura](evidencias/CP-08.png) |
| CP-09 | veterinarios | Eliminar (con relacionados) | Veterinaria Paula Andrea Muñoz (tiene citas) | Mensaje: no se puede eliminar | No se puede eliminar el veterinario porque tiene citas registradas. | Cumple ✓ | [captura](evidencias/CP-09.png) · [confirmación](evidencias/CP-09_confirmacion.png) |
| CP-10 | servicios | Editar | Consulta general: precio 45.000 → 50.000 | Se actualiza el precio en el listado | Servicio actualizado correctamente. | Cumple ✓ | [captura](evidencias/CP-10.png) |
| CP-11 | servicios | Crear (datos inválidos) | Precio -100 y duración 2 minutos | Mensajes de validación, no se guarda | El campo Precio debe ser mayor o igual a 0. / El campo Duración (min) debe ser mayor o igual a 5. | Cumple ✓ | [captura](evidencias/CP-11.png) |
| CP-12 | servicios | Eliminar | Servicio Hospitalización (día), sin citas asociadas | Pide confirmación, se elimina y desaparece del listado | Servicio eliminado correctamente. | Cumple ✓ | [captura](evidencias/CP-12.png) · [confirmación](evidencias/CP-12_confirmacion.png) |
| CP-13 | citas | Crear | Luna, Dra. Mónica Andrade, Consulta dermatológica, 01/12/2026 10:00 (listas desplegables) | Se guarda y el listado muestra mascota, dueño, veterinario y servicio por nombre | Cita registrada correctamente. | Cumple ✓ | [captura](evidencias/CP-13.png) |
| CP-14 | citas | Crear (duplicado) | Dr. Hernán Silva el 24/11/2026 a las 08:30 (ya ocupado) | Mensaje: el veterinario ya tiene una cita en esa fecha y hora | El veterinario ya tiene una cita en esa fecha y hora. | Cumple ✓ | [captura](evidencias/CP-14.png) |
| CP-15 | citas | Crear (datos inválidos) | Formulario vacío | Mensajes de campos obligatorios, no se guarda | El campo Fecha es obligatorio. / El campo Hora es obligatorio. / El campo Motivo es obligatorio. / Seleccione un(a) mascota. / Seleccione un(a) veterinario. / Seleccione un(a) servicio. | Cumple ✓ | [captura](evidencias/CP-15.png) |
| CP-16 | citas | Eliminar | Cita de Max del 28/11/2026 | Pide confirmación, se elimina y desaparece del listado | Cita eliminada correctamente. | Cumple ✓ | [captura](evidencias/CP-16.png) · [confirmación](evidencias/CP-16_confirmacion.png) |
| CP-17 | citas | Listar (filtro) | Filtro Programadas | Solo citas programadas, con nombres (no IDs) | (sin mensaje) | Cumple ✓ | [captura](evidencias/CP-17.png) |
| CP-18 | duenos | Eliminar | Dueña Ana Sofía Pérez (sin mascotas) | Pide confirmación y se elimina | Dueño eliminado correctamente. | Cumple ✓ | [captura](evidencias/CP-18.png) · [confirmación](evidencias/CP-18_confirmacion.png) |

## Evidencias

### CP-01 · duenos · Crear

![CP-01](evidencias/CP-01.png)

### CP-02 · duenos · Crear (duplicado)

![CP-02](evidencias/CP-02.png)

### CP-03 · duenos · Eliminar (con relacionados)

Confirmación previa:

![CP-03 confirmación](evidencias/CP-03_confirmacion.png)

![CP-03](evidencias/CP-03.png)

### CP-04 · mascotas · Crear

![CP-04](evidencias/CP-04.png)

### CP-05 · mascotas · Crear (datos inválidos)

![CP-05](evidencias/CP-05.png)

### CP-06 · mascotas · Editar

Formulario precargado:

![CP-06 precargado](evidencias/CP-06_precargado.png)

![CP-06](evidencias/CP-06.png)

### CP-07 · veterinarios · Listar

![CP-07](evidencias/CP-07.png)

### CP-08 · veterinarios · Crear (duplicado)

![CP-08](evidencias/CP-08.png)

### CP-09 · veterinarios · Eliminar (con relacionados)

Confirmación previa:

![CP-09 confirmación](evidencias/CP-09_confirmacion.png)

![CP-09](evidencias/CP-09.png)

### CP-10 · servicios · Editar

![CP-10](evidencias/CP-10.png)

### CP-11 · servicios · Crear (datos inválidos)

![CP-11](evidencias/CP-11.png)

### CP-12 · servicios · Eliminar

Confirmación previa:

![CP-12 confirmación](evidencias/CP-12_confirmacion.png)

![CP-12](evidencias/CP-12.png)

### CP-13 · citas · Crear

![CP-13](evidencias/CP-13.png)

### CP-14 · citas · Crear (duplicado)

![CP-14](evidencias/CP-14.png)

### CP-15 · citas · Crear (datos inválidos)

![CP-15](evidencias/CP-15.png)

### CP-16 · citas · Eliminar

Confirmación previa:

![CP-16 confirmación](evidencias/CP-16_confirmacion.png)

![CP-16](evidencias/CP-16.png)

### CP-17 · citas · Listar (filtro)

![CP-17](evidencias/CP-17.png)

### CP-18 · duenos · Eliminar

Confirmación previa:

![CP-18 confirmación](evidencias/CP-18_confirmacion.png)

![CP-18](evidencias/CP-18.png)

## Pruebas automatizadas (valor agregado)

La carpeta `tests/` tiene 14 pruebas con **pytest** de las funciones de validación (no necesitan la base de datos):

```powershell
pytest -v
```

Resultado: **14 passed**.
