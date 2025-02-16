from flask import Blueprint, request, session, redirect, url_for, render_template
from database import get_db_connection

eventos_bp = Blueprint("eventos", __name__)
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        # Verifica si el usuario ya existe
        cur.execute("SELECT * FROM usuario WHERE username = %s OR email = %s", (username, email))
        if cur.fetchone():
            cur.close()
            conn.close()
            return "Usuario o correo ya existe"

        # Inserta nuevo usuario
        cur.execute("INSERT INTO usuario (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()

        cur.close()
        conn.close()
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM usuario WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session["user_id"] = user[0]  # Almacena el ID del usuario en la sesión
            return redirect(url_for("index"))
        return "Credenciales incorrectas"

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))
