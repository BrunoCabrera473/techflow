"""
Punto de entrada de TechFlow.

Ejecutar este archivo y abrir http://127.0.0.1:5000.
Para detener el servidor, presionar Ctrl + C en la terminal.
"""

from app import create_app


# La construcción de la aplicación ahora está en el paquete app.
app = create_app()


if __name__ == "__main__":
    # Servidor de desarrollo accesible solo desde esta computadora.
    app.run(host="127.0.0.1", port=5000)