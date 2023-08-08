from functools import wraps

from flask import g, redirect, url_for

from controllers.ControllerDatabase import ControllerDatabase

from loguru import logger

def login_reqired(original_function):

    @wraps(original_function)
    def wrapped_function(*args, **kwargs):
        url_slug = kwargs.get('url_slug', None)

        result = None
        post = None

        if url_slug:
            post = ControllerDatabase.get_posts(url_slug=url_slug, get_one=True)
        
        if g.user is None:
            result = redirect(url_for('authentication.login'))
        elif (url_slug is not None) and g.user.user_id is not post.post_author_id:
            result = redirect(url_for('authentication.login'))
        else:
            result = original_function(*args, **kwargs)
        return result
    
    return wrapped_function