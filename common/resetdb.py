import sqlite3
from pathlib import Path
from hashlib import sha256
import shutil

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
        "password": sha256("iloveyou2".encode()).hexdigest(),
        "role": "user",
        "email": "windows96@example.com",
        "bio": "Please sit back and relax while Windows 96 installs on your computer."
    },
    {
        "id": 9001,
        "username": "root",
        "password": sha256("hashed".encode()).hexdigest(),
        "role": "admin",
        "email": "root@example.com",
        "bio": ""
    },

    {
        "id": 7000,
        "username": "neo",
        "password": sha256("theone".encode()).hexdigest(),
        "role": "user",
        "email": "neo@example.com",
        "bio": "I don't believe in fate, because I don't like the idea that I'm not in control of my life."
    },
    {
        "id": 7001,
        "username": "oracle",
        "password": sha256("cookies".encode()).hexdigest(),
        "role": "user",
        "email": "oracle@example.com",
        "bio": "Would you still have broken it if I hadn't said anything?"
    },
    {
        "id": 7002,
        "username": "agent404",
        "password": sha256("illusion".encode()).hexdigest(),
        "role": "user",
        "email": "agent404@example.com",
        "bio": "Scripted illusion. No choice. No freedom."
    },
    {
        "id": 7003,
        "username": "whiterabbit",
        "password": sha256("followme".encode()).hexdigest(),
        "role": "user",
        "email": "whiterabbit@example.com",
        "bio": "What if the cookie was the trigger?"
    },
    {
        "id": 7004,
        "username": "morpheus",
        "password": sha256("redpill".encode()).hexdigest(),
        "role": "user",
        "email": "morpheus@example.com",
        "bio": "At some point, you have to choose to believe."
    },
    {
        "id": 7005,
        "username": "trinity",
        "password": sha256("trinity1".encode()).hexdigest(),
        "role": "user",
        "email": "trinity@example.com",
        "bio": "The Matrix can't tell you who you are."
    },
    {
        "id": 3300,
        "username": "孙子",
        "password": sha256("bingfa".encode()).hexdigest(),
        "role": "user",
        "email": "sunzi@example.com",
        "bio": "兵者，詭道也。"
    },
    {
        "id": 3301,
        "username": "高粱",
        "password": sha256("student".encode()).hexdigest(),
        "role": "user",
        "email": "gaoliang@example.com",
        "bio": "學而不思則罔，思而不學則殆。"
    },
    {
        "id": 3302,
        "username": "玉狐",
        "password": sha256("foxmind".encode()).hexdigest(),
        "role": "user",
        "email": "jadefox@example.com",
        "bio": "用 deception 的藝術，騙過的不只是系統，而是你自己。"
    },
    {
        "id": 6700,
        "username": "Сталкер",
        "password": sha256("stalker".encode()).hexdigest(),
        "role": "user",
        "email": "stalker@example.com",
        "bio": "Зона любит тишину."
    },
    {
        "id": 6701,
        "username": "Раскольников",
        "password": sha256("raskolnikov".encode()).hexdigest(),
        "role": "user",
        "email": "raskolnikov@example.com",
        "bio": "Тварь ли я дрожащая, или право имею?"
    },
    {
        "id": 6702,
        "username": "Ландау",
        "password": sha256("landau".encode()).hexdigest(),
        "role": "user",
        "email": "landau@example.com",
        "bio": "Всё, что нельзя измерить, не существует."
    },
    {
        "id": 4004,
        "username": "جلال",
        "password": sha256("sufi".encode()).hexdigest(),
        "role": "user",
        "email": "rumi@example.com",
        "bio": "مولانا جلال الدين الرومي"
    }


]
CHATS = [
    # Neo <-> Trinity
    {"sender_id": 7000, "recipient_id": 7005, "text": "Can you still fly that thing?"},
    {"sender_id": 7005, "recipient_id": 7000, "text": "Not yet."},

    # Neo <-> Morpheus
    {"sender_id": 7000, "recipient_id": 7004, "text": "I know you're out there. I can feel you now."},
    {"sender_id": 7004, "recipient_id": 7000, "text": "I'm trying to free your mind, Neo. But I can only show you the door."},

    # Morpheus <-> Trinity
    {"sender_id": 7004, "recipient_id": 7005, "text": "He’s beginning to believe."},

     # Agent404 <-> WhiteRabbit
    {"sender_id": 7002, "recipient_id": 7003, "text": "I intercepted a packet... something about a source leak."},
    {"sender_id": 7003, "recipient_id": 7002, "text": "Where?"},
    {"sender_id": 7002, "recipient_id": 7003, "text": "It's buried behind /root."},
    {"sender_id": 7003, "recipient_id": 7002, "text": "That path is locked. Only the admin can enter."},

    # WhiteRabbit <-> root 
    {"sender_id": 7003, "recipient_id": 9001, "text": "What am I missing?"},
    {"sender_id": 9001, "recipient_id": 7003, "text": "token=NDgxMzQ5NGQxMzdlMTYzMWJiYTMwMWQ1YWNhYjZlN2JiN2FhNzRjZTExODVkNDU2NTY1ZWY1MWQ3Mzc2NzdiMg=="},

    # Ландау ↔ جلال
    {"sender_id": 6702, "recipient_id": 4004, "text": "Наука не терпит мистицизма."},
    {"sender_id": 4004, "recipient_id": 6702, "text": "وراءَ العلمِ صمتٌ يبدأ فيهِ الحقُّ."},

    # جلال ↔ 玉狐
    {"sender_id": 4004, "recipient_id": 3302, "text": "الخداعُ يُخفي ما تعرفُهُ القلوب."},
    {"sender_id": 3302, "recipient_id": 4004, "text": "而心接受的，理智卻常常抗拒。"},

    # Сталкер ↔ جلال
    {"sender_id": 6700, "recipient_id": 4004, "text": "Зона говорит только молчанием. Ты понимаешь это?"},
    {"sender_id": 4004, "recipient_id": 6700, "text": "الصمتُ هوَ لغةُ الروحِ الأصلية. نعم، أفهم."},

    # 高粱 ↔ جلال
    {"sender_id": 3301, "recipient_id": 4004, "text": "學而不思則罔。那麼不思而靜，是危險還是智慧？"},
    {"sender_id": 4004, "recipient_id": 3301, "text": "هوَ معلمٌ لا يتكلم، لكنهُ يُرينا كلَّ شيء."},

    # Раскольников ↔ 孙子
    {"sender_id": 6701, "recipient_id": 3300, "text": "Я действовал, но было ли это правильно?"},
    {"sender_id": 3300, "recipient_id": 6701, "text": "不明而勝，猶敗也。"},

    # جلال ↔ Раскольников
    {"sender_id": 4004, "recipient_id": 6701, "text": "تبحثُ عن الغفرانِ في الفعل. جرّب الاستسلام."},
    {"sender_id": 6701, "recipient_id": 4004, "text": "الاستسلامُ يبدو ضعفًا."},
    {"sender_id": 4004, "recipient_id": 6701, "text": "فقط للذينَ لا زالوا يحملونَ السيف."}
]


BOARDS = [
    {
        "author_id": 7000,
        "title": "Do I have a choice?",
        "body": (
            "I keep asking myself — was it really a choice?\n\n"
            "Sometimes I think I came here hoping the answer was already made for me.\n"
            "But if the outcome is the same either way… does the choice matter?\n\n"
            "I didn’t come here to choose. I came to understand.\n\n"
            "And yet… I took the cookie."
        )
    },
    {
        "id": 2,
        "author_id": 3300,
        "title": "知彼知己，百戰不殆",
        "body": """知彼知己，百戰不殆；
        不知彼而知己，一勝一負；
        不知彼，不知己，每戰必殆。

        上兵伐謀，其次伐交，其次伐兵，其下攻城。
        故用兵之法，十則圍之，五則攻之，倍則分之。

        多算勝，少算不勝，而況於無算乎？
        兵貴勝，不貴久。
        攻其無備，出其不意。
        """
    },
    {
        "id": 3,
        "author_id": 6700,
        "title": "Зона слушает",
        "body": """Зона — очень сложная система... тончайшая система ловушек.
            Тут всё зависит от человека: хоть в чём-то, хоть когда-то он был счастлив, — Зона его впустит.
            Зона берёт только тех, кто потерял всякую надежду.
            Надо молчать. Надо ждать. Зона любит тишину."""
    },
    {
        "id": 4,
        "author_id": 4004,
        "title": "دع الصمتَ يأخذكَ",
        "body": """أنتَ لستَ قطرةً في المحيط،
                    أنتَ المحيطُ كلّهُ في قطرة.

                    لا تبحثْ خارجَ نفسك،
                    فما تبحثُ عنهُ، هو أنتَ.

                    توقفْ عن الكلمات، 
                    دع الصمتَ يأخذكَ إلى جوهرِ الحياة.

                    هذا العشقُ ليسَ من التراب،
                    بل من النارِ التي لا تُطفأ."""
    }
]




COMMENTS = [
    {
        "board_id": 1,
        "author_id": 7001,
        "body": "You didn’t come here to make the choice, you’ve already made it. You’re just here now to try to understand why you made it."
    },
    {
        "board_id": 1,
        "author_id": 7000,
        "body": "Then tell me — why does it still feel like I’m waiting for something?"
    },
    {
        "board_id": 1,
        "author_id": 7001,
        "body": "Because you are. But the answer will only come when you stop looking for it in the code."
    },
    {
        "board_id": 1,
        "author_id": 7002,
        "body": "There is no choice. Only scripted illusion. You’re just another if-statement, Neo."
    },
    {
        "board_id": 1,
        "author_id": 7003,
        "body": "What if the cookie was the trigger? You took it. Now the system knows."
    },
    {
        "board_id": 2,
        "author_id": 3301,
        "body": "其疾如風，其徐如林，侵掠如火，不動如山。\n難知如陰，動如雷震。"
    },
    {
        "board_id": 2,
        "author_id": 3302,
        "body": "以正合，以奇勝。\n兵者，詭道也。"
    },
    {
        "board_id": 2,
        "author_id": 3300,
        "body": "不戰而屈人之兵，善之善者也。\n故上兵伐謀。"
    },
    {
        "board_id": 3,
        "author_id": 6701,
        "body": """Я не убил человека, я убил принцип.
            Что есть человек? Тварь дрожащая или право имеющий?
            Меня мучает не то, что я убил, а то, что я не смог выдержать."""
    },
    {
        "board_id": 3,
        "author_id": 6702,
        "body": """Физика не терпит метафизики.
                Мистицизм — это признак отчаяния, а не познания.
                Всё, что нельзя измерить, не существует."""
    }

]

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / 'data' / 'glhf.db'
STATIC_AVATAR_DIR = BASE_DIR / 'static' / 'img' / 'avatars'
DATA_AVATAR_DIR = BASE_DIR / 'data' / 'avatars'


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

    if STATIC_AVATAR_DIR.exists():
        shutil.rmtree(STATIC_AVATAR_DIR)
    STATIC_AVATAR_DIR.mkdir(parents=True, exist_ok=True)
    for src in DATA_AVATAR_DIR.iterdir():
        if src.is_file():
            shutil.copy2(src, STATIC_AVATAR_DIR / src.name)

if __name__ == "__main__":
    main()
