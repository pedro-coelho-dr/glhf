import hashlib
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / 'data'
USERS_FILE = DATA_DIR / 'users.json'
PENDING_FILE = DATA_DIR / 'pending_users.json'

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open(USERS_FILE) as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception as e:
        print(f"[ERROR] Failed to load users.json: {e}")
        return []

def load_pending_users():
    try:
        with open(PENDING_FILE) as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception as e:
        print(f"[ERROR] Failed to load pending_users.json: {e}")
        return []

def add_pending_user(username: str, password: str, email: str = ''):
    pending = load_pending_users()
    pending.append({
        'username': username,
        'password': password,
        'email': email
    })
    try:
        with open(PENDING_FILE, 'w') as f:
            json.dump(pending, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to write to pending_users.json: {e}")

