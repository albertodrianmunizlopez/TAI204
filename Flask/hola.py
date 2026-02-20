from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista simulada de usuarios
usuarios = [
    {"id": 1, "nombre": "Juan", "edad": 25},
    {"id": 2, "nombre": "María", "edad": 30},
    {"id": 3, "nombre": "Pedro", "edad": 22}
]

# Página principal: muestra usuarios y formulario de agregar
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"]
        edad = request.form["edad"]
        nuevo_id = max([u["id"] for u in usuarios]) + 1 if usuarios else 1
        usuarios.append({"id": nuevo_id, "nombre": nombre, "edad": int(edad)})
        return redirect(url_for("index"))
    return render_template("index.html", usuarios=usuarios)

# Ruta para eliminar usuario
@app.route("/eliminar/<int:usuario_id>")
def eliminar(usuario_id):
    global usuarios
    usuarios = [u for u in usuarios if u["id"] != usuario_id]
    return redirect(url_for("index"))

# Ruta para editar usuario
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    usuario = next((u for u in usuarios if u["id"] == id), None)
    if request.method == "POST":
        usuario["nombre"] = request.form["nombre"]
        usuario["edad"] = int(request.form["edad"])
        return redirect(url_for("index"))
    return render_template("editar.html", usuario=usuario)

if __name__ == "__main__":
    app.run(debug=True)
