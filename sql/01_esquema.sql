-- =====================================================
-- CREACION DE LA BASE DE DATOS
-- =====================================================

-- esto crea la base de datos y configura la codificacion para permitir caracteres especiales y distintos idiomas
CREATE DATABASE IF NOT EXISTS techflow
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

-- Selecciona la base de datos que va utilizar
USE techflow;


-- =====================================================
-- TABLA CATEGORIAS
-- =====================================================

-- Almacena las categorias disponibles para los productos
CREATE TABLE categorias (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,

    -- Evita que el nombre este vacio o tenga solo espacios
    CONSTRAINT chk_categorias_nombre
        CHECK (CHAR_LENGTH(TRIM(nombre)) > 0)
) ENGINE=InnoDB;


-- =====================================================
-- TABLA PRODUCTOS
-- =====================================================

-- Guarda la informacion general de cada producto
CREATE TABLE productos (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT NULL,
    categoria_id BIGINT UNSIGNED NOT NULL,
    precio DECIMAL(12,2) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,

    -- Registra automaticamente las fechas de creacion y de la ultima actualizacion
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    -- esto son indices para agilizar las busquedas
    KEY ix_productos_categoria (categoria_id),
    KEY ix_productos_nombre (nombre),

    -- Relaciona cada producto con una categoria existente
    CONSTRAINT fk_productos_categoria
        FOREIGN KEY (categoria_id)
        REFERENCES categorias(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Valida que el nombre no este vacio
    CONSTRAINT chk_productos_nombre
        CHECK (CHAR_LENGTH(TRIM(nombre)) > 0),

    -- El precio debe ser mayor que cero
    CONSTRAINT chk_productos_precio
        CHECK (precio > 0)
) ENGINE=InnoDB;


-- =====================================================
-- TABLA TALLES
-- =====================================================

-- Almacena los talles disponibles para las variantes
CREATE TABLE talles (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL UNIQUE,

    -- Impide guardar nombres vacios
    CONSTRAINT chk_talles_nombre
        CHECK (CHAR_LENGTH(TRIM(nombre)) > 0)
) ENGINE=InnoDB;


-- =====================================================
-- TABLA COLORES
-- =====================================================

-- Guarda los colores disponibles para los productos
CREATE TABLE colores (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL UNIQUE,

    -- Impide guardar nombres vacíos.
    CONSTRAINT chk_colores_nombre
        CHECK (CHAR_LENGTH(TRIM(nombre)) > 0)
) ENGINE=InnoDB;


-- =====================================================
-- TABLA VARIANTES
-- =====================================================

-- Define las variantes de cada producto segun su talle y color, incluyendo su codigo y control de stock
CREATE TABLE variantes (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    producto_id BIGINT UNSIGNED NOT NULL,
    talle_id BIGINT UNSIGNED NOT NULL,
    color_id BIGINT UNSIGNED NOT NULL,
    codigo VARCHAR(80) NOT NULL,
    stock_actual INT UNSIGNED NOT NULL DEFAULT 0,
    stock_minimo INT UNSIGNED NOT NULL DEFAULT 0,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Evita repetir la misma combinacion de producto, talle y color
    UNIQUE KEY uq_variantes_producto_talle_color (
        producto_id,
        talle_id,
        color_id
    ),

    -- Cada variante debe tener un codigo unico
    UNIQUE KEY uq_variantes_codigo (codigo),

    -- indice para buscar variantes por producto
    KEY ix_variantes_producto (producto_id),

    -- El codigo no puede estar vacio
    CONSTRAINT chk_variantes_codigo
        CHECK (CHAR_LENGTH(TRIM(codigo)) > 0),

    -- Relacion con la tabla de productos
    CONSTRAINT fk_variantes_producto
        FOREIGN KEY (producto_id)
        REFERENCES productos(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Relacion con la tabla de talles
    CONSTRAINT fk_variantes_talle
        FOREIGN KEY (talle_id)
        REFERENCES talles(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Relacion con la tabla de colores
    CONSTRAINT fk_variantes_color
        FOREIGN KEY (color_id)
        REFERENCES colores(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;


-- =====================================================
-- TABLA VENTAS
-- =====================================================

-- Registra las ventas realizadas y su estado
CREATE TABLE ventas (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(12,2) NOT NULL,
    medio_pago VARCHAR(30) NOT NULL,

    -- La venta puede estar completada o anulada
    estado ENUM('completada', 'anulada')
        NOT NULL DEFAULT 'completada',

    -- Guarda el motivo cuando se anula una venta
    motivo_anulacion VARCHAR(255) NULL,

    -- indice para consultar ventas por fecha
    KEY ix_ventas_fecha (fecha_hora),

    -- El total no puede ser negativo
    CONSTRAINT chk_ventas_total
        CHECK (total >= 0),

    -- El medio de pago no puede estar vacio
    CONSTRAINT chk_ventas_medio
        CHECK (CHAR_LENGTH(TRIM(medio_pago)) > 0)
) ENGINE=InnoDB;


-- =====================================================
-- TABLA DETALLE DE VENTA
-- =====================================================

-- Guarda los productos vendidos, sus cantidades, precios unitarios y subtotales de cada venta
CREATE TABLE detalle_venta (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    venta_id BIGINT UNSIGNED NOT NULL,
    variante_id BIGINT UNSIGNED NOT NULL,
    cantidad INT UNSIGNED NOT NULL,
    precio_unitario DECIMAL(12,2) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,

    -- indices para buscar detalles por venta o variante
    KEY ix_detalle_venta_venta (venta_id),
    KEY ix_detalle_venta_variante (variante_id),

    -- Relaciona el detalle con una venta
    CONSTRAINT fk_detalle_venta_venta
        FOREIGN KEY (venta_id)
        REFERENCES ventas(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Relaciona el detalle con una variante vendida
    CONSTRAINT fk_detalle_venta_variante
        FOREIGN KEY (variante_id)
        REFERENCES variantes(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- La cantidad debe ser mayor que cero
    CONSTRAINT chk_detalle_cantidad
        CHECK (cantidad > 0),

    -- El precio unitario no puede ser negativo
    CONSTRAINT chk_detalle_precio
        CHECK (precio_unitario >= 0),

    -- El subtotal no puede ser negativo
    CONSTRAINT chk_detalle_subtotal
        CHECK (subtotal >= 0)
) ENGINE=InnoDB;


-- =====================================================
-- TABLA MOVIMIENTOS DE STOCK
-- =====================================================

-- Registra los ingresos, egresos, ajustes y devoluciones para llevar un historial de los cambios de inventario.
CREATE TABLE movimientos_stock (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    variante_id BIGINT UNSIGNED NOT NULL,

    -- indica el tipo de movimiento realizado
    tipo ENUM('ingreso', 'egreso', 'ajuste', 'devolucion')
        NOT NULL,

    cantidad INT UNSIGNED NOT NULL,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    motivo VARCHAR(255) NOT NULL,
    venta_id BIGINT UNSIGNED NULL,

    -- indices para consultar movimientos por variante, fecha o venta relacionada
    KEY ix_movimientos_variante_fecha (
        variante_id,
        fecha_hora
    ),
    KEY ix_movimientos_venta (venta_id),

    -- Relaciona el movimiento con una variante
    CONSTRAINT fk_movimientos_variante
        FOREIGN KEY (variante_id)
        REFERENCES variantes(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Permite vincular el movimiento con una venta puede quedar vacio si no corresponde a una venta
    CONSTRAINT fk_movimientos_venta
        FOREIGN KEY (venta_id)
        REFERENCES ventas(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- La cantidad del movimiento debe ser mayor que cero
    CONSTRAINT chk_movimientos_cantidad
        CHECK (cantidad > 0),

    -- El motivo no puede estar vacio.
    CONSTRAINT chk_movimientos_motivo
        CHECK (CHAR_LENGTH(TRIM(motivo)) > 0)
) ENGINE=InnoDB;