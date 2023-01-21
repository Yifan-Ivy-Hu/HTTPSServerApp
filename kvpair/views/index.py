"""
kvpair index (main) view.

URLs include:
/
refer: https://eecs485staff.github.io/p2-insta485-serverside/setup_flask.html
"""
import flask
import kvpair


@kvpair.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    # Connect to database
    connection = kvpair.model.get_db()

    # Query database
    cur = connection.execute(
        "SELECT key, value "
        "FROM kvpairs ",
    )
    kvpairs = cur.fetchall()
    context = {"kvpairs": kvpairs}
    return flask.render_template("index.html", **context)

@kvpair.app.route('/insert/', methods=['GET', 'POST'])
def insert_kvpair():
    # Connect to database
    connection = kvpair.model.get_db()

    # Query database
    context = {}
    if flask.request.method == "POST":
        key = flask.request.form.get('key')
        value = flask.request.form.get('value')
        connection.execute(
            "INSERT INTO kvpairs(key, value) "
            "VALUES (?, ?)", (key, value,))
    return flask.render_template("insert.html", **context)