from flask import request
import json
import base64
from common.users import load_users

def generate_token(username: str, role: str = 'user', user_id: int = 0) -> str:
    token = {
        "u": username,
        "id": user_id,
        "r": role,         
        "exp": 1669766400, 
        "v": 1             
    }
    raw = json.dumps(token, separators=(',', ':'))
    return base64.b64encode(raw.encode()).decode()

def decode_token(token: str):
    try:
        decoded = base64.b64decode(token.encode()).decode()
        data = json.loads(decoded)
        return {
            "username": data.get("u"),
            "user_id": data.get("id"),
            "role": data.get("r"),
            "exp": data.get("exp"),
            "v": data.get("v")
        }
    except Exception:
        return None

def get_user_by_id(user_id):
    users = load_users()
    for u in users:
        if u["id"] == user_id:
            return u
    return None

def get_user_by_username(username):
    users = load_users()
    for u in users:
        if u["username"] == username:
            return u
    return None

def get_current_user(strict=True):
    token = request.cookies.get("session_id")
    if not token:
        return None if strict else {}
    token_data = decode_token(token)
    if not token_data:
        return None if strict else {}
    user = get_user_by_id(token_data["user_id"])
    if user and user["username"] == token_data["username"]:
        return user
    return None if strict else {}


