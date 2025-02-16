from flask import Blueprint, jsonify, request, session, redirect, url_for, render_template
from database import db
from models import Usuario

eventos_bp = Blueprint("eventos", __name__)
auth_bp = Blueprint("auth", __name__)

@eventos_bp.route("/eventos", methods=["GET"])
def get_eventos():
    return jsonify([])

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        
        if Usuario.query.filter_by(username=username).first() or Usuario.query.filter_by(email=email).first():
            return "Usuario o correo ya existe"
        
        new_user = Usuario(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = Usuario.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            return redirect(url_for("index"))
        return "Credenciales incorrectas"
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))
