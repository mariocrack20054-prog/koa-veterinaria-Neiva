# Justificación de la normalización (1FN, 2FN y 3FN)

## Reglas aplicadas

- **1FN:** cada campo guarda un solo valor atómico (sin listas ni grupos repetidos) y cada tabla tiene una llave primaria.
- **2FN:** está en 1FN y todos los atributos no clave dependen de **toda** la llave primaria. Como todas las tablas usan una llave primaria simple (un solo campo `SERIAL`), no pueden existir dependencias parciales.
- **3FN:** está en 2FN y ningún atributo no clave depende de otro atributo no clave (no hay dependencias transitivas).

## Análisis por tabla

### duenos
- **1FN:** un solo teléfono, un solo correo; nombres y apellidos en campos separados. PK `id_dueno`.
- **2FN:** PK simple, así que no hay dependencias parciales.
- **3FN:** documento, nombres, teléfono, correo y dirección describen solo al dueño. No se guardan datos de sus mascotas (esos van en `mascotas`).

### veterinarios
- **1FN:** valores atómicos, PK `id_veterinario`.
- **2FN:** PK simple.
- **3FN:** todos los atributos dependen solo del veterinario. La especialidad es un texto descriptivo del profesional y no determina ningún otro atributo.

### servicios
- **1FN:** valores atómicos, PK `id_servicio`.
- **2FN:** PK simple.
- **3FN:** precio y duración dependen directamente del servicio. El precio **no** se copia en `citas`: se consulta con un JOIN, así no hay redundancia.

### mascotas
- **1FN:** valores atómicos, PK `id_mascota`.
- **2FN:** PK simple.
- **3FN:** la mascota solo guarda `id_dueno` (FK). El nombre, teléfono o correo del dueño **no** se repiten en esta tabla, porque dependerían de `id_dueno` y no de `id_mascota` (sería una dependencia transitiva `id_mascota → id_dueno → nombre_dueño`).

### citas
- **1FN:** cada cita es una fila con valores atómicos (una fecha, una hora, un motivo). PK `id_cita`.
- **2FN:** PK simple, por lo tanto sin dependencias parciales.
- **3FN:** la cita guarda solo las llaves foráneas `id_mascota`, `id_veterinario` e `id_servicio`. Datos como el nombre de la mascota, el dueño, el nombre del veterinario o el precio del servicio **no** se almacenan aquí; se obtienen con JOIN. Así se evitan las dependencias transitivas y las anomalías de actualización (si cambia el precio de un servicio, se cambia en un solo lugar).

## Conclusión
Las cinco tablas cumplen 1FN, 2FN y 3FN. Cada dato se guarda una sola vez y las relaciones se representan mediante llaves foráneas.
