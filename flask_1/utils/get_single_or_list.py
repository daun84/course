from functools import wraps

from flask import g, redirect, url_for

from loguru import logger


def get_single_or_list(original_function):

    @wraps(original_function)
    def wrapped_function(*args, **kwargs):
        result = original_function(*args, **kwargs)

        get_one = kwargs.get('get_one', False)
    
        if get_one and len(result) == 1:
            result = result[0]
        return result
    
    return wrapped_function
