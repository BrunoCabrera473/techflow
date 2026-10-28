USE techflow;


-- =====================================================
-- INSERTAR CATEGORIAS
-- =====================================================

-- Carga las categorias disponibles para clasificar productos
INSERT INTO categorias (nombre)
VALUES
    ('Remeras'),
    ('Pantalones'),
    ('Abrigos');


-- =====================================================
-- INSERTAR TALLES
-- =====================================================

-- Registra los talles disponibles para las variantes
INSERT INTO talles (nombre)
VALUES
    ('XS'),
    ('S'),
    ('M'),
    ('L'),
    ('XL');


-- =====================================================
-- INSERTAR COLORES
-- =====================================================

-- Guarda los colores disponibles para los productos
INSERT INTO colores (nombre)
VALUES
    ('Negro'),
    ('Blanco'),
    ('Azul');


-- =====================================================
-- INSERTAR PRODUCTOS
-- =====================================================

-- Carga productos de ejemplo con su descripcion, categoria, precio y estado de disponibilidad
INSERT INTO productos (
    nombre,
    descripcion,
    categoria_id,
    precio,
    activo
)
VALUES
    (
        'Remera basica',
        'Ejemplo academico.',
        1,
        15000.00,
        TRUE
    ),
    (
        'Jean recto',
        'Ejemplo academico.',
        2,
        32000.00,
        TRUE
    ),
    (
        'Buzo liviano',
        'Ejemplo academico.',
        3,
        28000.00,
        FALSE
    );


-- =====================================================
-- INSERTAR VARIANTES
-- =====================================================

-- Registra combinaciones de productos, talles y colores, junto con sus codigos y cantidades de stock
INSERT INTO variantes (
    producto_id,
    talle_id,
    color_id,
    codigo,
    stock_actual,
    stock_minimo
)
VALUES
    (1, 3, 1, 'REM-BAS-M-NEG', 12, 3),
    (1, 4, 2, 'REM-BAS-L-BLA', 8, 2),
    (2, 3, 3, 'JEA-REC-M-AZU', 5, 2);


-- =====================================================
-- REGISTRAR UNA VENTA
-- =====================================================

-- Registra una venta de ejemplo con fecha, importe total y medio de pago utilizado
INSERT INTO ventas (
    fecha_hora,
    total,
    medio_pago
)
VALUES (
    '2026-01-15 14:30:00',
    30000.00,
    'efectivo'
);


-- =====================================================
-- INSERTAR EL DETALLE DE LA VENTA
-- =====================================================

-- Indica que variante se vendio, la cantidad, el precio unitario y el subtotal correspondiente
INSERT INTO detalle_venta (
    venta_id,
    variante_id,
    cantidad,
    precio_unitario,
    subtotal
)
VALUES (
    1,
    1,
    2,
    15000.00,
    30000.00
);


-- =====================================================
-- REGISTRAR MOVIMIENTOS DE STOCK
-- =====================================================

-- Guarda los movimientos de entrada y salida de stock, incluyendo el motivo y la venta relacionada
INSERT INTO movimientos_stock (
    variante_id,
    tipo,
    cantidad,
    fecha_hora,
    motivo,
    venta_id
)
VALUES
    (
        1,
        'ingreso',
        14,
        '2026-01-10 09:00:00',
        'Carga inicial ficticia',
        NULL
    ),
    (
        1,
        'egreso',
        2,
        '2026-01-15 14:30:00',
        'Venta de demostracion',
        1
    );