-- =============================================================
--  Koa Veterinaria - Script de carga de datos
-- -------------------------------------------------------------
--  Inserto datos de ejemplo (mínimo 10 por tabla) para poder
--  probar la aplicación. El orden importa: primero las tablas
--  que no dependen de nadie (duenos, veterinarios, servicios),
--  luego mascotas (necesita duenos) y al final citas (necesita
--  mascotas, veterinarios y servicios).
--  No escribo los id porque SERIAL los genera solos (1, 2, 3...).
-- =============================================================

INSERT INTO duenos (documento, nombres, apellidos, telefono, correo, direccion) VALUES
('1075234567', 'Carlos Andrés', 'Perdomo Rojas',   '3104567890', 'carlos.perdomo@gmail.com',   'Calle 10 # 5-23, Neiva'),
('1075345678', 'Laura Marcela', 'Trujillo Vargas', '3157894561', 'laura.trujillo@hotmail.com', 'Carrera 7 # 12-45, Neiva'),
('36178945',   'Martha Lucía',  'Cabrera Silva',   '3201234567', 'martha.cabrera@gmail.com',   'Av. La Toma # 20-10, Neiva'),
('1075456789', 'Andrés Felipe', 'Polanía Díaz',    '3009876543', 'andres.polania@yahoo.com',   'Calle 21 Sur # 3-15, Neiva'),
('12134567',   'Jorge Eliécer', 'Medina Charry',   '3112223344', 'jorge.medina@gmail.com',     'Carrera 16 # 8-30, Neiva'),
('1075567890', 'Valentina',     'Ramírez Ospina',  '3185556677', 'valentina.ramirez@gmail.com','Barrio Cándido, Mz 4 Casa 12'),
('1075678901', 'Juan David',    'Cuéllar Motta',   '3046667788', 'juan.cuellar@outlook.com',   'Calle 64 # 1W-50, Neiva'),
('55167890',   'Diana Patricia','Losada Quintero', '3167778899', 'diana.losada@gmail.com',     'Carrera 2 # 54-20, Neiva'),
('1075789012', 'Sebastián',     'Guzmán Puentes',  '3138889900', 'sebastian.guzman@gmail.com', 'Barrio Ipanema, Calle 8 # 33-11'),
('1075890123', 'Natalia',       'Vargas Cerquera', '3229990011', 'natalia.vargas@hotmail.com', 'Calle 18 # 30-05, Neiva'),
('1075901234', 'Camilo',        'Ortiz Liévano',   '3051112233', 'camilo.ortiz@gmail.com',     'Carrera 5 # 9-70, Neiva');

INSERT INTO veterinarios (documento, nombres, apellidos, tarjeta_profesional, especialidad, telefono, correo) VALUES
('1075111222', 'Paula Andrea',   'Muñoz Salazar',  'TP-10234', 'Medicina general',     '3101112222', 'paula.munoz@vetclinic.co'),
('1075222333', 'Ricardo',        'Calderón Paz',   'TP-10567', 'Cirugía',              '3152223333', 'ricardo.calderon@vetclinic.co'),
('1075333444', 'Mónica',         'Andrade Ruiz',   'TP-11021', 'Dermatología',         '3203334444', 'monica.andrade@vetclinic.co'),
('1075444555', 'Felipe',         'Cortés Bahamón', 'TP-11345', 'Odontología',          '3004445555', 'felipe.cortes@vetclinic.co'),
('1075555666', 'Juliana',        'Sánchez Tovar',  'TP-11789', 'Cardiología',          '3115556666', 'juliana.sanchez@vetclinic.co'),
('1075666777', 'Esteban',        'Rojas Perdomo',  'TP-12003', 'Medicina general',     '3186667777', 'esteban.rojas@vetclinic.co'),
('1075777888', 'Carolina',       'Díaz Montealegre','TP-12450','Oftalmología',         '3047778888', 'carolina.diaz@vetclinic.co'),
('1075888999', 'Hernán',         'Silva Gutiérrez','TP-12876', 'Animales exóticos',    '3168889999', 'hernan.silva@vetclinic.co'),
('1075999000', 'Lina María',     'Bonilla Ramos',  'TP-13102', 'Nutrición',            '3139990000', 'lina.bonilla@vetclinic.co'),
('1076000111', 'Daniel',         'Quintero Leal',  'TP-13567', 'Traumatología',        '3220001111', 'daniel.quintero@vetclinic.co');

INSERT INTO servicios (nombre, descripcion, precio, duracion_min) VALUES
('Consulta general',      'Valoración médica general de la mascota',            45000, 30),
('Vacunación',            'Aplicación de vacunas según el plan de vacunación',  35000, 15),
('Desparasitación',       'Desparasitación interna y externa',                  25000, 15),
('Baño y peluquería',     'Baño medicado, corte de pelo y uñas',                50000, 60),
('Cirugía de esterilización','Esterilización con anestesia general',            280000, 120),
('Limpieza dental',       'Profilaxis dental con ultrasonido',                  150000, 60),
('Consulta dermatológica','Diagnóstico de enfermedades de la piel',             70000, 40),
('Ecografía',             'Ecografía abdominal',                                120000, 45),
('Radiografía',           'Estudio radiográfico (2 proyecciones)',              95000, 30),
('Hospitalización (día)', 'Hospitalización con monitoreo por 24 horas',         180000, 480),
('Control nutricional',   'Plan de alimentación y control de peso',             55000, 30);

INSERT INTO mascotas (nombre, especie, raza, sexo, fecha_nacimiento, peso_kg, id_dueno) VALUES
('Max',     'Perro',  'Labrador',          'M', '2020-03-15', 28.50, 1),
('Luna',    'Gato',   'Siamés',            'H', '2021-07-02',  4.20, 1),
('Rocky',   'Perro',  'Bulldog francés',   'M', '2019-11-20', 12.30, 2),
('Mía',     'Gato',   'Criollo',           'H', '2022-01-10',  3.80, 3),
('Toby',    'Perro',  'Beagle',            'M', '2018-05-05', 14.00, 4),
('Kiara',   'Perro',  'Pastor alemán',     'H', '2021-09-18', 30.10, 5),
('Piolín',  'Ave',    'Canario',           'M', '2023-02-14',  0.03, 6),
('Copito',  'Conejo', 'Cabeza de león',    'M', '2022-08-30',  1.60, 7),
('Nala',    'Gato',   'Persa',             'H', '2020-12-01',  4.90, 8),
('Bruno',   'Perro',  'Golden retriever',  'M', '2017-04-22', 32.00, 9),
('Spike',   'Reptil', 'Iguana verde',      'M', '2021-06-11',  2.40, 10),
('Lola',    'Perro',  'Pinscher',          'H', '2023-03-03',  3.10, 2);

INSERT INTO citas (fecha, hora, motivo, estado, observaciones, id_mascota, id_veterinario, id_servicio) VALUES
('2026-11-03', '08:00', 'Control anual',                    'Atendida',   'Mascota en buen estado general', 1, 1, 1),
('2026-11-03', '09:00', 'Refuerzo de vacuna triple felina', 'Atendida',   NULL,                              2, 1, 2),
('2026-11-05', '10:30', 'Picazón constante en el lomo',     'Atendida',   'Se formula champú medicado',      3, 3, 7),
('2026-11-10', '14:00', 'Esterilización programada',        'Atendida',   'Recuperación satisfactoria',      4, 2, 5),
('2026-11-12', '11:00', 'Sarro y mal aliento',              'Cancelada',  'El dueño canceló por viaje',      5, 4, 6),
('2026-11-18', '15:30', 'Cojea de la pata trasera',         'Atendida',   'Se toma radiografía',             6, 10, 9),
('2026-11-24', '08:30', 'Revisión de plumaje',              'Programada', NULL,                              7, 8, 1),
('2026-11-24', '09:30', 'Desparasitación trimestral',       'Programada', NULL,                              8, 6, 3),
('2026-11-25', '16:00', 'Baño y corte de pelo',             'Programada', NULL,                              9, 6, 4),
('2026-11-26', '10:00', 'Control de peso por sobrepeso',    'Programada', 'Traer historial de alimentación', 10, 9, 11),
('2026-11-27', '11:30', 'Revisión de escamas',              'Programada', NULL,                              11, 8, 1),
('2026-11-28', '08:00', 'Soplo cardíaco detectado',         'Programada', 'Se solicita ecografía',           1, 5, 8);
