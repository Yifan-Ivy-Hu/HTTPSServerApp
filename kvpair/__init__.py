"""kvpair package initializer. source of this file: https://eecs485staff.github.io/p2-insta485-serverside/setup_flask.html"""
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Read settings from config module (kvpair/config.py)
app.config.from_object('kvpair.config')

# Overlay settings read from a Python file whose path is set in the environment
# variable KVPAIR_SETTINGS. Setting this environment variable is optional.
# Docs: http://flask.pocoo.org/docs/latest/config/
#
# EXAMPLE:
# $ export KVPAIR_SETTINGS=secret_key_config.py
app.config.from_envvar('KVPAIR_SETTINGS', silent=True)

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import kvpair.views  # noqa: E402  pylint: disable=wrong-import-position
import kvpair.model  # noqa: E402  pylint: disable=wrong-import-position