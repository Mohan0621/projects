from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import init_mongo
from app.auth.routes import auth_bp
from app.user.routes import user_bp
from app.admin.routes import admin_bp

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    init_mongo(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    return app