from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image

app = Flask(__name__, template_folder="../frontend/templates")

# Configuración de subida de imágenes
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "tu_clave_secreta"

# Ruta de Tesseract OCR (ajusta si es necesario)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Función para validar tipos de archivos permitidos
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if "file" not in request.files:
            return "No se envió ningún archivo"

        file = request.files["file"]

        if file.filename == "":
            return "No se seleccionó ningún archivo"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Procesar la imagen con OCR
            extracted_text = extract_text_from_image(filepath)
            return render_template("result.html", text=extracted_text)

    return render_template("upload.html")

def extract_text_from_image(image_path):
    """Extrae el texto de una imagen usando Tesseract OCR"""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang="eng")  # Usa "spa" para español si es necesario
    return text

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
