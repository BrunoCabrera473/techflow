# Creacion, respaldo y restauracion

## Crear la base
1. Instalar MySQL 8.0+ y disponer de `mysql` y `mysqldump`.
2. En la raiz del proyecto, ejecutar `mysql -u root -p < sql/01_esquema.sql`.
3. Solo para una base recien creada, cargar ejemplos ficticios con `mysql -u root -p < sql/02_datos_demo.sql`.
4. Opcionalmente revisar `sql/03_usuario_aplicacion.sql`, reemplazar la contraseña de ejemplo y ejecutarlo como administrador.
5. Configurar `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` en las variables de entorno. `.env.example` es una plantilla, no se carga automaticamente.
6. Ejecutar `python -m pip install -r requirements.txt` y luego `python run.py`.

## Respaldo
```bash
mysqldump -u root -p --single-transaction --routines --triggers techflow > respaldo_techflow.sql
```

El parametro `-p` solicita la contraseña. Guardar los respaldos fuera de carpetas publicas, con acceso limitado y retencion definida.

## Restauracion y comprobacion
1. Restaurar primero en una base de prueba, no sobre produccion.
2. Verificar si el dump incluye `CREATE DATABASE` o `USE techflow`; si apunta al nombre original, editar una copia para la base de prueba.
3. Ejecutar `mysql -u root -p techflow_restore_test < respaldo_techflow.sql` si el dump no contiene una instruccion `USE` con otro nombre.
4. Comparar conteos del origen y restauracion: `SELECT COUNT(*) FROM productos;`, `variantes`, `ventas`, `detalle_venta` y `movimientos_stock`.
5. Verificar totales y referencias de ventas. Registrar archivo, fecha, operador y resultado.
