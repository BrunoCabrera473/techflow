"""Controlador de la pantalla principal."""

from flask import Blueprint, render_template


# Un Blueprint agrupa rutas para poder organizarlas por módulo.
inicio_bp = Blueprint("inicio", __name__)


@inicio_bp.get("/")
def mostrar_inicio():
    """Devuelve la pantalla de bienvenida."""
    return render_template("index.html")