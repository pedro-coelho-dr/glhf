import json
from pathlib import Path
import hashlib

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
USERS_FILE = DATA_DIR / 'users.json'

def load_users():
    with open(USERS_FILE) as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
