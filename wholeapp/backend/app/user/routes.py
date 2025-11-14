import os
from flask import Blueprint, jsonify, current_app, request, send_from_directory
from bson import ObjectId
from app.utils.jwt_utils import token_required
from app.models import users_collection

user_bp = Blueprint("user", __name__, url_prefix="/user")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.get("/me")
@token_required
def me(payload):
    user_id = payload["sub"]
    users = users_collection()
    user = users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if not user:
        return jsonify({"msg": "User not found"}), 404
    user["_id"] = str(user["_id"])
    return jsonify(user)

@user_bp.post("/update")
@token_required
def update_user(payload):
    user_id = payload["sub"]
    data = request.get_json()
    new_username = data.get("username")
    new_email = data.get("email")
    users = users_collection()
    update_data = {}
    if new_username:
        update_data["username"] = new_username
    if new_email:
        update_data["email"] = new_email
    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    return jsonify({"msg": "Profile updated"})

@user_bp.post("/upload")
@token_required
def upload_image(payload):
    if "file" not in request.files:
        return jsonify({"msg": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"msg": "Empty filename"}), 400
    if not allowed_file(file.filename):
        return jsonify({"msg": "Invalid file type"}), 400
    users = users_collection()
    user_id = payload["sub"]
    filename = f"{user_id}.jpg"
    upload_path = os.path.join("uploads", filename)
    file.save(upload_path)
    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"profile_image": filename}}
    )
    return jsonify({"msg": "Image uploaded", "filename": filename})

@user_bp.get("/image/<filename>")
def serve_image(filename):
    return send_from_directory("uploads", filename)
