"""Rutas HTTP del modulo de productos y variantes."""

# Importa las herramientas de Flask para crear rutas, devolver respuestas JSON y recibir solicitudes HTTP
from flask import Blueprint, jsonify, request

# Intenta importar los errores de MySQL. Si el conector no esta instalado, define una clase alternativa
try:
    from mysql.connector import Error as MySQLError

except ImportError:
    class MySQLError(Exception):
        errno = None


# Importa el servicio y los errores de validacion
from app.services.productos_service import (
    ProductosService,
    ErrorValidacion
)


# =====================================================
# CONFIGURACION DEL MODULO
# =====================================================

# Crea el grupo de rutas con el prefijo /api
productos_bp = Blueprint(
    'productos',
    __name__,
    url_prefix='/api'
)

# Inicializa el servicio que contiene la logica del modulo
service = ProductosService()


# =====================================================
# MANEJO DE ERRORES
# =====================================================

# Devuelve un error HTTP 400 cuando los datos no son validos
@productos_bp.errorhandler(ErrorValidacion)
def err_validacion(e):
    return jsonify({
        'error': str(e)
    }), 400


# Maneja errores de la base de datos. Devuelve 409 para conflictos de datos y 503 para otros errores
@productos_bp.errorhandler(MySQLError)
def err_db(e):
    return jsonify({
        'error': (
            'No se pudo completar la operacion en la base '
            'de datos. Revisa duplicados, referencias y conexion.'
        )
    }), (
        409
        if getattr(e, 'errno', None) in (1062, 1451, 1452)
        else 503
    )


# =====================================================
# RUTAS DE PRODUCTOS
# =====================================================

# GET /api/productos Lista los productos y permite filtrar por busqueda e incluir productos inactivos
@productos_bp.get('/productos')
def listar():
    return jsonify({
        'datos': service.listar(
            request.args.get('q', '').strip(),
            request.args.get(
                'incluir_inactivos',
                ''
            ).lower() in ('1', 'true', 'si')
        )
    })


# POST /api/productos Crea un producto y devuelve su identificador
@productos_bp.post('/productos')
def crear():
    return jsonify({
        'id': service.crear(
            request.get_json(silent=True)
        ),
        'mensaje': 'Producto creado.'
    }), 201


# GET /api/productos/<pid> Busca un producto por su identificador
@productos_bp.get('/productos/<int:pid>')
def obtener(pid):
    # Consulta el producto mediante el repositorio
    p = service.repo.obtener_producto(pid)

    # Devuelve el producto o un error 404 si no existe
    return (
        (jsonify({'datos': p}), 200)
        if p
        else (
            jsonify({
                'error': 'Producto no encontrado.'
            }),
            404
        )
    )


# PATCH /api/productos/<pid> Modifica los datos de un producto existente
@productos_bp.patch('/productos/<int:pid>')
def modificar(pid):
    return (
        (
            jsonify({
                'mensaje': 'Producto modificado.'
            }),
            200
        )
        if service.modificar(
            pid,
            request.get_json(silent=True)
        )
        else (
            jsonify({
                'error': 'Producto no encontrado.'
            }),
            404
        )
    )


# POST /api/productos/<pid>/desactivacion Desactiva un producto sin eliminar su historial
@productos_bp.post('/productos/<int:pid>/desactivacion')
def desactivar(pid):
    return (
        (
            jsonify({
                'mensaje': (
                    'Producto desactivado; '
                    'se conserva el historial.'
                )
            }),
            200
        )
        if service.desactivar(pid)
        else (
            jsonify({
                'error': 'Producto no encontrado.'
            }),
            404
        )
    )


# =====================================================
# RUTAS DE CATALOGOS
# =====================================================

# GET /api/<tabla> Lista categorias, talles o colores
@productos_bp.get('/<string:tabla>')
def listar_catalogo(tabla):

    # Solo permite consultar los catalogos autorizados
    if tabla not in ('categorias', 'talles', 'colores'):
        return jsonify({
            'error': 'Catalogo no encontrado.'
        }), 404

    # Devuelve los elementos del catalogo seleccionado
    return jsonify({
        'datos': service.catalogo(tabla)
    })


# POST /api/<tabla> Crea una categoria, un talle o un color
@productos_bp.post('/<string:tabla>')
def crear_catalogo(tabla):

    # Comprueba que el catalogo sea valido
    if tabla not in ('categorias', 'talles', 'colores'):
        return jsonify({
            'error': 'Catalogo no encontrado.'
        }), 404

    # Valida los datos y crea el elemento
    return jsonify({
        'id': service.crear_catalogo(
            tabla,
            request.get_json(silent=True)
        ),
        'mensaje': 'Elemento creado.'
    }), 201


# =====================================================
# RUTAS DE VARIANTES
# =====================================================

# GET /api/productos/<pid>/variantes Lista las variantes asociadas a un producto
@productos_bp.get('/productos/<int:pid>/variantes')
def listar_variantes(pid):
    return jsonify({
        'datos': service.variantes(pid)
    })


# POST /api/productos/<pid>/variantes Crea una variante asociada al producto indicado
@productos_bp.post('/productos/<int:pid>/variantes')
def crear_variante(pid):

    # Obtiene los datos enviados en formato JSON.
    d = request.get_json(silent=True)

    # Asigna el ID del producto recibido en la URL.
    if isinstance(d, dict):
        d['producto_id'] = pid

    # Crea la variante con stock inicial en cero.
    return jsonify({
        'id': service.crear_variante(d),
        'mensaje': 'Variante creada con stock inicial cero.'
    }), 201


# PATCH /api/variantes/<vid> Modifica una variante sin alterar su stock actual
@productos_bp.patch('/variantes/<int:vid>')
def modificar_variante(vid):
    return (
        (
            jsonify({
                'mensaje': (
                    'Variante modificada; '
                    'el stock actual no se altera.'
                )
            }),
            200
        )
        if service.modificar_variante(
            vid,
            request.get_json(silent=True)
        )
        else (
            jsonify({
                'error': 'Variante no encontrada.'
            }),
            404
        )
    )