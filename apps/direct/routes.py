from flask import request, render_template, redirect

from apps.direct import direct_bp
from common.session import get_current_user


@direct_bp.route('/direct')
def direct():
    current = get_current_user()
    if not current:
        return redirect("/login")

    return render_template('direct.html', user=current, page='direct')

