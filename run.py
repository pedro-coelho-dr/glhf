from flask import Flask
from apps.lobby_app import lobby_bp
from apps.user_app import user_bp
from apps.direct_app import direct_bp
from apps.board_app import board_bp

app = Flask(__name__)
app.secret_key = 'super_insecure_lobby_key'

app.register_blueprint(lobby_bp)
app.register_blueprint(user_bp)
app.register_blueprint(direct_bp)
app.register_blueprint(board_bp)


if __name__ == '__main__':
    app.run(debug=False, port=1337)
