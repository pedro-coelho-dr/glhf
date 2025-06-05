import time
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / 'data'
LOG_FILE = DATA_DIR / 'auth_logs.json'

def log_auth_attempt(username: str, success: bool, ip: str, token: str = ''):
    log_data = {
        "timestamp": int(time.time()),
        "username": username,
        "ip": ip,
        "success": success,
        "session_id": token if success else None
    }
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(log_data) + '\n')
    except Exception as e:
        print(f"[ERROR] Failed to write auth log: {e}")
