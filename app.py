from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

from routes.auth_routes import auth_bp
from routes.song_routes import songs_bp
from routes.playlist_routes import playlist_bp

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret")
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(songs_bp, url_prefix="/api")
app.register_blueprint(playlist_bp, url_prefix="/api")

@app.route("/")
def home():
    return {"status": "Backend running"}

if __name__ == "__main__":
    app.run()
