from functools import wraps

from flask import abort
from flask_login import logout_user, current_user


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    return wrapper