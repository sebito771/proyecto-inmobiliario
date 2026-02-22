DROP DATABASE IF EXISTS sistema_inmobiliario;
CREATE DATABASE sistema_inmobiliario;
USE sistema_inmobiliario;

-- =========================
-- ROLES
-- =========================
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO roles (nombre) VALUES 
('Administrador'),
('Cliente');

-- =========================
-- USUARIOS
-- =========================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, -- preparado para bcrypt
    rol_id INT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

INSERT INTO usuarios (nombre, email, password, rol_id) VALUES
('Admin Sistema', 'admin@inmobiliaria.com', 'hash_admin', 1),
('Juan Perez', 'juan@email.com', 'hash_juan', 2),
('Maria Lopez', 'maria@email.com', 'hash_maria', 2);

-- =========================
-- ETAPAS
-- =========================
CREATE TABLE etapas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

INSERT INTO etapas (nombre, descripcion) VALUES
('Lanzamiento','Inicio oficial del proyecto'),
('Preventa','Venta anticipada de lotes'),
('Construccion','Etapa de construcción'),
('Entrega','Entrega formal al propietario');

-- =========================
-- LOTES
-- =========================
CREATE TABLE lotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    area_m2 INT NOT NULL CHECK (area_m2 BETWEEN 100 AND 200),
    ubicacion VARCHAR(150) NOT NULL,
    valor DECIMAL(12,2) NOT NULL,
    estado ENUM('Disponible','Reservado','Vendido') DEFAULT 'Disponible',
    etapa_id INT NOT NULL,
    FOREIGN KEY (etapa_id) REFERENCES etapas(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

INSERT INTO lotes (area_m2, ubicacion, valor, etapa_id) VALUES
(120,'Sector Norte',45000000,1),
(150,'Sector Sur',60000000,2),
(180,'Sector Este',75000000,3),
(200,'Sector Oeste',90000000,4);

-- =========================
-- COMPRAS
-- =========================
CREATE TABLE compras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(12,2) NOT NULL,
    estado ENUM('Activa','Pagada','Cancelada') DEFAULT 'Activa',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO compras (usuario_id, total) VALUES
(2,45000000),
(3,60000000);

-- =========================
-- DETALLE COMPRA
-- =========================
CREATE TABLE detalle_compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    compra_id INT NOT NULL,
    lote_id INT NOT NULL,
    precio DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (compra_id) REFERENCES compras(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (lote_id) REFERENCES lotes(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

INSERT INTO detalle_compra (compra_id, lote_id, precio) VALUES
(1,1,45000000),
(2,2,60000000);

UPDATE lotes SET estado='Vendido' WHERE id IN (1,2);

-- =========================
-- PAGOS
-- =========================
CREATE TABLE pagos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    compra_id INT NOT NULL,
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_pagado DECIMAL(12,2) NOT NULL,
    comprobante VARCHAR(255),
    FOREIGN KEY (compra_id) REFERENCES compras(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO pagos (compra_id, valor_pagado, comprobante) VALUES
(1,10000000,'pago1.pdf'),
(1,15000000,'pago2.pdf'),
(2,20000000,'pago3.pdf');

-- =========================
-- PQRS
-- =========================
CREATE TABLE pqrs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tipo ENUM('Peticion','Queja','Reclamo','Sugerencia') NOT NULL,
    descripcion TEXT NOT NULL,
    estado ENUM('Pendiente','En proceso','Cerrado') DEFAULT 'Pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO pqrs (usuario_id, tipo, descripcion) VALUES
(2,'Peticion','Solicito informacion sobre mi saldo'),
(3,'Queja','No he recibido mi comprobante');


	