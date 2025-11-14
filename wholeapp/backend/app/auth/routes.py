from flask import Blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
from flask import request, jsonify,current_app
from app.utils.hash_utils import hash_password, verify_password
from app.models import users_collection
from app.utils.jwt_utils import create_acces_token,create_refresh_token,decode_token
@auth_bp.route("/register", methods=["POST"])
def register():
    data=request.get_json()
    username=data.get("username")
    password=data.get("password")
    col=users_collection()
    if col.findone({"username":username}):
        return jsonify({"message":"Username already exists"}),400
    col.insert_one({"username":username,"password":hash_password(password),"role":"user"})
    return jsonify({"message":"User registered successfully"}),201
@auth_bp.route("/login", methods=["POST"])
def login():
    data=request.get_json()
    username=data["username"]
    password=data["password"]
    col=users_collection()
    user=col.find_one({"username":username})
    if not user :
        return jsonify({"message":"Invalid username"}),401
    if not verify_password(password,user["password"]):
        return jsonify({"message":"Invalid password"}),401
    access_token=create_acces_token(str(user["_id"]),user["role"])
    refresh_token,jti=create_refresh_token(str(user["_id"]))
    current_app.db["refresh_tokens"].insert_one({"jti":jti,"user_id":str(user["_id"]),"revoked":False})
    response=jsonify({"access_token":access_token})
    response.set_cookie("refresh_token",refresh_token,httponly=True,samesite="Strict")
    return response,200
@auth_bp.post("/refresh")
def refresh():
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return jsonify({"msg": "missing refresh token"}), 401

    payload = decode_token(refresh_token)
    if "error" in payload:
        return jsonify(payload), 401

    if payload["type"] != "refresh":
        return jsonify({"msg": "invalid token type"}), 401

    jti = payload["jti"]
    token_doc = current_app.db["refresh_tokens"].find_one({"jti": jti})
    if not token_doc:
        return jsonify({"msg": "refresh token revoked"}), 401

    new_access = create_acces_token(payload["sub"], payload.get("role"))
    return jsonify({"access_token": new_access})
@auth_bp.post("/logout")
def logout():
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        payload = decode_token(refresh_token)
        jti = payload.get("jti")

        current_app.db["refresh_tokens"].delete_one({"jti": jti})

    response = jsonify({"msg": "logged out"})
    response.delete_cookie("refresh_token")
    return response
