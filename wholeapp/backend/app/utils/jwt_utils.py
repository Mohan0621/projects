import jwt
import uuid
import datetime
from flask import current_app

def create_acces_token(user_id, role):
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "sub": user_id,
        "role": role,
        "iat": now,
        "exp": now + datetime.timedelta(seconds=current_app.config["ACCESS_EXPIRES"]),
        "jti": str(uuid.uuid4()),
        "type": "access"
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")
    return token

def create_refresh_token(user_id):
    now = datetime.datetime.now(datetime.timezone.utc)
    jti = str(uuid.uuid4())
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + datetime.timedelta(seconds=current_app.config["REFRESH_EXPIRES"]),
        "jti": jti,
        "type": "refresh"
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")
    return token, jti
def decode_token(token):
    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET"],
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "token_expired"}
    except jwt.InvalidTokenError:
        return {"error": "invalid_token"}
from functools import wraps
from flask import request, jsonify
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({"msg": "Missing or invalid token"}), 401

        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        if "error" in payload:
            return jsonify(payload), 401
        return f(payload, *args, **kwargs)
    return decorated
def role_required(required_role):
    def wrapper(f):
        @wraps(f)
        def decorated(payload, *args, **kwargs):
            user_role = payload.get("role")
            if user_role != required_role:
                return {"msg": "Admin access required"}, 403
            return f(payload, *args, **kwargs)
        return decorated
    return wrapper
