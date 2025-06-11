from flask import request, render_template, redirect
from apps.user import user_bp

from common.session import (
    get_current_user,
    get_user_by_id,
    get_user_by_username,
)
from apps.user.logic.users import update_password, update_avatar_file, update_bio 


@user_bp.route("/user/<username>")
def public_user(username):
    current = get_current_user()
    if not current:
        return redirect("/login")
    user = get_user_by_username(username)
    if not user:
        return render_template("user_not_found.html", username=username), 404
    return render_template("public_profile.html", user=user, page="user")

@user_bp.route("/user")
def user_by_id():
    current = get_current_user()
    if not current:
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
    current = get_current_user()
    if not current:
        return redirect("/login")
    return render_template("edit_profile.html", user=current, page="user")


@user_bp.route("/profile/edit_password", methods=["POST"])
def edit_password():
    current = get_current_user()
    if not current:
        return redirect("/login")
    password = request.form.get("password")
    confirm = request.form.get("confirm")
    if not password or password != confirm:
        return redirect("/profile")
    update_password(current["id"], password)
    return redirect("/profile")

@user_bp.route("/profile/edit_avatar", methods=["POST"])
def edit_avatar():
    current = get_current_user()
    if not current:
        return redirect("/login")
    target_id = request.form.get("user_id", type=int)
    if not target_id:
        target_id = current["id"]

    file = request.files.get("avatar")
    if not file or file.filename == "":
        return redirect("/profile")

    update_avatar_file(target_id, file)
    return redirect("/profile")

@user_bp.route("/profile/edit_bio", methods=["POST"])
def edit_bio():
    current = get_current_user()
    if not current:
        return redirect("/login")
    target_id = request.form.get("user_id", type=int)
    if not target_id:
        target_id = current["id"]

    new_bio = request.form.get("bio", "")
    update_bio(target_id, new_bio)
    return redirect("/profile")
