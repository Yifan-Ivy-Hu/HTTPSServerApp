"""
kvpair views.

URLs include:
/kvpair/getall/
/kvpair/insert/
/kvpair/delete/
/kvpair/deleteall/
/kvpair/getvalue/
"""
import flask
import httpsserver

@httpsserver.app.route('/kvpair/getall/', methods=['GET', 'POST'])
def get_all():
    # Connect to database
    connection = httpsserver.model.get_db()

    context = {}
    if flask.request.method == "POST":
        cur = connection.execute(
            "SELECT key, value "
            "FROM kvpairs ",
        )
        kvpairs = cur.fetchall()
        context = {"kvpairs": kvpairs}
    return flask.render_template("keyvaluepair/getall.html", **context)

@httpsserver.app.route('/kvpair/insert/', methods=['GET', 'POST'])
def insert_kvpair():
    # Connect to database
    connection = httpsserver.model.get_db()

    context = {}
    if flask.request.method == "POST":
        key = flask.request.form.get('key')

        # if key already exists, request ignored
        cur = connection.execute("SELECT value "
            "FROM kvpairs WHERE key = ?",(key,))
        existedValue = cur.fetchone()
        if existedValue != None:
            return flask.render_template("keyvaluepair/insert.html", **context)
        value = flask.request.form.get('value')
        connection.execute(
            "INSERT INTO kvpairs(key, value) "
            "VALUES (?, ?)", (key, value,))

    return flask.render_template("keyvaluepair/insert.html", **context)

@httpsserver.app.route('/kvpair/delete/', methods=['GET', 'POST'])
def delete_kvpair():
    # Connect to database
    connection = httpsserver.model.get_db()

    context = {}
    if flask.request.method == "POST":
        key = flask.request.form.get('key')
        connection.execute(
            "DELETE FROM kvpairs WHERE key = ?", (key,))
    # if key does not exist, request ignored
    return flask.render_template("keyvaluepair/delete.html", **context)

@httpsserver.app.route('/kvpair/deleteall/', methods=['GET', 'POST'])
def delete_all_kvpairs():
    # Connect to database
    connection = httpsserver.model.get_db()

    context = {}
    if flask.request.method == "POST":
        key = flask.request.form.get('key')
        connection.execute("DELETE FROM kvpairs")
    return flask.render_template("keyvaluepair/deleteall.html", **context)

@httpsserver.app.route('/kvpair/getvalue/', methods=['GET', 'POST'])
def get_value():
    # Connect to database
    connection = httpsserver.model.get_db()

    context = {"value": ""}
    if flask.request.method == "POST":
        key = flask.request.form.get('key')
        cur = connection.execute("SELECT value "
            "FROM kvpairs WHERE key = ?",(key,))
        value = cur.fetchone()
        context = {"value": value}
    return flask.render_template("keyvaluepair/getvalue.html", **context)

