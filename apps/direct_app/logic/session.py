import json
import base64
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / 'data'
USERS_FILE = DATA_DIR / 'users.json'

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
    user = decode_token(token)
    if not user:
        return None
    try:
        with open(USERS_FILE) as f:
            users = json.load(f)
        for u in users:
            if u["id"] == user["user_id"]:
                return user
    except Exception:
        pass
    return None
