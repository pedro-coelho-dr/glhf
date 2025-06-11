import json
import time
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parents[1] / 'data' / 'pre_auth.json'
EXPIRATION_TIME = 300

def _load_all():
    try:
        now = int(time.time())
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                data = json.load(f)

            valid_data = {
                token: entry
                for token, entry in data.items()
                if now - entry.get("timestamp", 0) <= EXPIRATION_TIME
            }

            if valid_data != data:
                _save_all(valid_data)

            return valid_data
        return {}
    except Exception:
        return {}


def _save_all(data):
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f)

def save_pre_auth(token: str, user_id: int):
    data = _load_all()
    data[token] = {
        "id": user_id,
        "timestamp": int(time.time()),
        "attempts": 0
    }
    _save_all(data)

def load_pre_auth(token: str):
    data = _load_all()
    entry = data.get(token)
    if not entry:
        return None
    if int(time.time()) - entry['timestamp'] > EXPIRATION_TIME:
        delete_pre_auth(token)
        return None
    return entry

def delete_pre_auth(token: str):
    data = _load_all()
    if token in data:
        del data[token]
        _save_all(data)

def increment_attempt(token: str):
    data = _load_all()
    if token in data:
        data[token]["attempts"] = data[token].get("attempts", 0) + 1
        _save_all(data)

def get_attempts(token: str) -> int:
    data = _load_all()
    return data.get(token, {}).get("attempts", 0)
