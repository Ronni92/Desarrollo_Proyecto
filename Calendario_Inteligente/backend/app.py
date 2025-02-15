from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import eventos_bp
from database import db, init_db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Ares1997@localhost:5432/calendario_db"

init_db(app)
migrate = Migrate(app, db)

app.register_blueprint(eventos_bp, url_prefix="/api")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
