# Diccionario de datos (MySQL 8.0+)

`NOT NULL` indica obligatoriedad. Los IDs son autoincrementales.

| Campo | Tipo | Significado | Obligatorio | Restricciones |
|---|---|---|---|---|
| categorias.id | BIGINT UNSIGNED | ID de categoría | Sí | PK, autoincremental |
| categorias.nombre | VARCHAR(100) | Nombre de categoría | Sí | Único, no vacío |
| productos.id | BIGINT UNSIGNED | ID de producto | Sí | PK |
| productos.nombre | VARCHAR(150) | Nombre comercial | Sí | No vacío |
| productos.descripcion | TEXT | Descripción | No | NULL permitido |
| productos.categoria_id | BIGINT UNSIGNED | Categoría | Sí | FK a categorias, borrado restringido |
| productos.precio | DECIMAL(12,2) | Precio común a variantes | Sí | Mayor que cero; evitar FLOAT |
| productos.activo | BOOLEAN | Estado del producto | Sí | TRUE por defecto; desactivar conserva ventas |
| productos.creado_en | TIMESTAMP | Fecha de alta | Sí | Automático |
| productos.actualizado_en | TIMESTAMP | Última actualización | Sí | Automático al modificar |
| talles.id | BIGINT UNSIGNED | ID de talle | Sí | PK |
| talles.nombre | VARCHAR(40) | Talle | Sí | Único, no vacío |
| colores.id | BIGINT UNSIGNED | ID de color | Sí | PK |
| colores.nombre | VARCHAR(60) | Color | Sí | Único, no vacío |
| variantes.id | BIGINT UNSIGNED | ID de variante | Sí | PK |
| variantes.producto_id | BIGINT UNSIGNED | Producto padre | Sí | FK a productos |
| variantes.talle_id | BIGINT UNSIGNED | Talle asignado | Sí | FK a talles |
| variantes.color_id | BIGINT UNSIGNED | Color asignado | Sí | FK a colores |
| variantes.codigo | VARCHAR(80) | Código de variante | Sí | Único global, no vacío |
| variantes.stock_actual | INT UNSIGNED | Existencia | Sí | No negativo, default 0; solo inventario lo modifica |
| variantes.stock_minimo | INT UNSIGNED | Umbral de alerta | Sí | No negativo, default 0 |
| ventas.id | BIGINT UNSIGNED | ID de venta | Sí | PK |
| ventas.fecha_hora | DATETIME | Momento de venta | Sí | Default fecha/hora del servidor |
| ventas.total | DECIMAL(12,2) | Total histórico | Sí | No negativo |
| ventas.medio_pago | VARCHAR(30) | Medio de pago principal | Sí | No vacío; pagos mixtos pendientes de diseño específico |
| ventas.estado | ENUM | Estado | Sí | completada/anulada; default completada |
| ventas.motivo_anulacion | VARCHAR(255) | Motivo de anulación | No | NULL mientras no se anule |
| detalle_venta.id | BIGINT UNSIGNED | ID de línea | Sí | PK |
| detalle_venta.venta_id | BIGINT UNSIGNED | Venta relacionada | Sí | FK, borrado restringido |
| detalle_venta.variante_id | BIGINT UNSIGNED | Variante vendida | Sí | FK, borrado restringido |
| detalle_venta.cantidad | INT UNSIGNED | Unidades vendidas | Sí | Mayor que cero |
| detalle_venta.precio_unitario | DECIMAL(12,2) | Precio cobrado por unidad | Sí | No negativo; snapshot histórico |
| detalle_venta.subtotal | DECIMAL(12,2) | Total de línea | Sí | No negativo; cantidad × precio |
| movimientos_stock.id | BIGINT UNSIGNED | ID de movimiento | Sí | PK |
| movimientos_stock.variante_id | BIGINT UNSIGNED | Variante afectada | Sí | FK a variantes |
| movimientos_stock.tipo | ENUM | Tipo de movimiento | Sí | ingreso/egreso/ajuste/devolucion |
| movimientos_stock.cantidad | INT UNSIGNED | Magnitud del movimiento | Sí | Mayor que cero; tipo define el sentido |
| movimientos_stock.fecha_hora | DATETIME | Fecha/hora | Sí | Default servidor |
| movimientos_stock.motivo | VARCHAR(255) | Justificación | Sí | No vacío |
| movimientos_stock.venta_id | BIGINT UNSIGNED | Venta relacionada | No | FK nullable |

## Restricciones transversales
Unicidad de nombres de catálogos, código de variante y combinación producto/talle/color. Importes con `DECIMAL(12,2)`. Las FK preservan referencias históricas. Las validaciones del servidor complementan, pero no reemplazan, las restricciones de base de datos.
