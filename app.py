from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "clave_super_secreta"

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

def token_requerido(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"mensaje": "Debe iniciar sesión"}), 401
        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return jsonify({"mensaje": "Token inválido o expirado"}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data["usuario"] in usuarios and data["password"] == usuarios[data["usuario"]]["password"]:
        token = generar_token(data["usuario"])
        return jsonify({"token": token})
    return jsonify({"mensaje": "Credenciales incorrectas"}), 401

@app.route("/")
@token_requerido
def home():
    return jsonify({"mensaje": "Bienvenido Dr. Christian Arias"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
