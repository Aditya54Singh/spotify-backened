from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_and_cursor

playlist_bp = Blueprint("playlists", __name__)

# ---------------- CREATE PLAYLIST ----------------
@playlist_bp.route("/playlists", methods=["POST"])
@jwt_required()
def create_playlist():
    user_id = get_jwt_identity()
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"msg": "Playlist name required"}), 400

    conn, cursor = get_db_and_cursor()

    cursor.execute(
        "INSERT INTO playlists (user_id, name) VALUES (%s, %s)",
        (user_id, name)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"msg": "Playlist created"}), 201


# ---------------- GET USER PLAYLISTS ----------------
@playlist_bp.route("/playlists", methods=["GET"])
@jwt_required()
def get_playlists():
    user_id = get_jwt_identity()

    conn, cursor = get_db_and_cursor()

    cursor.execute(
        "SELECT id, name FROM playlists WHERE user_id = %s",
        (user_id,)
    )
    playlists = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(playlists), 200


# ---------------- ADD SONG TO PLAYLIST ----------------
@playlist_bp.route("/playlists/<int:playlist_id>/songs", methods=["POST"])
@jwt_required()
def add_song_to_playlist(playlist_id):
    data = request.get_json()
    song_id = data.get("song_id")

    if not song_id:
        return jsonify({"msg": "Song ID required"}), 400

    conn, cursor = get_db_and_cursor()

    # Optional: prevent duplicate songs in same playlist
    cursor.execute(
        """
        SELECT id FROM playlist_songs
        WHERE playlist_id = %s AND song_id = %s
        """,
        (playlist_id, song_id)
    )
    exists = cursor.fetchone()

    if exists:
        cursor.close()
        conn.close()
        return jsonify({"msg": "Song already in playlist"}), 409

    cursor.execute(
        "INSERT INTO playlist_songs (playlist_id, song_id) VALUES (%s, %s)",
        (playlist_id, song_id)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"msg": "Song added to playlist"}), 200


# ---------------- GET PLAYLIST SONGS ----------------
@playlist_bp.route("/playlists/<int:playlist_id>/songs", methods=["GET"])
@jwt_required()
def get_playlist_songs(playlist_id):
    conn, cursor = get_db_and_cursor()

    cursor.execute(
        """
        SELECT 
            s.id,
            s.name,
            s.description,
            s.image,
            s.audio,
            s.duration
        FROM playlist_songs ps
        JOIN songs s ON ps.song_id = s.id
        WHERE ps.playlist_id = %s
        """,
        (playlist_id,)
    )

    songs = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(songs), 200


# ---------------- DELETE PLAYLIST ----------------
@playlist_bp.route("/playlists/<int:playlist_id>", methods=["DELETE"])
@jwt_required()
def delete_playlist(playlist_id):
    user_id = get_jwt_identity()

    conn, cursor = get_db_and_cursor()

    # Ensure playlist belongs to user
    cursor.execute(
        "SELECT id FROM playlists WHERE id = %s AND user_id = %s",
        (playlist_id, user_id)
    )
    playlist = cursor.fetchone()

    if not playlist:
        cursor.close()
        conn.close()
        return jsonify({"msg": "Playlist not found"}), 404

    # Delete playlist songs first
    cursor.execute(
        "DELETE FROM playlist_songs WHERE playlist_id = %s",
        (playlist_id,)
    )

    # Delete playlist
    cursor.execute(
        "DELETE FROM playlists WHERE id = %s",
        (playlist_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"msg": "Playlist deleted"}), 200
