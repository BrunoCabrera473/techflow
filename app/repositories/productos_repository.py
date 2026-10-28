"""Acceso a datos parametrizado para productos y variantes."""

# Importa el administrador de conexiones y cursores de la base de datos
from app.db import cursor_db


# =====================================================
# REPOSITORIO DE PRODUCTOS
# =====================================================

# Centraliza las operaciones de consulta y modificacion de productos, variantes y catalogos
class ProductosRepository:

    # Busca productos por nombre o descripcion y permite incluir productos inactivos si se solicita
    def listar_productos(
        self,
        busqueda='',
        incluir_inactivos=False
    ):
        sql = """
            SELECT
                p.id,
                p.nombre,
                p.descripcion,
                p.categoria_id,
                c.nombre AS categoria,
                p.precio,
                p.activo,
                p.creado_en,
                p.actualizado_en
            FROM productos p
            JOIN categorias c
                ON c.id = p.categoria_id
            WHERE (
                p.nombre LIKE %s
                OR COALESCE(p.descripcion, '') LIKE %s
            )
        """

        # Prepara los valores para buscar coincidencias parciales
        args = [
            f'%{busqueda}%',
            f'%{busqueda}%'
        ]

        # Si no se solicitan inactivos, muestra solo los activos
        if not incluir_inactivos:
            sql += " AND p.activo = TRUE"

        # Ordena los resultados por nombre e identificador
        sql += " ORDER BY p.nombre, p.id"

        # Ejecuta la consulta y devuelve todos los resultados
        with cursor_db() as (_, cur):
            cur.execute(sql, tuple(args))
            return cur.fetchall()

    # Busca un producto especifico por su identificador
    def obtener_producto(self, pid):
        with cursor_db() as (_, cur):
            cur.execute(
                """
                SELECT
                    p.id,
                    p.nombre,
                    p.descripcion,
                    p.categoria_id,
                    c.nombre AS categoria,
                    p.precio,
                    p.activo
                FROM productos p
                JOIN categorias c
                    ON c.id = p.categoria_id
                WHERE p.id = %s
                """,
                (pid,)
            )

            # Devuelve el producto encontrado o None
            return cur.fetchone()

    # Inserta un producto nuevo en la base de datos
    def crear_producto(self, d):
        with cursor_db() as (_, cur):
            cur.execute(
                """
                INSERT INTO productos (
                    nombre,
                    descripcion,
                    categoria_id,
                    precio,
                    activo
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    d['nombre'],
                    d.get('descripcion'),
                    d['categoria_id'],
                    d['precio'],
                    d.get('activo', True)
                )
            )

            # Devuelve el ID generado para el nuevo producto
            return cur.lastrowid

    # Actualiza los datos de un producto existente
    def modificar_producto(self, pid, d):
        with cursor_db() as (_, cur):
            cur.execute(
                """
                UPDATE productos
                SET
                    nombre = %s,
                    descripcion = %s,
                    categoria_id = %s,
                    precio = %s,
                    activo = %s
                WHERE id = %s
                """,
                (
                    d['nombre'],
                    d.get('descripcion'),
                    d['categoria_id'],
                    d['precio'],
                    d.get('activo', True),
                    pid
                )
            )

            # Devuelve True si alguna fila fue modificada
            return cur.rowcount > 0

    # Desactiva el producto sin eliminarlo de la base de datos
    def desactivar_producto(self, pid):
        with cursor_db() as (_, cur):
            cur.execute(
                """
                UPDATE productos
                SET activo = FALSE
                WHERE id = %s
                """,
                (pid,)
            )

            # Indica si se modifico algun registro
            return cur.rowcount > 0

    # Consulta categorias, talles o colores disponibles
    def listar_catalogo(self, tabla):

        # Acepta unicamente las tablas autorizadas.
        if tabla not in {'categorias', 'talles', 'colores'}:
            raise ValueError('Catalogo invalido')

        with cursor_db() as (_, cur):
            cur.execute(
                f"""
                SELECT id, nombre
                FROM {tabla}
                ORDER BY nombre
                """
            )

            # Devuelve todos los elementos del catalogo
            return cur.fetchall()

    # Agrega una categoria, un talle o un color
    def crear_catalogo(self, tabla, nombre):

        # Valida el nombre de la tabla antes de usarlo
        if tabla not in {'categorias', 'talles', 'colores'}:
            raise ValueError('Catalogo invalido')

        with cursor_db() as (_, cur):
            cur.execute(
                f"""
                INSERT INTO {tabla} (nombre)
                VALUES (%s)
                """,
                (nombre,)
            )

            # Devuelve el ID del elemento creado
            return cur.lastrowid

    # =================================================
    # GESTION DE VARIANTES
    # =================================================

    # Busca las variantes de un producto con sus talles, colores, codigos y cantidades de stock
    def listar_variantes(self, pid):
        with cursor_db() as (_, cur):
            cur.execute(
                """
                SELECT
                    v.id,
                    v.producto_id,
                    v.talle_id,
                    t.nombre AS talle,
                    v.color_id,
                    c.nombre AS color,
                    v.codigo,
                    v.stock_actual,
                    v.stock_minimo
                FROM variantes v
                JOIN talles t
                    ON t.id = v.talle_id
                JOIN colores c
                    ON c.id = v.color_id
                WHERE v.producto_id = %s
                ORDER BY t.nombre, c.nombre
                """,
                (pid,)
            )

            # Devuelve todas las variantes encontradas
            return cur.fetchall()

    # Crea una variante con talle, color, codigo y stock minimo inicial
    def crear_variante(self, d):

        # El stock actual lo administra exclusivamente el modulo de inventario; aqui comienza en cero
        with cursor_db() as (_, cur):
            cur.execute(
                """
                INSERT INTO variantes (
                    producto_id,
                    talle_id,
                    color_id,
                    codigo,
                    stock_minimo
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    d['producto_id'],
                    d['talle_id'],
                    d['color_id'],
                    d['codigo'],
                    d.get('stock_minimo', 0)
                )
            )

            # Devuelve el ID de la variante creada
            return cur.lastrowid

    # Actualiza el talle, el color, el codigo y el stock minimo de una variante
    def modificar_variante(self, vid, d):
        with cursor_db() as (_, cur):
            cur.execute(
                """
                UPDATE variantes
                SET
                    talle_id = %s,
                    color_id = %s,
                    codigo = %s,
                    stock_minimo = %s
                WHERE id = %s
                """,
                (
                    d['talle_id'],
                    d['color_id'],
                    d['codigo'],
                    d.get('stock_minimo', 0),
                    vid
                )
            )

            # Devuelve True si alguna fila fue modificada
            return cur.rowcount > 0