from flask import Flask
from apps.lobby_app.routes import lobby_bp

app = Flask(__name__)
app.secret_key = 'super_insecure_lobby_key'

app.register_blueprint(lobby_bp)

if __name__ == '__main__':
    app.run(debug=False, port=1337)
