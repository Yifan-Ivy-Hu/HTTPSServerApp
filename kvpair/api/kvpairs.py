"""REST API for kvpairs."""
import flask
import kvpair


@kvpair.app.route('/api/kvpairs/', methods=['GET', 'POST', 'DELETE'])
def get_kvpairs():
    """Return all kvpairs.
    """
    # Connect to database
    connection = kvpair.model.get_db()

    # Query database
    cur = connection.execute(
        "SELECT key, value "
        "FROM kvpairs ",
    )
    kvpairs = cur.fetchall()
    context = {"kvpairs": kvpairs}
    return flask.jsonify(**context)

@kvpair.app.route('/api/kvpairs/<int:key>', methods=['GET', 'POST', 'DELETE'])
def get_kvpair():
    """Return all kvpairs.
    """
    # Connect to database
    connection = kvpair.model.get_db()

    # Query database
    # if flask.request.method == 'DELETE':
    #     connection.execute(
    #         "DELETE FROM kvpairs WHERE key = {}".format(key)
    #     )
    #     context = {}
    #     return (flask.jsonify(**context), 204)
    # else if flask.request.method == 'POST':
    #     connection.execute(
    #         "INSERT INTO kvpairs(key, value)"
    #         "VALUES ({}, {});"
    #     )
    #     context = {
    #         "logname": flask.session['username'],
    #         "postid": postid_url_slug
    #     }
    #     return (flask.jsonify(**context), 201)
    cur = connection.execute(
        "SELECT key, value "
        "FROM kvpairs where key = {}", (key,)
    )
    kvpairs = cur.fetchone()
    context = {"kvpairs": kvpairs}
    return (flask.jsonify(**context), 200)
