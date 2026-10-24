"""Este archivo contiene el código principal para ejecutar la aplicación Flask.
 también define la ruta raíz ("/") que devuelve un mensaje de bienvenida."""

# importar la clase Flask desde el módulo flask
from flask import Flask, render_template

# crear una instancia de la aplicación Flask
app = Flask(__name__)

# definir la ruta raíz ("/") y la función que se ejecutará cuando se acceda a esa ruta
@app.get("/")
def inicio():
    """Prepara y devuelve la página de bienvenida."""
    return render_template("index.html")

if __name__ == "__main__": # ejecutar la aplicación Flask en el host y puerto especificados
    app.run(host="127.0.0.1", port=5000) # ejecutar la aplicación Flask en el host y puerto especificados

# Este archivo es el punto de entrada principal para ejecutar la aplicación Flask.