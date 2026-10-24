"""Este archivo contiene el código principal para ejecutar la aplicación Flask.
 también define la ruta raíz ("/") que devuelve un mensaje de bienvenida."""

# importar la clase Flask desde el módulo flask
from flask import Flask

# crear una instancia de la aplicación Flask
app = Flask(__name__)

# definir la ruta raíz ("/") y la función que se ejecutará cuando se acceda a esa ruta
@app.get("/") # Ruta raíz
def inicio(): # función que se ejecuta cuando se accede a la ruta raíz
    return "<h1>TechFlow Solutions</h1><p>La aplicación está funcionando.</p>" # mensaje de bienvenida que se devuelve al acceder a la ruta raíz

if __name__ == "__main__": # ejecutar la aplicación Flask en el host y puerto especificados
    app.run(host="127.0.0.1", port=5000) # ejecutar la aplicación Flask en el host y puerto especificados

# Este archivo es el punto de entrada principal para ejecutar la aplicación Flask.