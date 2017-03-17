"""Control access to Flask endpoints."""

import inspect

import flask

ABORT_FN = "flask_access_abort_fn"
CURRENT_USER = "flask_access_current_user"


def _abort():
    """Call a custom abort function if defined, else flask's 403."""
    flask.current_app.config.get(ABORT_FN, lambda: flask.abort(403))()


def _current_user():
    """Return the current user from the app config."""
    user = flask.current_app.config[CURRENT_USER]
    if inspect.isfunction(user):
        user = user()
    return user


def require(access):
    """Return a decorator to control access to a Flask endpoint."""
    def decorator(original_fn):
        def new_fn(*args, **kwargs):
            user = _current_user()
            if hasattr(user, "has_access") and user.has_access(access):
                return original_fn(*args, **kwargs)
            _abort()
        return new_fn
    return decorator