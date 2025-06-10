# apps/user_app/logic/session.py

import json
import base64
from pathlib import Path
from flask import request

DATA_DIR = Path(__file__).resolve().parents[2] / 'data'
USERS_FILE = DATA_DIR / 'users.json'

def load_users():
    with open(USERS_FILE) as f:
        return json.load(f)

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

def validate_token(token: str):
    token_data = decode_token(token)
    if not token_data:
        return None

    users = load_users()
    for u in users:
        if u["id"] == token_data["user_id"]:
            return token_data
    return None

def get_user_by_id(user_id: int):
    users = load_users()
    for u in users:
        if u["id"] == user_id:
            return u
    return None

def get_user_by_username(username: str):
    users = load_users()
    for u in users:
        if u["username"] == username:
            return u
    return None

def get_current_user(strict=True):
    token = request.cookies.get('session_id')
    user = validate_token(token)
    if not user and strict:
        return None
    return user

def token_matches_user(user_data, token_data):
    return (
        user_data["id"] == token_data["user_id"] and
        user_data["username"] == token_data["username"]
    )
