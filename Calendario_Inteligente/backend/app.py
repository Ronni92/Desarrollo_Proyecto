from flask import Flask, render_template
from routes import eventos_bp, auth_bp
from database import init_db  # Importamos la función para inicializar la BD
import os

app = Flask(__name__, template_folder=os.path.join("../frontend/templates"))
app.secret_key = "tu_clave_secreta"

# Inicializar la base de datos con la aplicación Flask
init_db(app)

# Registrar Blueprints
app.register_blueprint(eventos_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
