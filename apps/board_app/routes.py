from flask import request, render_template, redirect

from apps.board_app import board_bp
from apps.board_app.logic.session import validate_token


@board_bp.route('/board')
def board():
    token = request.cookies.get('session_id')
    user = validate_token(token)

    if not user:
        return redirect('/login')

    return render_template('board.html', user=user, page='board')

