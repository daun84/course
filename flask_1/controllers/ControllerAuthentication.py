import flask
from flask import request, redirect, url_for, render_template, flash, session, g
from werkzeug.security import check_password_hash, generate_password_hash

from models.ModelUser import ModelUser

from database import Session


class ControllerAuthentication:
    blueprint = flask.Blueprint("authentication", __name__)
    
    @staticmethod
    @blueprint.route('/register', methods=["GET", "POST"])
    def register():
        if request.method == "POST":

            username = request.form.get("username").strip()
            email = request.form.get("email").strip()
            password = request.form.get("password").strip()
            repeat_password = request.form.get("repeat_password").strip()

            user = g.db_session.query(ModelUser).filter_by(user_name=username).first()

            existing_email = g.db_session.query(ModelUser).filter_by(user_email=email).first()

            if user is not None:
                flash("Account with this username already exists", category="error")
            elif password != repeat_password:
                flash("Passwords must be the same", category="error")
            elif existing_email:
                flash("This email is already being used", category="error")
            else:
                user = ModelUser(
                    user_name=username,
                    user_email=email,
                    user_password=generate_password_hash(password)
                    )
                g.db_session.add(user)
                g.db_session.commit()
                return redirect(url_for('authentication.login'))

        return render_template('registration.html')

    
    @staticmethod
    @blueprint.route('/login', methods=["GET", "POST"])
    def login():
        if request.method == "POST":

            username = request.form.get("username").strip()
            password = request.form.get("password").strip()

            user = g.db_session.query(ModelUser).filter_by(user_name=username).first()
            
            if user is None:
                flash("This user does not exist", category="error")
            elif not check_password_hash(user.user_password, password):
                flash("Wrong password", category="error")
            else:
                session['user'] = user.user_name
                return redirect(url_for('posts.published_posts'))

        return render_template('login.html')

    
    @staticmethod
    @blueprint.route('/logout')
    def logout():
        session.pop('user', default=None)
        return redirect(url_for('posts.published_posts'))