-- =============================================================
--  Koa Veterinaria - Script de creación de tablas (PostgreSQL)
-- -------------------------------------------------------------
--  Aquí creo las 5 tablas del proyecto con sus llaves primarias,
--  llaves foráneas y restricciones (NOT NULL, UNIQUE y CHECK).
--
--  Relaciones:
--    duenos       1 --- N  mascotas
--    mascotas     1 --- N  citas
--    veterinarios 1 --- N  citas
--    servicios    1 --- N  citas
--
--  Las llaves foráneas usan ON DELETE RESTRICT: no se puede
--  borrar un registro que esté siendo usado en otra tabla.
--  Uso SERIAL para que el id se genere solo (1, 2, 3...).
--
--  Se ejecuta conectado a la base de datos "veterinaria".
--  Primero borro las tablas (DROP) en orden inverso a las
--  dependencias, para poder ejecutar el script varias veces.
-- =============================================================

DROP TABLE IF EXISTS citas;
DROP TABLE IF EXISTS mascotas;
DROP TABLE IF EXISTS servicios;
DROP TABLE IF EXISTS veterinarios;
DROP TABLE IF EXISTS duenos;

-- -------------------------------------------------------------
-- 1. DUEÑOS: personas propietarias de las mascotas
-- -------------------------------------------------------------
CREATE TABLE duenos (
    id_dueno    SERIAL       PRIMARY KEY,
    documento   VARCHAR(15)  NOT NULL UNIQUE,
    nombres     VARCHAR(60)  NOT NULL,
    apellidos   VARCHAR(60)  NOT NULL,
    telefono    VARCHAR(15)  NOT NULL,
    correo      VARCHAR(100) NOT NULL UNIQUE,
    direccion   VARCHAR(120),
    CONSTRAINT ck_duenos_documento CHECK (documento ~ '^[0-9]{6,15}$'),
    CONSTRAINT ck_duenos_correo    CHECK (correo LIKE '%_@_%._%')
);

-- -------------------------------------------------------------
-- 2. VETERINARIOS: profesionales que atienden las citas
-- -------------------------------------------------------------
CREATE TABLE veterinarios (
    id_veterinario      SERIAL       PRIMARY KEY,
    documento           VARCHAR(15)  NOT NULL UNIQUE,
    nombres             VARCHAR(60)  NOT NULL,
    apellidos           VARCHAR(60)  NOT NULL,
    tarjeta_profesional VARCHAR(20)  NOT NULL UNIQUE,
    especialidad        VARCHAR(60)  NOT NULL,
    telefono            VARCHAR(15)  NOT NULL,
    correo              VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT ck_vet_documento CHECK (documento ~ '^[0-9]{6,15}$'),
    CONSTRAINT ck_vet_correo    CHECK (correo LIKE '%_@_%._%')
);

-- -------------------------------------------------------------
-- 3. SERVICIOS: catálogo de servicios que ofrece la clínica
-- -------------------------------------------------------------
CREATE TABLE servicios (
    id_servicio   SERIAL        PRIMARY KEY,
    nombre        VARCHAR(80)   NOT NULL UNIQUE,
    descripcion   VARCHAR(255),
    precio        NUMERIC(10,2) NOT NULL,
    duracion_min  INTEGER       NOT NULL,
    CONSTRAINT ck_servicios_precio   CHECK (precio >= 0),
    CONSTRAINT ck_servicios_duracion CHECK (duracion_min BETWEEN 5 AND 480)
);

-- -------------------------------------------------------------
-- 4. MASCOTAS: animales registrados (cada una tiene un dueño)
-- -------------------------------------------------------------
CREATE TABLE mascotas (
    id_mascota       SERIAL       PRIMARY KEY,
    nombre           VARCHAR(50)  NOT NULL,
    especie          VARCHAR(20)  NOT NULL,
    raza             VARCHAR(50),
    sexo             CHAR(1)      NOT NULL,
    fecha_nacimiento DATE,
    peso_kg          NUMERIC(6,2),
    id_dueno         INTEGER      NOT NULL,
    CONSTRAINT fk_mascotas_dueno FOREIGN KEY (id_dueno)
        REFERENCES duenos (id_dueno) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT ck_mascotas_especie CHECK (especie IN ('Perro','Gato','Ave','Conejo','Reptil','Otro')),
    CONSTRAINT ck_mascotas_sexo    CHECK (sexo IN ('M','H')),
    CONSTRAINT ck_mascotas_peso    CHECK (peso_kg IS NULL OR peso_kg > 0),
    CONSTRAINT ck_mascotas_fecha   CHECK (fecha_nacimiento IS NULL OR fecha_nacimiento <= CURRENT_DATE)
);

-- -------------------------------------------------------------
-- 5. CITAS: tabla transaccional con TRES llaves foráneas
--    (mascota, veterinario y servicio)
-- -------------------------------------------------------------
CREATE TABLE citas (
    id_cita         SERIAL       PRIMARY KEY,
    fecha           DATE         NOT NULL,
    hora            TIME         NOT NULL,
    motivo          VARCHAR(200) NOT NULL,
    estado          VARCHAR(15)  NOT NULL DEFAULT 'Programada',
    observaciones   VARCHAR(255),
    id_mascota      INTEGER      NOT NULL,
    id_veterinario  INTEGER      NOT NULL,
    id_servicio     INTEGER      NOT NULL,
    CONSTRAINT fk_citas_mascota FOREIGN KEY (id_mascota)
        REFERENCES mascotas (id_mascota) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_citas_veterinario FOREIGN KEY (id_veterinario)
        REFERENCES veterinarios (id_veterinario) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_citas_servicio FOREIGN KEY (id_servicio)
        REFERENCES servicios (id_servicio) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT ck_citas_estado CHECK (estado IN ('Programada','Atendida','Cancelada')),
    -- Un veterinario no puede tener dos citas a la misma fecha y hora
    CONSTRAINT uq_citas_vet_fecha_hora UNIQUE (id_veterinario, fecha, hora)
);
