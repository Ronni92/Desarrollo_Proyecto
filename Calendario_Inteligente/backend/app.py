from flask import Flask, render_template
from routes import eventos_bp, auth_bp
import os

app = Flask(__name__, template_folder=os.path.join("../frontend/templates"))  # Usar la carpeta de templates en frontend
app.secret_key = "tu_clave_secreta"  # Clave para sesiones
app.register_blueprint(eventos_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
