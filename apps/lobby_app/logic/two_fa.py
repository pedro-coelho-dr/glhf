import json
import time
import hashlib
from pathlib import Path

TWO_FA_FILE = Path(__file__).resolve().parents[2] / 'data' / 'global_2fa_code.json'
TWO_FA_TTL = 15

def generate_or_get_global_2fa_code():
    current_time = int(time.time())

    if TWO_FA_FILE.exists():
        with open(TWO_FA_FILE) as f:
            data = json.load(f)
        if current_time - data["timestamp"] < TWO_FA_TTL:
            return data["code"]

    t_window = current_time // TWO_FA_TTL

    seed = f"glhf_secret:{t_window}"
    hashed = hashlib.sha256(seed.encode()).hexdigest()

    new_code = str(int(hashed[:8], 16) % 10000).zfill(4)

    with open(TWO_FA_FILE, "w") as f:
        json.dump({"code": new_code, "timestamp": current_time}, f)

    return new_code
