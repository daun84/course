import flask
from flask import url_for, session, request, g, redirect

from controllers.ControllerAuthentication import ControllerAuthentication
from controllers.ControllerPosts import ControllerPosts
from controllers.ControllerDatabase import ControllerDatabase

from database import ModelBase, engine, Session

from models.ModelUser import ModelUser

from loguru import logger


app = flask.Flask(__name__, template_folder='views')
app.secret_key = 'a75c3e474eed90c68a9a12971769bc6dc0f4865d05b84c2911' # os.urandom(25).hex()


@app.before_request
def before_request():
    g.user = None
    g.db_session = Session()
    if 'user' in session:
        username = session['user']
        g.user = ControllerDatabase.get_user(username=username)


# cannot use session only in ControllerDatabase
# because then objects are not bounded to a session
# thus, we cannot load related objects
@app.teardown_request
def teardown_request(exception=None):
    try:
        g.db_session.commit()
    except Exception as e:
        logger.error(e)
        g.db_session.rollback()
    finally:
        g.db_session.close()


app.register_blueprint(ControllerAuthentication.blueprint)
app.register_blueprint(ControllerPosts.blueprint)

logger.add(
    "output.log",  
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}",
    level="INFO",
    rotation="10MB",
    compression="zip"
)


@app.route('/')
def home():
    return redirect(url_for('posts.published_posts'))


if __name__ == '__main__':
    ModelBase.metadata.create_all(engine)
    app.run(debug=True)

