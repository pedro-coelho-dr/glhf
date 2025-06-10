from flask import request, render_template, redirect
from apps.user_app import user_bp
from apps.user_app.logic.session import (
    validate_token,
    get_user_by_id,
    get_user_by_username,
)


@user_bp.route("/user/<username>")
def public_user(username):
    token = request.cookies.get("session_id")
    current_user = validate_token(token)
    if not current_user:
        return redirect("/login")

    user = get_user_by_username(username)
    if not user:
        return render_template("user_not_found.html", username=username), 404

    return render_template("public_profile.html", user=user, page="user")


@user_bp.route("/user")
def user_by_id():
    token = request.cookies.get("session_id")
    current_user = validate_token(token)
    if not current_user:
        return redirect("/login")

    user_id = request.args.get("id", type=int)
    if not user_id:
        return redirect("/")

    user = get_user_by_id(user_id)
    if not user:
        return render_template("user_not_found.html"), 404

    return render_template("public_profile.html", user=user, page="user")


@user_bp.route("/profile")
def profile():
    token = request.cookies.get("session_id")
    current_user = validate_token(token)
    if not current_user:
        return redirect("/login")

    real_user = get_user_by_id(current_user["user_id"])
    if not real_user:
        return render_template("user_not_found.html"), 404

    return render_template("edit_profile.html", user=real_user, page="user")

