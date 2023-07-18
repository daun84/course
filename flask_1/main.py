import flask
from flask import url_for, session, request
from flask_login import LoginManager, current_user

from login_manager import login_manager

from controllers.ControllerAuthentication import ControllerAuthentication
from controllers.ControllerDatabase import ControllerDatabase

app = flask.Flask(__name__, template_folder='views')
app.config['SECRET_KEY'] = 'aboba'

app.register_blueprint(ControllerAuthentication.blueprint)

login_manager.init_app(app)

if __name__ == '__main__':
    ControllerDatabase.setup_database()
    app.run(debug=True)
