
from pathlib import Path
import os

from common.users import load_users, save_users, hash_password

def update_password(user_id, new_password):
    users = load_users()
    for u in users:
        if u["id"] == user_id:
            u["password"] = hash_password(new_password)
            save_users(users)
            return True
    return False

def update_avatar_file(user_id, file_storage):

    base_dir = Path(__file__).resolve().parents[3] 
    avatar_dir = base_dir / 'static' / 'img' / 'avatars'
    os.makedirs(avatar_dir, exist_ok=True)

    filename = f"{user_id}.jpg"
    filepath = avatar_dir / filename

    file_storage.save(filepath)

    return filename

def update_bio(user_id, new_bio):
    users = load_users()
    for u in users:
        if u["id"] == user_id:
            u["bio"] = new_bio  # salva sem sanitizar!
            save_users(users)
            return True
    return False
