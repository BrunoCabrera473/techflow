from flask import Flask

app = Flask(__name__)

@app.get("/")
def inicio():
    return "<h1>TechFlow Solutions</h1><p>La aplicación está funcionando.</p>"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
