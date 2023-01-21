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
    #TODO: what if key already exists
    return flask.render_template("insert.html", **context)

@kvpair.app.route('/delete/', methods=['GET', 'POST'])
def delete_kvpair():
    # Connect to database
    connection = kvpair.model.get_db()

    # Query database
    context = {}
    if flask.request.method == "POST":
        key = flask.request.form.get('key')
        connection.execute(
            "DELETE FROM kvpairs WHERE key = ?", (key,))
    #TODO: what if key does not exist
    return flask.render_template("delete.html", **context)

@kvpair.app.route('/deleteall/', methods=['GET', 'POST'])
def delete_all_kvpairs():
    # Connect to database
    connection = kvpair.model.get_db()

    # Query database
    context = {}
    if flask.request.method == "POST":
        key = flask.request.form.get('key')
        connection.execute("DELETE FROM kvpairs")
    return flask.render_template("deleteall.html", **context)

@kvpair.app.route('/getvalue/', methods=['GET', 'POST'])
def get_value():
    # Connect to database
    connection = kvpair.model.get_db()

    # Query database
    context = {"value": ""}
    if flask.request.method == "POST":
        key = flask.request.form.get('key')
        cur = connection.execute("SELECT value "
            "FROM kvpairs WHERE key = ?",(key,))
        value = cur.fetchone()
        print("!!!", value)
        context = {"value": value}
    return flask.render_template("getvalue.html", **context)