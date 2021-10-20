from flask import Blueprint, render_template, request, flash, redirect, url_for

from website import views

from .models import User
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from flask_login import login_user, login_required, logout_user, current_user

#to split up end points

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")


        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("incorrecr password", category="error")
        else:
            flash("no such email", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up",  methods=["GET", "POST"])
def sign_up():
    if(request.method == "POST"):
        email = request.form.get("email")
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()

        if user:
             flash("email already exist", category="error")
        elif len(email)<4:
            flash("email length should be at least 4 characters", category="error")
        elif len(name)<2:
            flash("name length should be at least 2 characters", category="error")
        elif password1 != password2:
            flash("passwords should be same", category="error")
        elif len(password1)< 7:
            flash("password length should be at least 7 characters", category="error")
        else:
            #add users
            new_user = User(email=email, name = name, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("account created", category="success")
            return redirect(url_for("views.home"))
            
    return render_template("sign_up.html", user=current_user)