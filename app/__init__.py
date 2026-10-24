"""Construcción y configuración de la aplicación TechFlow."""

from pathlib import Path

from flask import Flask

from app.controllers.inicio_controller import inicio_bp


def create_app():
    """Crea la aplicación y registra sus controladores."""
    # Ubicamos la raíz del proyecto a partir de este archivo.
    # Así encontramos los recursos sin depender de dónde se ejecute.
    raiz = Path(__file__).resolve().parent.parent

    app = Flask(
        __name__,
        template_folder=str(raiz / "templates"),
        static_folder=str(raiz / "static"),
    )

    # Incorporamos las rutas del controlador de inicio.
    app.register_blueprint(inicio_bp)

    return app