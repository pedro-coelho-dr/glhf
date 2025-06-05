from flask import Blueprint, request, render_template, redirect, make_response, send_file
import time
from pathlib import Path

from apps.lobby_app.logic.users import load_users, add_pending_user, hash_password
from apps.lobby_app.logic.session import generate_token, decode_token
from apps.lobby_app.logic.logger import log_auth_attempt

lobby_bp = Blueprint(
    'lobby',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/lobby_static'
)


DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

FAST_DELAY = 0.1
SLOW_DELAY = 0.3

@lobby_bp.route('/')
def index():
    token = request.cookies.get('session_id')
    user = decode_token(token) if token else None

    if not user:
        return redirect('/login')

    return render_template('index.html', username=user['username'])

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
            log_auth_attempt(username_input, False, request.remote_addr)

        elif user['password'] != hash_password(password):
            time.sleep(SLOW_DELAY)
            error = error_message + '<!-- id:1 padding -------------- -->'
            log_auth_attempt(username_input, False, request.remote_addr)

        else:
            role = user.get('role', 'user')
            token = generate_token(username_input, role)

            resp = make_response(redirect('/2fa'))
            resp.set_cookie('session_id', token)
            log_auth_attempt(username_input, True, request.remote_addr, token)

            return resp

    return render_template('login.html', error=error, username=username_input)


@lobby_bp.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    submitted_username = ''
    if request.method == 'POST':
        submitted_username = request.form.get('username', '')
        password = request.form.get('password', '')

        users = load_users()

        if any(u['username'] == submitted_username for u in users):
            time.sleep(1.2)
            message = f"User `{submitted_username}` already exists. <!-- reg:0 -->"
        else:
            add_pending_user(submitted_username, password)
            message = f"Registration request received for `{submitted_username}`. <!-- reg:1 padding --------- -->"


    return render_template('register.html', message=message, username=submitted_username)

@lobby_bp.route('/2fa', methods=['GET', 'POST'])
def two_fa():
    token = request.cookies.get('session_id')
    user = decode_token(token) if token else None

    if not user:
        return redirect('/login')

    error = ''
    if request.method == 'POST':
        code_input = request.form.get('code', '')
        if code_input == '1337':
            return redirect('/')
        else:
            time.sleep(0.5)
            error = 'Invalid 2FA code. <!-- 2fa:0 -->'

    return render_template('2fa.html', error=error)


@lobby_bp.route('/download/nicks.txt')
def download_nicks():
    return send_file(
        DATA_DIR / 'nicks.txt',
        as_attachment=True,
        download_name='nicks.txt'
    )


@lobby_bp.route('/download/rockyou.txt')
def download_rockyou():
    return send_file(
        DATA_DIR / 'rockyou.txt',
        as_attachment=True,
        download_name='rockyou.txt'
    )

@lobby_bp.route('/download/readme.txt')
def download_readme():
    return send_file(
        DATA_DIR / 'readme.txt',
        as_attachment=True,
        download_name='readme.txt'
    )