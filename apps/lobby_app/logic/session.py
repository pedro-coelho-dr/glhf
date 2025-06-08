import json
import base64

def generate_token(username, role='user', user_id=0):
    payload = {
        "u": username,
        "r": role,
        "id": user_id,
        "exp": 9999999999
    }
    raw = json.dumps(payload, separators=(',', ':'))
    return base64.b64encode(raw.encode()).decode()

def decode_token(token):
    try:
        data = json.loads(base64.b64decode(token.encode()).decode())
        return {
            "username": data.get("u"),
            "role": data.get("r"),
            "id": data.get("id"),
            "exp": data.get("exp")
        }
    except Exception:
        return None
