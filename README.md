# TechFlow Solutions

Proyecto académico de un sistema de gestión para tiendas de ropa.

## Estado actual

Ya funciona una pantalla de bienvenida local desarrollada con
Python y Flask, con el HTML y el CSS separados.

Todavía no están implementados la conexión a MySQL ni los módulos
de productos, inventario, ventas, caja, proveedores y estadísticas.

## Tecnologías

- Python y Flask: servidor local.
- HTML y CSS: contenido y diseño de las pantallas.
- JavaScript: interacciones de la interfaz, por incorporar.
- MySQL: base de datos, pendiente de conectar.

## Cómo ejecutar el proyecto

### Primera vez

1. Instalar Python, GitHub Desktop y Visual Studio Code.
   La versión inicial fue probada con Python 3.10.9.
2. Clonar este repositorio con GitHub Desktop.
3. Abrir la carpeta del proyecto en VS Code.
4. Abrir Terminal → New Terminal y ejecutar, uno por uno:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

5. En VS Code, usar Python: Select Interpreter y seleccionar
   `.venv\Scripts\python.exe`.

### Iniciar la aplicación

Abrir `run.py` y presionar Run Python File en VS Code.

También se puede ejecutar desde la terminal:

```powershell
.\.venv\Scripts\python.exe run.py
```

Con el servidor encendido, abrir:

http://127.0.0.1:5000

El navegador no se abre automáticamente.
Para detener el servidor, presionar Ctrl + C en la terminal.

Por ahora no hace falta instalar MySQL para ver la bienvenida.

## Organización actual

```text
techflow/
├── app/
│   ├── __init__.py                  # Crea y configura la aplicación
│   └── controllers/
│       ├── __init__.py
│       └── inicio_controller.py     # Atiende la página principal
├── run.py                          # Inicia el servidor
├── requirements.txt                # Dependencias
├── .gitignore                      # Archivos excluidos de Git
├── templates/
│   └── index.html                  # Pantalla de bienvenida
└── static/
    └── css/
        └── estilos.css             # Diseño visual
```

La carpeta `.venv` se crea en cada computadora y no se sube a GitHub.

## Equipo

- Ezequiel: arquitectura, servidor e integración.
- Maximiliano: base de datos, productos y proveedores.
- Bruno: inventario, ventas y caja.
- Abel: interfaz, estilos y manual de usuario.
- Andrés: estadísticas, reportes y textos académicos.

## Cómo colaborar

1. Actualizar la rama `main` antes de comenzar una tarea.
2. Crear una rama con un nombre que describa el trabajo.
3. Realizar los cambios y probarlos.
4. Crear un commit con un mensaje claro.
5. Subir la rama y abrir un pull request hacia `main`.
6. Pedir revisión a otro integrante antes de integrar los cambios.

No subir contraseñas, archivos `.env` ni la carpeta `.venv`.
Los cambios de tablas o de comunicación entre módulos deben
acordarse con quienes los utilizan.

## Espacios del equipo

- [Repositorio](https://github.com/Nekro3898/techflow)
- [Tablero de tareas](https://techflow-equipo-tablero-ezequiel.dusky-moss-4252.chatgpt.site/board)
- [Página de TechFlow](https://techflow-solutions-coronda.dusky-moss-4252.chatgpt.site)

Exposición: 10 de noviembre de 2026.
