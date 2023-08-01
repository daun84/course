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
        result = render_template('registration.html')

        if request.method == "POST":

            username = request.form.get("username").strip()
            email = request.form.get("email").strip()
            password = request.form.get("password").strip()
            repeat_password = request.form.get("repeat_password").strip()

            user = g.db_session.query(ModelUser).filter_by(user_name=username).first()

            existing_email = g.db_session.query(ModelUser).filter_by(user_email=email).first()

            if user is not None:
                error = "Account with this username already exists"
                result = render_template('registration.html', error=error)
            elif password != repeat_password:
                error = "Passwords must be the same"
                result = render_template('registration.html', error=error)
            elif existing_email:
                error = "This email is already being used"      
                result = render_template('registration.html', error=error)
            else:
                user = ModelUser(
                    user_name=username,
                    user_email=email,
                    user_password=generate_password_hash(password)
                    )
                g.db_session.add(user)
                g.db_session.commit()
                result = redirect(url_for('authentication.login'))

        return result

    
    @staticmethod
    @blueprint.route('/login', methods=["GET", "POST"])
    def login():
        result = render_template('login.html')

        if request.method == "POST":

            username = request.form.get("username").strip()
            password = request.form.get("password").strip()

            user = g.db_session.query(ModelUser).filter_by(user_name=username).first()
            
            if user is None:
                error = "This user does not exist"
                result = render_template('login.html', error=error)
            elif not check_password_hash(user.user_password, password):
                error = "Wrong password"
                result = render_template('login.html', error=error)
            else:
                session['user'] = user.user_name
                result = redirect(url_for('posts.published_posts'))

        return result

    
    @staticmethod
    @blueprint.route('/logout')
    def logout():
        session.pop('user', default=None)
        return redirect(url_for('posts.published_posts'))