DROP DATABASE IF EXISTS sistema_inmobiliario;
CREATE DATABASE sistema_inmobiliario;
USE sistema_inmobiliario;

-- ROLES
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

-- USUARIOS
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    activo BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    password VARCHAR(255) NOT NULL,
    rol_id INT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- ETAPAS
CREATE TABLE etapas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- LOTES
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

-- COMPRAS
CREATE TABLE compras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NULL,
    total DECIMAL(12,2) NOT NULL,
    pendiente DECIMAL(12,2) NULL,
    estado ENUM('Activa','Pagada','Cancelada') DEFAULT 'Activa',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- DETALLE COMPRA
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

-- PAGOS
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

-- PQRS
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