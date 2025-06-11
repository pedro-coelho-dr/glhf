from flask import request, render_template, redirect

from apps.board import board_bp
from common.session import get_current_user


@board_bp.route('/board')
def board():
    current = get_current_user()
    if not current:
        return redirect("/login")

    return render_template('board.html', user=current, page='board')

