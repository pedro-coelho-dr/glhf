from flask import Flask, send_from_directory, request, redirect
from apps.lobby import lobby_bp
from apps.user import user_bp
from apps.direct import direct_bp
from apps.board import board_bp
from apps.root import root_bp
from common.resetdb import main as reset_database

app = Flask(__name__)
app.secret_key = 'super_insecure_lobby_key'

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/resetdb')
def resetdb():
    reset_database()
    referer = request.headers.get("Referer")
    return redirect(referer or "/")

app.register_blueprint(lobby_bp)
app.register_blueprint(user_bp)
app.register_blueprint(direct_bp)
app.register_blueprint(board_bp)
app.register_blueprint(root_bp)


if __name__ == '__main__':
    app.run(debug=False, port=1337)
