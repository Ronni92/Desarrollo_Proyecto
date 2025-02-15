from flask import Blueprint, jsonify, request
from database import db
from models import Evento

eventos_bp = Blueprint("eventos", __name__)

@eventos_bp.route("/eventos", methods=["GET"])
def get_eventos():
    eventos = Evento.query.all()
    return jsonify([{ "id": e.id, "titulo": e.titulo, "descripcion": e.descripcion } for e in eventos])
