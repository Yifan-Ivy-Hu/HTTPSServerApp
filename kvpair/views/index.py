"""
index (main) view.

URLs include:
/
source: https://eecs485staff.github.io/p2-insta485-serverside/setup_flask.html
"""
import flask
import kvpair

@kvpair.app.route('/', methods=['GET'])
def show_index():
    """Display all the routes for both servers."""
    return flask.render_template("index.html")
