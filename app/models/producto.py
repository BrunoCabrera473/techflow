"""Entidades del dominio de productos."""

# Importa dataclass para generar automaticamente metodos como el constructor de cada clase
from dataclasses import dataclass

# Permite manejar precios con precision decimal
from decimal import Decimal

# Permite indicar que un atributo puede tener un valor del tipo especificado o ser None
from typing import Optional


# =====================================================
# CLASE PRODUCTO
# =====================================================

# Representa un producto dentro del sistema
@dataclass
class Producto:

    # Nombre del producto
    nombre: str

    # Identificador de la categoria a la que pertenece
    categoria_id: int

    # Precio del producto
    precio: Decimal

    # Descripcion opcional del producto
    descripcion: Optional[str] = None

    # Indica si el producto esta activo
    activo: bool = True

    # Identificador del producto, opcional
    id: Optional[int] = None


# =====================================================
# CLASE VARIANTE
# =====================================================

# Representa una variante de un producto segun su talle, color, codigo y disponibilidad de stock
@dataclass
class Variante:

    # Identificador del producto asociado
    producto_id: int

    # Identificador del talle de la variante
    talle_id: int

    # Identificador del color de la variante
    color_id: int

    # Codigo unico que identifica la variante
    codigo: str

    # Cantidad de unidades disponibles actualmente
    stock_actual: int = 0

    # Cantidad minima de stock establecida
    stock_minimo: int = 0

    # Identificador de la variante, opcional
    id: Optional[int] = None


# =====================================================
# CLASE CATALOGO
# =====================================================

# Representa un catalogo o una categoria de catalogo e identificada por su nombre
@dataclass
class Catalogo:

    # Nombre del catalogo
    nombre: str

    # Identificador del catalogo, opcional
    id: Optional[int] = None