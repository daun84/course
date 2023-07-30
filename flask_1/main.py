import flask
from flask import url_for, session, request, g, redirect

from controllers.ControllerAuthentication import ControllerAuthentication
from controllers.ControllerPosts import ControllerPosts

from database import ModelBase, engine, Session

from models.ModelUser import ModelUser


app = flask.Flask(__name__, template_folder='views')
app.secret_key = 'a75c3e474eed90c68a9a12971769bc6dc0f4865d05b84c2911' # os.urandom(25).hex()


@app.before_request
def before_request():
    g.user = None
    g.db_session = Session()
    if 'user' in session:
        username = session['user']
        g.user = g.db_session.query(ModelUser).filter_by(user_name=username).first()


@app.teardown_request
def teardown_request(exception=None):
    db_session = g.pop('db_session', None)
    if db_session is not None:
        db_session.close()


app.register_blueprint(ControllerAuthentication.blueprint)
app.register_blueprint(ControllerPosts.blueprint)


@app.route('/')
def home():
    return redirect(url_for('posts.published_posts'))


if __name__ == '__main__':
    ModelBase.metadata.create_all(engine)
    app.run(debug=True)

# TODO search bar
# TODO comments
# TODO profile pages
# TODO root users

