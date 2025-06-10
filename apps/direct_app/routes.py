from flask import request, render_template, redirect

from apps.direct_app import direct_bp
from apps.direct_app.logic.session import validate_token


@direct_bp.route('/direct')
def direct():
    token = request.cookies.get('session_id')
    user = validate_token(token)

    if not user:
        return redirect('/login')

    return render_template('direct.html', user=user, page='direct')

