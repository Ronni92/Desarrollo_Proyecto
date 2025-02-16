from flask import Blueprint, render_template, request, redirect, url_for, session
import pytesseract
from PIL import Image
import os
import re
from database import get_db_connection

# ==============================
# 🔹 DEFINICIÓN DE BLUEPRINTS
# ==============================
eventos_bp = Blueprint("eventos", __name__)
auth_bp = Blueprint("auth", __name__)

# ==============================
# 🔹 REGISTRO DE USUARIOS
# ==============================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Maneja el registro de usuarios. Si el usuario ya existe, devuelve un mensaje de error.
    """
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        # Verifica si el usuario o email ya existen en la base de datos
        cur.execute("SELECT * FROM usuario WHERE username = %s OR email = %s", (username, email))
        if cur.fetchone():
            cur.close()
            conn.close()
            return "⚠ Usuario o correo ya registrado."

        # Inserta el nuevo usuario
        cur.execute("INSERT INTO usuario (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()

        cur.close()
        conn.close()
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Maneja el inicio de sesión de los usuarios.
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        # Busca el usuario en la base de datos
        cur.execute("SELECT id FROM usuario WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session["user_id"] = user[0]  # Guarda el ID del usuario en la sesión
            return redirect(url_for("index"))

        return "⚠ Credenciales incorrectas."

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """
    Cierra la sesión del usuario y lo redirige a la página principal.
    """
    session.pop("user_id", None)
    return redirect(url_for("index"))

# ==============================
# 🔹 SUBIDA Y PROCESAMIENTO DE IMÁGENES CON OCR
# ==============================
@eventos_bp.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Permite a los usuarios subir una imagen con su horario y extraer el texto con OCR.
    Luego, genera una tabla con el horario clasificado por días de la semana.
    """
    if request.method == "POST":
        if "file" not in request.files:
            return "No se ha subido ninguna imagen", 400

        file = request.files["file"]

        if file.filename == "":
            return "Archivo no válido", 400

        # Guardar la imagen en la carpeta de uploads
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)

        # Procesar la imagen con OCR
        text = pytesseract.image_to_string(Image.open(filepath))

        # Clasificar el texto en una tabla estructurada
        horario = procesar_texto_a_tabla(text)

        # Renderizar la tabla con el horario generado
        return render_template("horario.html", horario=horario)

    return render_template("upload.html")


# ==============================
# 🔹 PROCESAMIENTO DEL TEXTO EXTRAÍDO A UNA TABLA
# ==============================
def procesar_texto_a_tabla(text):
    """
    Convierte el texto extraído de la imagen en un diccionario estructurado de horarios.
    
    Args:
        text (str): Texto extraído de la imagen con OCR.

    Returns:
        dict: Diccionario con los días de la semana como claves y las materias como valores.
    """
    # Definir los días de la semana
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    horario = {dia: [] for dia in dias}  # Diccionario para almacenar el horario

    # Separar el texto en líneas y procesarlo
    lineas = text.split("\n")
    dia_actual = None  # Almacenar el día actual mientras se recorren las líneas

    for linea in lineas:
        linea = linea.strip()  # Eliminar espacios en blanco extra

        if not linea:
            continue  # Saltar líneas vacías

        # Detectar si la línea contiene un día de la semana
        for dia in dias:
            if re.search(rf"\b{dia}\b", linea, re.IGNORECASE):  # Buscar el nombre del día
                dia_actual = dia
                break

        # Si ya identificamos un día, asociamos las clases a ese día
        if dia_actual and dia_actual not in linea:
            horario[dia_actual].append(linea)

    return horario
