from flask import Blueprint, render_template, request, redirect, url_for, session
import pytesseract
from PIL import Image
import os
import cv2
import numpy as np
from database import get_db_connection
from dotenv import load_dotenv
import openai

# ==============================
# 🔹 CARGAR CONFIGURACIONES Y API KEY
# ==============================
# Cargar la API Key desde .env
# Cargar la API Key desde .env
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Configurar el cliente con la API de DeepSeek
# Cargar la API Key desde .env
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Configurar OpenAI para usar DeepSeek
openai.api_key = DEEPSEEK_API_KEY
openai.base_url = "https://api.deepseek.com/v1"  # Asegurar que se usa la API de DeepSeek

# Prueba de conexión con DeepSeek
response = openai.ChatCompletion.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "¿Cómo extraer texto de una imagen?"}]
)

# Mostrar la respuesta
print(response["choices"][0]["message"]["content"])
# ==============================
# 🔹 BLUEPRINTS PARA RUTAS
# ==============================
eventos_bp = Blueprint("eventos", __name__)
auth_bp = Blueprint("auth", __name__)

# ==============================
# 🔹 FUNCIONES DE PROCESAMIENTO
# ==============================
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    """ Verifica si el archivo tiene una extensión permitida """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    """ Convierte la imagen a escala de grises y aplica binarización para mejorar OCR """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Escala de grises
    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)  # Binarización
    return thresh

def limpiar_texto(texto):
    """ Elimina líneas vacías y caracteres extraños del texto OCR """
    lineas = texto.split("\n")
    lineas_filtradas = [linea.strip() for linea in lineas if len(linea.strip()) > 5]
    return "\n".join(lineas_filtradas)

def procesar_texto_a_tabla(text):
    """ Convierte el texto extraído en una tabla estructurada """
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    horario = {dia: [] for dia in dias}
    
    lineas = text.split("\n")
    dia_actual = None

    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue  # Omitir líneas vacías

        for dia in dias:
            if dia in linea:
                dia_actual = dia  # Detectar el día en la línea y cambiar el contexto
                break

        if dia_actual:
            horario[dia_actual].append(linea)
    
    return horario

# ==============================
# 🔹 PROCESAMIENTO DE IMÁGENES Y OCR CON DEEPSEEK
# ==============================
@eventos_bp.route("/upload", methods=["GET", "POST"])
def upload():
    """ Subida de imágenes y procesamiento OCR usando DeepSeek """
    if request.method == "POST":
        if "file" not in request.files:
            return "No se ha subido ninguna imagen", 400

        file = request.files["file"]

        if file.filename == "" or not allowed_file(file.filename):
            return "Formato de imagen no permitido. Usa PNG o JPG", 400

        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)

        # Preprocesar la imagen antes de OCR
        processed_image = preprocess_image(filepath)
        text = pytesseract.image_to_string(Image.open(filepath), config='--psm 6')  # OCR tradicional
        text = limpiar_texto(text)  # Limpieza del texto extraído

        # Llamada a DeepSeek para mejorar la estructuración del texto
        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un asistente que organiza horarios de clases extraídos de imágenes."},
                {"role": "user", "content": f"Organiza este horario en una estructura clara: {text}"}
            ]
        )
        texto_mejorado = response["choices"][0]["message"]["content"]

        # Convertir a tabla estructurada
        horario = procesar_texto_a_tabla(texto_mejorado)

        return render_template("horario.html", horario=horario)
    
    return render_template("upload.html")

# ==============================
# 🔹 AUTENTICACIÓN DE USUARIOS
# ==============================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """ Registro de usuarios """
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM usuario WHERE username = %s OR email = %s", (username, email))
        if cur.fetchone():
            cur.close()
            conn.close()
            return "⚠ Usuario o correo ya registrado."

        cur.execute("INSERT INTO usuario (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("auth.login"))
    
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """ Inicio de sesión """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM usuario WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session["user_id"] = user[0]
            return redirect(url_for("index"))
        return "⚠ Credenciales incorrectas."
    
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    """ Cierre de sesión """
    session.pop("user_id", None)
    return redirect(url_for("index"))
