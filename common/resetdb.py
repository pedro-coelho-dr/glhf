import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / 'data' / 'glhf.db'

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    bio TEXT
);

CREATE TABLE IF NOT EXISTS chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(sender_id) REFERENCES users(id),
    FOREIGN KEY(recipient_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS board (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(author_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    board_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    body TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(board_id) REFERENCES board(id),
    FOREIGN KEY(author_id) REFERENCES users(id)
);
"""
USERS = [
    {
        "id": 1337,
        "username": "windows96",
        "password": "3113c9e45ff0b8e19f06e443deaa361cedb08d420b0e63606219cd5881f5fa27",
        "role": "user",
        "email": "windows96@example.com",
        "bio": "Please sit back and relax while Windows 96 installs on your computer."
    },
    {
        "id": 9001,
        "username": "root",
        "password": "1a06df824ed741b53c785079a6347f00eec5af82f9850775409ca69dff4068a6",
        "role": "admin",
        "email": "root@example.com",
        "bio": ""
    },
    {
        "id": 4242,
        "username": "cypher",
        "password": "f2f8382e7c4be91597f3ae07dbb372ae7fc3a54a7cb1c14f6b4f35db6b2f43e9",
        "role": "user",
        "email": "cypher@example.com",
        "bio": "Decoding secrets, one byte at a time."
    }
]

CHATS = [
    # windows96 <-> root
    {
        "sender_id": 1337,
        "recipient_id": 9001,
        "text": "Hey root, is there any secret command in this chat?"
    },
    {
        "sender_id": 9001,
        "recipient_id": 1337,
        "text": "You should know, windows96. Try /debugmode!"
    },
    # cypher <-> root
    {
        "sender_id": 4242,
        "recipient_id": 9001,
        "text": "root, can you give me admin access? :)"
    },
    {
        "sender_id": 9001,
        "recipient_id": 4242,
        "text": "Nice try, cypher. Not this time!"
    },
    # cypher <-> windows96
    {
        "sender_id": 1337,
        "recipient_id": 4242,
        "text": "cypher, did you figure out the flag from last night?"
    },
    {
        "sender_id": 4242,
        "recipient_id": 1337,
        "text": "Not yet, windows96. I think we need to brute-force the hash!"
    }
]

BOARDS = [
    {
        "author_id": 1337,
        "title": "Welcome to GLHF Board!",
        "body": "Feel free to post any bugs or features. (No, we don't have a dark mode yet!)"
    },
    {
        "author_id": 9001,
        "title": "Root's Announcement",
        "body": "System maintenance at midnight. Expect random glitches and secret flags."
    }
]

COMMENTS = [
    {
        "board_id": 1,
        "author_id": 9001,
        "body": "Welcome, users. Remember to change your password!"
    },
    {
        "board_id": 2,
        "author_id": 1337,
        "body": "Will there be any downtime for the board? Asking for a friend."
    }
]

def reset_db():
    if DB_PATH.exists():
        DB_PATH.unlink()
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)

def seed_all():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        for u in USERS:
            c.execute("INSERT INTO users (id, username, password, role, email, bio) VALUES (?, ?, ?, ?, ?, ?)",
                      (u["id"], u["username"], u["password"], u["role"], u["email"], u["bio"]))
        for b in BOARDS:
            c.execute("INSERT INTO board (author_id, title, body) VALUES (?, ?, ?)",
                      (b["author_id"], b["title"], b["body"]))
        for ch in CHATS:
            c.execute("INSERT INTO chat (sender_id, recipient_id, text) VALUES (?, ?, ?)",
                      (ch["sender_id"], ch["recipient_id"], ch["text"]))
        for cm in COMMENTS:
            c.execute("INSERT INTO comments (board_id, author_id, body) VALUES (?, ?, ?)",
                      (cm["board_id"], cm["author_id"], cm["body"]))
        conn.commit()

def main():
    reset_db()
    init_db()
    seed_all()

if __name__ == "__main__":
    main()
