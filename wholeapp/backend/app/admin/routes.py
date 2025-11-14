from flask import Blueprint, jsonify, request, current_app
from bson import ObjectId
from app.models import users_collection
from app.utils.jwt_utils import token_required, role_required
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
@admin_bp.get("/users")
@token_required
@role_required("admin")
def get_users(payload):
    col = users_collection()

    users = list(col.find({}, {"password": 0}))
    for u in users:
        u["_id"] = str(u["_id"])
    return jsonify(users)
@admin_bp.delete("/delete/<user_id>")
@token_required
@role_required("admin")
def delete_user(payload, user_id):
    col = users_collection()
    result = col.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        return {"msg": "User not found"}, 404
    return {"msg": "User deleted"}
@admin_bp.post("/promote/<user_id>")
@token_required
@role_required("admin")
def promote_user(payload, user_id):
    col = users_collection()
    result = col.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": "admin"}}
    )
    if result.modified_count == 0:
        return {"msg": "User not found"}, 404
    return {"msg": "User promoted to admin"}
@admin_bp.get("/stats")
@token_required
@role_required("admin")
def system_stats(payload):
    col = users_collection()
    total = col.count_documents({})
    admins = col.count_documents({"role": "admin"})
    users = total - admins
    stats = {
        "total_users": total,
        "admins": admins,
        "normal_users": users
    }
    return jsonify(stats)
