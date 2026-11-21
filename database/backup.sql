--
-- PostgreSQL database dump
--

\restrict 2fMelpgO5Nt04F7ssNEh7yQZm2p3ihr9gwUNdG3bkXgoX86GRdtcOJ0SYNgc4Rs

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: citas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.citas (
    id_cita integer NOT NULL,
    fecha date NOT NULL,
    hora time without time zone NOT NULL,
    motivo character varying(200) NOT NULL,
    estado character varying(15) DEFAULT 'Programada'::character varying NOT NULL,
    observaciones character varying(255),
    id_mascota integer NOT NULL,
    id_veterinario integer NOT NULL,
    id_servicio integer NOT NULL,
    CONSTRAINT ck_citas_estado CHECK (((estado)::text = ANY ((ARRAY['Programada'::character varying, 'Atendida'::character varying, 'Cancelada'::character varying])::text[])))
);


--
-- Name: citas_id_cita_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.citas_id_cita_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: citas_id_cita_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.citas_id_cita_seq OWNED BY public.citas.id_cita;


--
-- Name: duenos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.duenos (
    id_dueno integer NOT NULL,
    documento character varying(15) NOT NULL,
    nombres character varying(60) NOT NULL,
    apellidos character varying(60) NOT NULL,
    telefono character varying(15) NOT NULL,
    correo character varying(100) NOT NULL,
    direccion character varying(120),
    CONSTRAINT ck_duenos_correo CHECK (((correo)::text ~~ '%_@_%._%'::text)),
    CONSTRAINT ck_duenos_documento CHECK (((documento)::text ~ '^[0-9]{6,15}$'::text))
);


--
-- Name: duenos_id_dueno_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.duenos_id_dueno_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: duenos_id_dueno_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.duenos_id_dueno_seq OWNED BY public.duenos.id_dueno;


--
-- Name: mascotas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mascotas (
    id_mascota integer NOT NULL,
    nombre character varying(50) NOT NULL,
    especie character varying(20) NOT NULL,
    raza character varying(50),
    sexo character(1) NOT NULL,
    fecha_nacimiento date,
    peso_kg numeric(6,2),
    id_dueno integer NOT NULL,
    CONSTRAINT ck_mascotas_especie CHECK (((especie)::text = ANY ((ARRAY['Perro'::character varying, 'Gato'::character varying, 'Ave'::character varying, 'Conejo'::character varying, 'Reptil'::character varying, 'Otro'::character varying])::text[]))),
    CONSTRAINT ck_mascotas_fecha CHECK (((fecha_nacimiento IS NULL) OR (fecha_nacimiento <= CURRENT_DATE))),
    CONSTRAINT ck_mascotas_peso CHECK (((peso_kg IS NULL) OR (peso_kg > (0)::numeric))),
    CONSTRAINT ck_mascotas_sexo CHECK ((sexo = ANY (ARRAY['M'::bpchar, 'H'::bpchar])))
);


--
-- Name: mascotas_id_mascota_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mascotas_id_mascota_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mascotas_id_mascota_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mascotas_id_mascota_seq OWNED BY public.mascotas.id_mascota;


--
-- Name: servicios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.servicios (
    id_servicio integer NOT NULL,
    nombre character varying(80) NOT NULL,
    descripcion character varying(255),
    precio numeric(10,2) NOT NULL,
    duracion_min integer NOT NULL,
    CONSTRAINT ck_servicios_duracion CHECK (((duracion_min >= 5) AND (duracion_min <= 480))),
    CONSTRAINT ck_servicios_precio CHECK ((precio >= (0)::numeric))
);


--
-- Name: servicios_id_servicio_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.servicios_id_servicio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: servicios_id_servicio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.servicios_id_servicio_seq OWNED BY public.servicios.id_servicio;


--
-- Name: veterinarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.veterinarios (
    id_veterinario integer NOT NULL,
    documento character varying(15) NOT NULL,
    nombres character varying(60) NOT NULL,
    apellidos character varying(60) NOT NULL,
    tarjeta_profesional character varying(20) NOT NULL,
    especialidad character varying(60) NOT NULL,
    telefono character varying(15) NOT NULL,
    correo character varying(100) NOT NULL,
    CONSTRAINT ck_vet_correo CHECK (((correo)::text ~~ '%_@_%._%'::text)),
    CONSTRAINT ck_vet_documento CHECK (((documento)::text ~ '^[0-9]{6,15}$'::text))
);


--
-- Name: veterinarios_id_veterinario_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.veterinarios_id_veterinario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: veterinarios_id_veterinario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.veterinarios_id_veterinario_seq OWNED BY public.veterinarios.id_veterinario;


--
-- Name: citas id_cita; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas ALTER COLUMN id_cita SET DEFAULT nextval('public.citas_id_cita_seq'::regclass);


--
-- Name: duenos id_dueno; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.duenos ALTER COLUMN id_dueno SET DEFAULT nextval('public.duenos_id_dueno_seq'::regclass);


--
-- Name: mascotas id_mascota; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mascotas ALTER COLUMN id_mascota SET DEFAULT nextval('public.mascotas_id_mascota_seq'::regclass);


--
-- Name: servicios id_servicio; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servicios ALTER COLUMN id_servicio SET DEFAULT nextval('public.servicios_id_servicio_seq'::regclass);


--
-- Name: veterinarios id_veterinario; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.veterinarios ALTER COLUMN id_veterinario SET DEFAULT nextval('public.veterinarios_id_veterinario_seq'::regclass);


--
-- Data for Name: citas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.citas (id_cita, fecha, hora, motivo, estado, observaciones, id_mascota, id_veterinario, id_servicio) FROM stdin;
1	2026-11-03	08:00:00	Control anual	Atendida	Mascota en buen estado general	1	1	1
2	2026-11-03	09:00:00	Refuerzo de vacuna triple felina	Atendida	\N	2	1	2
3	2026-11-05	10:30:00	Picazón constante en el lomo	Atendida	Se formula champú medicado	3	3	7
4	2026-11-10	14:00:00	Esterilización programada	Atendida	Recuperación satisfactoria	4	2	5
5	2026-11-12	11:00:00	Sarro y mal aliento	Cancelada	El dueño canceló por viaje	5	4	6
6	2026-11-18	15:30:00	Cojea de la pata trasera	Atendida	Se toma radiografía	6	10	9
7	2026-11-24	08:30:00	Revisión de plumaje	Programada	\N	7	8	1
8	2026-11-24	09:30:00	Desparasitación trimestral	Programada	\N	8	6	3
9	2026-11-25	16:00:00	Baño y corte de pelo	Programada	\N	9	6	4
10	2026-11-26	10:00:00	Control de peso por sobrepeso	Programada	Traer historial de alimentación	10	9	11
11	2026-11-27	11:30:00	Revisión de escamas	Programada	\N	11	8	1
12	2026-11-28	08:00:00	Soplo cardíaco detectado	Programada	Se solicita ecografía	1	5	8
\.


--
-- Data for Name: duenos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.duenos (id_dueno, documento, nombres, apellidos, telefono, correo, direccion) FROM stdin;
1	1075234567	Carlos Andrés	Perdomo Rojas	3104567890	carlos.perdomo@gmail.com	Calle 10 # 5-23, Neiva
2	1075345678	Laura Marcela	Trujillo Vargas	3157894561	laura.trujillo@hotmail.com	Carrera 7 # 12-45, Neiva
3	36178945	Martha Lucía	Cabrera Silva	3201234567	martha.cabrera@gmail.com	Av. La Toma # 20-10, Neiva
4	1075456789	Andrés Felipe	Polanía Díaz	3009876543	andres.polania@yahoo.com	Calle 21 Sur # 3-15, Neiva
5	12134567	Jorge Eliécer	Medina Charry	3112223344	jorge.medina@gmail.com	Carrera 16 # 8-30, Neiva
6	1075567890	Valentina	Ramírez Ospina	3185556677	valentina.ramirez@gmail.com	Barrio Cándido, Mz 4 Casa 12
7	1075678901	Juan David	Cuéllar Motta	3046667788	juan.cuellar@outlook.com	Calle 64 # 1W-50, Neiva
8	55167890	Diana Patricia	Losada Quintero	3167778899	diana.losada@gmail.com	Carrera 2 # 54-20, Neiva
9	1075789012	Sebastián	Guzmán Puentes	3138889900	sebastian.guzman@gmail.com	Barrio Ipanema, Calle 8 # 33-11
10	1075890123	Natalia	Vargas Cerquera	3229990011	natalia.vargas@hotmail.com	Calle 18 # 30-05, Neiva
11	1075901234	Camilo	Ortiz Liévano	3051112233	camilo.ortiz@gmail.com	Carrera 5 # 9-70, Neiva
\.


--
-- Data for Name: mascotas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mascotas (id_mascota, nombre, especie, raza, sexo, fecha_nacimiento, peso_kg, id_dueno) FROM stdin;
1	Max	Perro	Labrador	M	2020-03-15	28.50	1
2	Luna	Gato	Siamés	H	2021-07-02	4.20	1
3	Rocky	Perro	Bulldog francés	M	2019-11-20	12.30	2
4	Mía	Gato	Criollo	H	2022-01-10	3.80	3
5	Toby	Perro	Beagle	M	2018-05-05	14.00	4
6	Kiara	Perro	Pastor alemán	H	2021-09-18	30.10	5
7	Piolín	Ave	Canario	M	2023-02-14	0.03	6
8	Copito	Conejo	Cabeza de león	M	2022-08-30	1.60	7
9	Nala	Gato	Persa	H	2020-12-01	4.90	8
10	Bruno	Perro	Golden retriever	M	2017-04-22	32.00	9
11	Spike	Reptil	Iguana verde	M	2021-06-11	2.40	10
12	Lola	Perro	Pinscher	H	2023-03-03	3.10	2
\.


--
-- Data for Name: servicios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.servicios (id_servicio, nombre, descripcion, precio, duracion_min) FROM stdin;
1	Consulta general	Valoración médica general de la mascota	45000.00	30
2	Vacunación	Aplicación de vacunas según el plan de vacunación	35000.00	15
3	Desparasitación	Desparasitación interna y externa	25000.00	15
4	Baño y peluquería	Baño medicado, corte de pelo y uñas	50000.00	60
5	Cirugía de esterilización	Esterilización con anestesia general	280000.00	120
6	Limpieza dental	Profilaxis dental con ultrasonido	150000.00	60
7	Consulta dermatológica	Diagnóstico de enfermedades de la piel	70000.00	40
8	Ecografía	Ecografía abdominal	120000.00	45
9	Radiografía	Estudio radiográfico (2 proyecciones)	95000.00	30
10	Hospitalización (día)	Hospitalización con monitoreo por 24 horas	180000.00	480
11	Control nutricional	Plan de alimentación y control de peso	55000.00	30
\.


--
-- Data for Name: veterinarios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.veterinarios (id_veterinario, documento, nombres, apellidos, tarjeta_profesional, especialidad, telefono, correo) FROM stdin;
1	1075111222	Paula Andrea	Muñoz Salazar	TP-10234	Medicina general	3101112222	paula.munoz@vetclinic.co
2	1075222333	Ricardo	Calderón Paz	TP-10567	Cirugía	3152223333	ricardo.calderon@vetclinic.co
3	1075333444	Mónica	Andrade Ruiz	TP-11021	Dermatología	3203334444	monica.andrade@vetclinic.co
4	1075444555	Felipe	Cortés Bahamón	TP-11345	Odontología	3004445555	felipe.cortes@vetclinic.co
5	1075555666	Juliana	Sánchez Tovar	TP-11789	Cardiología	3115556666	juliana.sanchez@vetclinic.co
6	1075666777	Esteban	Rojas Perdomo	TP-12003	Medicina general	3186667777	esteban.rojas@vetclinic.co
7	1075777888	Carolina	Díaz Montealegre	TP-12450	Oftalmología	3047778888	carolina.diaz@vetclinic.co
8	1075888999	Hernán	Silva Gutiérrez	TP-12876	Animales exóticos	3168889999	hernan.silva@vetclinic.co
9	1075999000	Lina María	Bonilla Ramos	TP-13102	Nutrición	3139990000	lina.bonilla@vetclinic.co
10	1076000111	Daniel	Quintero Leal	TP-13567	Traumatología	3220001111	daniel.quintero@vetclinic.co
\.


--
-- Name: citas_id_cita_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.citas_id_cita_seq', 12, true);


--
-- Name: duenos_id_dueno_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.duenos_id_dueno_seq', 11, true);


--
-- Name: mascotas_id_mascota_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mascotas_id_mascota_seq', 12, true);


--
-- Name: servicios_id_servicio_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.servicios_id_servicio_seq', 11, true);


--
-- Name: veterinarios_id_veterinario_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.veterinarios_id_veterinario_seq', 10, true);


--
-- Name: citas citas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT citas_pkey PRIMARY KEY (id_cita);


--
-- Name: duenos duenos_correo_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.duenos
    ADD CONSTRAINT duenos_correo_key UNIQUE (correo);


--
-- Name: duenos duenos_documento_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.duenos
    ADD CONSTRAINT duenos_documento_key UNIQUE (documento);


--
-- Name: duenos duenos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.duenos
    ADD CONSTRAINT duenos_pkey PRIMARY KEY (id_dueno);


--
-- Name: mascotas mascotas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mascotas
    ADD CONSTRAINT mascotas_pkey PRIMARY KEY (id_mascota);


--
-- Name: servicios servicios_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servicios
    ADD CONSTRAINT servicios_nombre_key UNIQUE (nombre);


--
-- Name: servicios servicios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servicios
    ADD CONSTRAINT servicios_pkey PRIMARY KEY (id_servicio);


--
-- Name: citas uq_citas_vet_fecha_hora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT uq_citas_vet_fecha_hora UNIQUE (id_veterinario, fecha, hora);


--
-- Name: veterinarios veterinarios_correo_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.veterinarios
    ADD CONSTRAINT veterinarios_correo_key UNIQUE (correo);


--
-- Name: veterinarios veterinarios_documento_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.veterinarios
    ADD CONSTRAINT veterinarios_documento_key UNIQUE (documento);


--
-- Name: veterinarios veterinarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.veterinarios
    ADD CONSTRAINT veterinarios_pkey PRIMARY KEY (id_veterinario);


--
-- Name: veterinarios veterinarios_tarjeta_profesional_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.veterinarios
    ADD CONSTRAINT veterinarios_tarjeta_profesional_key UNIQUE (tarjeta_profesional);


--
-- Name: citas fk_citas_mascota; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT fk_citas_mascota FOREIGN KEY (id_mascota) REFERENCES public.mascotas(id_mascota) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: citas fk_citas_servicio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT fk_citas_servicio FOREIGN KEY (id_servicio) REFERENCES public.servicios(id_servicio) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: citas fk_citas_veterinario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.citas
    ADD CONSTRAINT fk_citas_veterinario FOREIGN KEY (id_veterinario) REFERENCES public.veterinarios(id_veterinario) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: mascotas fk_mascotas_dueno; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mascotas
    ADD CONSTRAINT fk_mascotas_dueno FOREIGN KEY (id_dueno) REFERENCES public.duenos(id_dueno) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

\unrestrict 2fMelpgO5Nt04F7ssNEh7yQZm2p3ihr9gwUNdG3bkXgoX86GRdtcOJ0SYNgc4Rs

