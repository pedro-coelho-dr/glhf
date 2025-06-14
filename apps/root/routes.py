
from flask import render_template, request, redirect, send_from_directory

import os
from apps.root import root_bp
from common.session import get_current_user, get_user_by_id
from apps.root.logic.root import load_pending_users, execute_sql, execute_shell

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')

@root_bp.route('/root', methods=['GET', 'POST'])
def root():
    current = get_current_user()
    if not current:
        return redirect("/login")

    token = request.headers.get("X-GLHF-Token") or request.args.get("token")
    if token != "root":
        return redirect("/")

    user = get_user_by_id(current["id"])
    if not user or user.get("role") != "admin":
        return redirect("/")

    pending = load_pending_users()
    shell_output = ""
    sql_output = ""

    if request.method == "POST":
        if "cmd" in request.form:
            shell_output = execute_shell(request.form.get("cmd", ""))
        elif "sql" in request.form:
            sql_output = execute_sql(request.form.get("sql", ""))

    return render_template(
        'root.html',
        user=user,
        pending=pending,
        output=shell_output,
        sql_output=sql_output,
        page='root'
    )

@root_bp.route('/root/download_source')
def download_source():
    current = get_current_user()
    if not current or current.get('role') != 'admin':
        return redirect('/')
    return send_from_directory(DATA_DIR, 'source_leak.tar', as_attachment=True)
