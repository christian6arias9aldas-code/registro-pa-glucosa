from flask import Flask, request, jsonify, render_template
import jwt
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "clave_super_secreta"

# Usuarios (luego se guardarán en base de datos)
usuarios = {
    "carias": {
        "nombre": "Dr. Christian Arias",
        "password": "123456"
    }
}

def generar_token(usuario):
    payload = {
        "usuario": usuario,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = data.get("usuario")
    password = data.get("password")

    if usuario in usuarios and password == usuarios[usuario]["password"]:
        token = generar_token(usuario)
        return jsonify({"token": token})
    return jsonify({"mensaje": "Usuario o contraseña incorrectos"}), 401

@app.route("/panel")
def panel():
    return """
    <h2>Bienvenido Dr. Christian Arias</h2>
    <p>Sistema de Registro de Presión Arterial y Glucosa Capilar</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
