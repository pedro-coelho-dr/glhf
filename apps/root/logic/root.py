import os
import json
import sqlite3
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / 'data'
DB_PATH = DATA_DIR / 'glhf.db'
PENDING_USERS_FILE = DATA_DIR / 'pending_users.json'


def load_pending_users():
    try:
        with open(PENDING_USERS_FILE, encoding='utf-8') as f:
            content = f.read().strip()
            return json.dumps(json.loads(content or "[]"), indent=2, ensure_ascii=False)
    except Exception as e:
        return f"[ERROR] Failed to load pending_users.json: {e}"


def execute_sql(query: str) -> str:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(query)
            if query.strip().lower().startswith("select"):
                rows = cur.fetchall()
                if not rows:
                    return "[INFO] Query returned no results."
                headers = rows[0].keys()
                result_lines = [" | ".join(headers)]
                result_lines.append("-" * len(result_lines[0]))
                for row in rows:
                    result_lines.append(" | ".join(str(row[h]) for h in headers))
                return "\n".join(result_lines)
            else:
                conn.commit()
                return f"[SUCCESS] Executed: {query}"
    except Exception as e:
        return f"[SQL ERROR] {e}"


def execute_shell(cmd: str) -> str:
    try:
        return subprocess.getoutput(cmd)
    except Exception as e:
        return f"[SHELL ERROR] {e}"
