from flask import Flask, render_template
from routes import eventos_bp, auth_bp
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__, template_folder=os.path.join("../frontend/templates"))  # Asegurar la ruta correcta
app.secret_key = "tu_clave_secreta"

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(eventos_bp, url_prefix="/api")  # Esto hace que /upload esté en /api/upload


@app.route("/")
def index():
    return render_template("index.html")  # Asegurar que index.html existe

if __name__ == "__main__":
    app.run(debug=True)
