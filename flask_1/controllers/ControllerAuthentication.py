import flask
from flask import request, redirect, url_for, render_template, flash, session, g
from werkzeug.security import check_password_hash, generate_password_hash

from models.ModelUser import ModelUser

from controllers.ControllerDatabase import ControllerDatabase

from database import Session

from loguru import logger

class ControllerAuthentication:
    blueprint = flask.Blueprint("authentication", __name__)
    
    @staticmethod
    @blueprint.route('/register', methods=["GET", "POST"])
    def register():
        result = None

        try:                  
            result = render_template('registration.html')

            if request.method == "POST":

                username = request.form.get("username").strip()
                email = request.form.get("email").strip()
                password = request.form.get("password").strip()
                repeat_password = request.form.get("repeat_password").strip()

                user = ControllerDatabase.get_user(username=username)

                existing_email = ControllerDatabase.get_user(email=email)

                if user is not None:
                    error = "Account with this username already exists"
                    result = render_template('registration.html', error_message=error)
                elif password != repeat_password:
                    error = "Passwords must be the same"
                    result = render_template('registration.html', error_message=error)
                elif existing_email:
                    error = "This email is already being used"      
                    result = render_template('registration.html', error_message=error)
                else:
                    user = ModelUser(
                        user_name=username,
                        user_email=email,
                        user_password=generate_password_hash(password)
                        )
                    ControllerDatabase.insert_user(user)

                    success_message = "User successfully created"

                    result = redirect(url_for('authentication.login', success_message=success_message))
        except Exception as e:
            logger.error(e)
            result = render_template('error.html', error_code=500, error_message="Internal error")

        return result

    
    @staticmethod
    @blueprint.route('/login', methods=["GET", "POST"])
    def login():
        result = None

        try:
            success_message = request.args.get('success_message')
            result = render_template('login.html', success_message=success_message)

            if request.method == "POST":

                username = request.form.get("username").strip()
                password = request.form.get("password").strip()

                user = ControllerDatabase.get_user(username=username)
                
                if user is None:
                    error = "This user does not exist"
                    result = render_template('login.html', error_message=error)
                elif not check_password_hash(user.user_password, password):
                    error = "Wrong password"
                    result = render_template('login.html', error_message=error)
                else:
                    session['user'] = user.user_name

                    success_message = "You successfully logged in"

                    result = redirect(url_for('posts.published_posts', success_message=success_message))
        except Exception as e:
            logger.error(e)
            result = render_template('error.html', error_code=500, error_message="Internal error")

        return result

    
    @staticmethod
    @blueprint.route('/logout')
    def logout():
        session.pop('user', default=None)
        return redirect(url_for('posts.published_posts'))