from flask import request, render_template, redirect, make_response, send_file

import time
from pathlib import Path
from uuid import uuid4

from . import lobby_bp
from apps.lobby.logic.users import add_pending_user
from apps.lobby.logic.auth_state import save_pre_auth, load_pre_auth, delete_pre_auth, get_attempts, increment_attempt
from apps.lobby.logic.two_fa import generate_or_get_global_2fa_code

from common.session import get_current_user, generate_token
from common.users import load_users, hash_password


LOBBY_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = LOBBY_DIR / 'data' / 'download'

FAST_DELAY = 0.05
SLOW_DELAY = 0.1

@lobby_bp.route('/')
def index():
    current = get_current_user()
    if not current:
        return redirect("/login")

    return redirect('/profile')

@lobby_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    username_input = ''

    if request.method == 'POST':
        username_input = request.form.get('username', '')
        password = request.form.get('password', '')
        users = load_users()

        user = next((u for u in users if u['username'] == username_input), None)
        error_message = 'Invalid credentials.'

        if not user:
            time.sleep(FAST_DELAY)
            error = error_message + '<!-- id:0 -->'

        elif user['password'] != hash_password(password):
            time.sleep(SLOW_DELAY)
            error = error_message + '<!-- id:1 padding -------------- -->'

        else:
            pre_auth_token = str(uuid4())
            save_pre_auth(pre_auth_token, user['id'])

            resp = make_response(redirect('/2fa'))
            resp.set_cookie('pre_auth_token', pre_auth_token, path='/', httponly=True)
            return resp

    return render_template('login.html', error=error, username=username_input)


@lobby_bp.route('/2fa', methods=['GET', 'POST'])
def two_fa():
    token = request.cookies.get('pre_auth_token')
    state = load_pre_auth(token) if token else None

    if not state:
        return redirect('/login')

    if get_attempts(token) >= 3:
        delete_pre_auth(token)
        return redirect('/login')

    users = load_users()
    user = next((u for u in users if u['id'] == state['id']), None)

    if not user:
        return redirect('/login')

    error = ''
    if request.method == 'POST':
        increment_attempt(token)

        if get_attempts(token) >= 4:
            delete_pre_auth(token)
            return redirect('/login')

        code_input = request.form.get('code', '').strip()
        correct_code = generate_or_get_global_2fa_code()

        if code_input == correct_code:
            session_token = generate_token(user['username'], user['role'], user['id'])
            resp = make_response(redirect('/'))
            resp.set_cookie(
                'session_id',
                session_token,
                path='/', 
                httponly=False,
                secure=False,
                samesite=None
            )
            resp.delete_cookie('pre_auth_token')
            delete_pre_auth(token)
            return resp
        else:
            time.sleep(0.025)
            error = 'Invalid code.'

    return render_template('2fa.html', error=error)


@lobby_bp.route('/register', methods=['GET', 'POST'])
def register():
    submitted_username = ''
    message = None

    if request.method == 'POST':
        submitted_username = request.form.get('username', '')
        email_input = request.form.get('email', '')
        password = request.form.get('password', '')
        users = load_users()

        username_exists = any(u['username'] == submitted_username for u in users)
        email_exists = any(u.get('email') == email_input for u in users if u.get('email'))

        if username_exists and email_exists:
            time.sleep(SLOW_DELAY)
        elif username_exists or email_exists:
            time.sleep(FAST_DELAY)

        else:
            time.sleep(0.01)
            add_pending_user(submitted_username, password, email_input)

        message = 'Registration request received.'

    return render_template('register.html', message=message, username=submitted_username)


@lobby_bp.route('/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.delete_cookie('session_id', path='/')
    return resp


@lobby_bp.route('/download/nicks.txt')
def download_nicks():
    return send_file(
        DOWNLOAD_DIR / 'nicks.txt',
        as_attachment=True,
        download_name='nicks.txt'
    )


@lobby_bp.route('/download/rockyou.txt')
def download_rockyou():
    return send_file(
        DOWNLOAD_DIR / 'rockyou.txt',
        as_attachment=True,
        download_name='rockyou.txt'
    )

@lobby_bp.route('/download/readme.txt')
def download_readme():
    return send_file(
        DOWNLOAD_DIR / 'readme.txt',
        as_attachment=True,
        download_name='readme.txt'
    )