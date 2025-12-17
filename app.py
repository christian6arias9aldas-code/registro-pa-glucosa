from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "clave_super_secreta"

# Usuarios de ejemplo (luego irán a base de datos)
usuarios = {
    "carias": {
        "nombre": "Dr. Christian Arias",
        "password": generate_password_hash("123456")
    }
}

@app.route("/")
def home():
    if "usuario" in session:
        return jsonify({
            "mensaje": f"Bienvenido {usuarios[session['usuario']]['nombre']}"
        })
    return jsonify({"mensaje": "Debe iniciar sesión"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = data.get("usuario")
    password = data.get("password")

    if usuario in usuarios and check_password_hash(usuarios[usuario]["password"], password):
        session["usuario"] = usuario
        return jsonify({"mensaje": "Inicio de sesión exitoso"})
    return jsonify({"mensaje": "Usuario o contraseña incorrectos"}), 401

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return jsonify({"mensaje": "Sesión cerrada"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
