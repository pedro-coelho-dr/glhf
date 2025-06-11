import os
from flask import render_template, request, redirect, send_from_directory
import json
import subprocess
from apps.root import root_bp
from common.session import get_current_user, get_user_by_id

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')

@root_bp.route('/root', methods=['GET', 'POST'])
def root():
    current = get_current_user()
    if not current:
        return redirect("/login")
    user = get_user_by_id(current["id"])
    if not user or user.get("role") != "admin":
        return redirect("/")

    with open(os.path.join(DATA_DIR, 'users.json')) as f:
        users = json.dumps(json.load(f), indent=2, ensure_ascii=False)
    with open(os.path.join(DATA_DIR, 'pending_users.json')) as f:
        pending = json.dumps(json.load(f), indent=2, ensure_ascii=False)

    output = ""
    if request.method == "POST":
        cmd = request.form.get("cmd", "")
        output = subprocess.getoutput(cmd)

    return render_template(
        'root.html',
        user=user,
        users=users,
        pending=pending,
        output=output,
        page='root'
    )


@root_bp.route('/root/download_source')
def download_source():
    current = get_current_user()
    if not current or current.get('role') != 'admin':
        return redirect('/')
    return send_from_directory(DATA_DIR, 'source_leak.tar', as_attachment=True)
