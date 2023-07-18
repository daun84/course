import flask
from flask_login import login_user, logout_user, current_user
from flask import request, redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash

from models.ModelUser import ModelUser

from controllers.ControllerDatabase import ControllerDatabase
from controllers.ControllerUser import ControllerUser

from login_manager import login_manager


class ControllerAuthentication:
    blueprint = flask.Blueprint("authentication", __name__)

    @staticmethod
    @login_manager.user_loader
    def user_loader(user_id):
        user = ControllerDatabase.get_user(user_id)
        conn = None
        if user is not None:
            conn = ControllerUser(user)
        return conn


    @staticmethod
    @blueprint.route('/')
    def home():
        return render_template('home.html')

    
    @staticmethod
    @blueprint.route('/register', methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            repeat_password = request.form.get("repeat_password")

            if ControllerDatabase.get_user(username) is not None:
                flash("Account with this username already exists", category="error")
            elif password != repeat_password:
                flash("Passwords must be the same", category="error")
            else:
                user = ModelUser(username, password)
                ControllerDatabase.register_user(user)
                return redirect(url_for('authentication.login'))

        return render_template('registration.html')

    
    @staticmethod
    @blueprint.route('/login', methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            user = ControllerDatabase.get_user(username)

            if user is None:
                flash("This user does not exist", category="error")
            elif not check_password_hash(user.password, password):
                flash("Wrong password", category="error")
            else:
                login_user(ControllerUser(user))
                return redirect(url_for('authentication.home'))


        return render_template('login.html')

    
    @staticmethod
    @blueprint.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('authentication.home'))