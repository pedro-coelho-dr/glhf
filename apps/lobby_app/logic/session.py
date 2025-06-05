import time
import base64

def generate_token(username, role='user'):
    raw = f"{username}:{int(time.time())}:{role}"
    return base64.b64encode(raw.encode()).decode()

def decode_token(token):
    try:
        decoded = base64.b64decode(token.encode()).decode()
        username, timestamp, role = decoded.split(":")
        return {
            "username": username,
            "timestamp": int(timestamp),
            "role": role
        }
    except Exception:
        return None
