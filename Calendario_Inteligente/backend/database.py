from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Ares1997@localhost:5432/calendario_db"
    db.init_app(app)
    migrate.init_app(app, db)
