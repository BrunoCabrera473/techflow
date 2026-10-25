# Acuerdos técnicos de TechFlow

Estado: propuesta de Ezequiel para revisar con el equipo. No es un contrato aprobado ni implica que los módulos estén implementados.

## 1. Qué funciona hoy

- `GET /`: muestra la bienvenida.
- `GET /api/estado`: informa que el servidor responde. No comprueba MySQL.
- El botón de la bienvenida consulta esa ruta con JavaScript y muestra éxito o error.

Respuesta actual de `/api/estado` (se conserva para no romper el botón):

```json
{"estado":"ok","mensaje":"El servidor de TechFlow está funcionando."}
```

## 2. Alcance de la primera versión

Una tienda, una computadora y un operador. Aplicación local en Python/Flask, interfaz HTML/CSS/JavaScript y futura BD MySQL local. Cada instalación tendrá datos independientes.

Incluye productos y variantes por talle/color, stock, carrito, pagos mixtos registrados, caja, historial, proveedores y estadísticas. Los contactos y enlaces externos requieren internet; las operaciones locales no deberían necesitarlo.

Quedan fuera: cobros integrados con bancos, facturación fiscal, múltiples usuarios, sincronización entre computadoras y comercio electrónico. Un comprobante interno no es una factura fiscal.

## 3. Responsables y coordinación

| Responsable | Aporte | Coordina con |
|---|---|---|
| Ezequiel | Servidor, configuración, integración y acuerdos de API | Todos |
| Maximiliano | Modelo relacional, productos, variantes y proveedores | Bruno para transacciones; Andrés para reportes |
| Bruno | Inventario, ventas, pagos y caja | Maximiliano y Abel |
| Abel | Pantallas, estilos y llamadas JavaScript | Autores de cada API |
| Andrés | Consultas, estadísticas y gráficos | Maximiliano y Abel |

Cada cambio de campos, tablas o respuestas debe revisarse con quien lo consume antes de integrarlo. Una tarea terminada incluye prueba y documentación.

## 4. Cómo se comunican las partes

Ejemplo futuro: el usuario guarda una prenda → JavaScript envía JSON → el controlador recibe la petición → el servicio valida reglas → el repositorio consulta MySQL → Python devuelve JSON → la pantalla informa el resultado.

- `controllers`: reciben peticiones y seleccionan la respuesta HTTP.
- `services`: coordinan reglas y operaciones del negocio.
- `models`: clases que representan entidades del dominio.
- `repositories`: consultas parametrizadas y persistencia.
- `templates`: vistas HTML; `static`: CSS, JavaScript e imágenes.

La interfaz nunca recibe la contraseña de MySQL ni se conecta directamente a la BD. Crear carpetas no demuestra por sí solo POO/MVC: se documentará un recorrido real cuando exista un módulo completo.

## 5. Convenciones propuestas

- Rutas bajo `/api`, nombres en español sin tildes y campos en `snake_case`.
- GET consulta; POST crea o registra una operación; PATCH modifica campos.
- Peticiones con cuerpo: `Content-Type: application/json`.
- Identificadores: enteros positivos asignados por el servidor.
- Importes en JSON: texto decimal con dos decimales, por ejemplo `"15000.00"`. Python usará Decimal y MySQL DECIMAL; no usar flotantes como fuente de verdad del dinero.
- Cantidades de prendas: enteros positivos. Para un ajuste se usa una diferencia entera distinta de cero, que puede ser negativa.
- Fechas de filtro: `AAAA-MM-DD`. Acordar zona America/Argentina/Buenos_Aires para agrupar ventas. Los instantes se devuelven en ISO 8601 con desplazamiento horario.
- Un filtro `desde`/`hasta` incluye ambos días locales. Rechazar rangos invertidos.
- Listados: `pagina` (por defecto 1), `limite` (por defecto 20, máximo 100).
- El servidor valida siempre y calcula precios, totales y stock. La validación del navegador ayuda al usuario, pero no la reemplaza.
- Consultas SQL parametrizadas. No incluir trazas internas o credenciales en respuestas.

Para los módulos futuros, respuesta de éxito:

```json
{"datos":{"id":1,"nombre":"Remera básica"}}
```

Listado:

```json
{"datos":[],"paginacion":{"pagina":1,"limite":20,"total":0}}
```

Error:

```json
{"error":{"codigo":"VALIDACION","mensaje":"Revisá los datos ingresados.","campos":{"nombre":"Es obligatorio."}}}
```

| Estado HTTP | Uso |
|---|---|
| 200 | Consulta o modificación correcta |
| 201 | Recurso creado |
| 400 | Datos o JSON inválidos |
| 404 | Recurso inexistente |
| 409 | Conflicto: falta de stock, caja cerrada u operación repetida incompatible |
| 500 | Error interno inesperado, con mensaje público genérico |
| 503 | Dependencia temporalmente no disponible, como MySQL |

## 6. Rutas propuestas: todavía no implementadas

Los nombres `{id}` y `{variante_id}` representan identificadores reales.

| Método y ruta | Operación | Responsable |
|---|---|---|
| GET /api/productos | Listar; filtrar por `busqueda` y `activo` | Maximiliano |
| POST /api/productos | Crear producto | Maximiliano |
| GET /api/productos/{id} | Consultar producto | Maximiliano |
| PATCH /api/productos/{id} | Editar o desactivar con `activo: false` | Maximiliano |
| GET /api/productos/{id}/variantes | Listar talles/colores | Maximiliano |
| POST /api/productos/{id}/variantes | Crear variante | Maximiliano |
| PATCH /api/variantes/{id} | Editar datos o desactivar; no cambiar stock aquí | Maximiliano |
| GET /api/proveedores | Listar contactos | Maximiliano |
| POST /api/proveedores | Crear contacto | Maximiliano |
| PATCH /api/proveedores/{id} | Editar contacto | Maximiliano |
| GET /api/inventario | Consultar existencias por variante | Bruno |
| POST /api/inventario/ingresos | Registrar entrada positiva con motivo | Bruno |
| POST /api/inventario/ajustes | Registrar diferencia y motivo obligatorio | Bruno |
| GET /api/caja/actual | Consultar sesión abierta; `datos: null` si no existe | Bruno |
| POST /api/caja/aperturas | Abrir caja con saldo inicial | Bruno |
| POST /api/caja/{id}/cierres | Registrar efectivo contado y calcular diferencia | Bruno |
| POST /api/ventas | Confirmar carrito, pagos y descuento de stock | Bruno |
| GET /api/ventas | Listar ventas por período y estado | Bruno |
| GET /api/ventas/{id} | Ver detalle y pagos | Bruno |
| POST /api/ventas/{id}/anulacion | Anular una vez, con motivo | Bruno |
| GET /api/estadisticas/resumen | Ventas y promedios por período | Andrés |
| GET /api/estadisticas/productos | Ranking de unidades vendidas | Andrés |
| GET /api/estadisticas/ventas-por-dia | Serie por fecha | Andrés |

Abel conecta las pantallas con estas rutas; Andrés y Abel acuerdan cómo mostrar gráficos. Las rutas de análisis restantes y cualquier exportación se documentarán antes de implementarlas. No usar datos ficticios como si fueran una conexión real.

## 7. Primer ejemplo: crear un producto

Propuesta de cuerpo para `POST /api/productos`:

```json
{"nombre":"Remera básica","categoria_id":1,"precio":"15000.00","proveedor_id":1}
```

Validar nombre no vacío, precio mayor que cero y referencias existentes. Si el proveedor es opcional, se enviará `null`. Acordar con Maximiliano cómo se cargan las categorías antes de desarrollar el formulario.

Crear producto no crea stock. Después se crea una variante con talle/color y se registra un ingreso. Propuesta inicial: precio común por producto; confirmar si la consigna requiere precio por variante.

## 8. Segundo ejemplo: confirmar una venta

Propuesta para `POST /api/ventas`:

```json
{
  "solicitud_id":"a1bbcf82-3781-4d14-9014-aac179902d08",
  "caja_id":1,
  "items":[{"variante_id":1,"cantidad":2}],
  "pagos":[
    {"medio":"efectivo","importe":"10000.00"},
    {"medio":"transferencia","importe":"20000.00"}
  ],
  "efectivo_recibido":"10000.00"
}
```

Para este ejemplo el servidor encuentra un precio de 15000.00 por unidad, calcula total 30000.00 y verifica que los pagos aplicados sumen ese total. No acepta un total arbitrario del navegador. Los medios iniciales propuestos son efectivo, transferencia y tarjeta; solo se registran, no se procesan cobros externos.

Si se entregan 15000.00 en efectivo para aplicar 10000.00, el cambio es 5000.00. No confundir el efectivo recibido con el importe aplicado al pago.

Venta, detalles, pagos y movimientos se guardan en una sola transacción. Ante cualquier falla se revierte todo. El precio unitario vendido se conserva en el detalle aunque cambie el precio actual.

`solicitud_id` se genera una vez por intento de venta y se reutiliza al reintentar después de un fallo de red. Mismo identificador y mismo contenido devuelven la venta ya creada; mismo identificador con datos distintos da 409. El control debe existir en el servidor, además de deshabilitar el botón.

## 9. Reglas que requieren acuerdo del equipo

- Stock: nunca negativo; movimientos con fecha y motivo.
- Caja: una sola sesión abierta. Separar ventas totales de efectivo esperado.
- Productos con historial: desactivar, no borrar físicamente.
- Anulaciones: conservar venta y motivo; revertir una sola vez. Propuesta inicial: solo anular si la caja original sigue abierta. Definir devoluciones posteriores antes de permitirlas.
- Estadísticas: excluir ventas anuladas según regla documentada; evitar división por cero; aclarar si se cuentan días abiertos o calendario.
- Tendencia: comparación entre períodos equivalentes de esta tienda, no una afirmación sobre la moda general.
- SQL y UML: Maximiliano propone y los autores de módulos revisan; este documento no sustituye el diseño de BD.

## 10. Orden de construcción y revisión

1. Revisar este borrador entre los cinco y registrar decisiones pendientes.
2. Definir tablas y categorías con Maximiliano.
3. Preparar conexión local a MySQL y manejo de errores.
4. Implementar crear/listar productos y su primera pantalla.
5. Incorporar variantes e inventario.
6. Integrar caja, carrito, venta y pagos mixtos.
7. Construir estadísticas sobre ventas verificadas.
8. Probar instalación, respaldo y recorrido completo.

Para cada ruta: probar un caso correcto, datos inválidos y recurso inexistente cuando corresponda. Para ventas: falta de stock, pagos incompletos, repetición y reversión de transacción.

Estado de revisión: pendiente de los cinco integrantes. Las nuevas rutas, campos y reglas siguen siendo propuestas hasta esa revisión.
