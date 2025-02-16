from flask import Blueprint, render_template, request, jsonify
import os
import pytesseract
import openai
import cv2
from dotenv import load_dotenv
from PIL import Image
from database import get_db_connection

# Cargar API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configurar OpenAI para usar GROQ
openai.api_key = GROQ_API_KEY
openai.base_url = "https://api.groq.com/v1"

# Blueprint de eventos
eventos_bp = Blueprint("eventos", __name__)

# -------------------------
# 📌 Procesar imagen antes del OCR
# -------------------------
def preprocess_image(image_path):
    """ Convierte la imagen a escala de grises y aplica binarización para mejorar OCR """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    return thresh

# -------------------------
# 📌 Limpiar texto extraído
# -------------------------
def limpiar_texto(texto):
    """ Elimina líneas vacías y caracteres innecesarios """
    lineas = texto.split("\n")
    lineas_filtradas = [linea.strip() for linea in lineas if len(linea.strip()) > 5]
    return "\n".join(lineas_filtradas)

# -------------------------
# 📌 Organizar texto en tabla
# -------------------------
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
            horario[dia_actual].append({
                "hora_inicio": "08:00",  # Se pueden mejorar con regex
                "hora_fin": "10:00",
                "materia": linea,
                "aula": "Aula 101"
            })
    
    return horario

# -------------------------
# 📌 Endpoint para subir imagen y mostrar horario
# -------------------------
@eventos_bp.route("/upload", methods=["GET", "POST"])
def upload():
    """ Subida de imágenes y procesamiento OCR usando GROQ """
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"error": "No se ha subido ninguna imagen"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Nombre de archivo inválido"}), 400

        # Guardar imagen
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)

        # Procesar la imagen con OCR
        processed_image = preprocess_image(filepath)
        text = pytesseract.image_to_string(Image.open(filepath), config='--psm 6')
        text = limpiar_texto(text)

        # -------------------------
        # 📌 Llamada a GROQ para estructurar
        # -------------------------
        response = openai.ChatCompletion.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Eres un asistente que organiza horarios de clases extraídos de imágenes."},
                {"role": "user", "content": f"Organiza este horario en una tabla estructurada: {text}"}
            ]
        )
        texto_mejorado = response["choices"][0]["message"]["content"]
        horario = procesar_texto_a_tabla(texto_mejorado)

        return render_template("horario.html", horario=horario)

    return render_template("upload.html")
