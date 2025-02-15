from flask import Flask, render_template
from routes import eventos_bp
import os

app = Flask(__name__, template_folder=os.path.join("../frontend/templates"))  # Usar la carpeta de templates en frontend
app.register_blueprint(eventos_bp, url_prefix="/api")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
