from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from db import get_db_and_cursor

songs_bp = Blueprint("songs", __name__)

@songs_bp.route("/songs", methods=["GET"])
@jwt_required()
def get_songs():
    conn, cursor = get_db_and_cursor()
    cursor.execute("SELECT * FROM songs")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)
