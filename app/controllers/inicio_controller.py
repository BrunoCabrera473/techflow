"""Controlador de la bienvenida y del estado básico del servidor."""

from flask import Blueprint, jsonify, render_template


inicio_bp = Blueprint("inicio", __name__)


@inicio_bp.get("/")
def mostrar_inicio():
    """Devuelve la pantalla de bienvenida."""
    return render_template("index.html")


@inicio_bp.get("/api/estado")
def consultar_estado():
    """Confirma que el servidor responde; no comprueba MySQL."""
    return jsonify({
        "estado": "ok",
        "mensaje": "El servidor de TechFlow está funcionando."
    })