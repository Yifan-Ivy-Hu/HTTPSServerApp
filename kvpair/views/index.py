"""
kvpair index (main) view.

URLs include:
/
refer: https://eecs485staff.github.io/p2-insta485-serverside/setup_flask.html
"""
import flask
import kvpair
from fileinput import filename
import shutil
import os

@kvpair.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""

    return flask.render_template("index.html")

@kvpair.app.route('/getall/', methods=['GET', 'POST'])
def get_all():
    # Connect to database
    connection = kvpair.model.get_db()

    # Query database
    context = {}
    if flask.request.method == "POST":
        cur = connection.execute(
            "SELECT key, value "
            "FROM kvpairs ",
        )
        kvpairs = cur.fetchall()
        context = {"kvpairs": kvpairs}
    return flask.render_template("getall.html", **context)

@kvpair.app.route('/insert/', methods=['GET', 'POST'])
def insert_kvpair():
    # Connect to database
    connection = kvpair.model.get_db()

    # Query database
    context = {}
    if flask.request.method == "POST":
        key = flask.request.form.get('key')
        # if key already exists, request ignored
        cur = connection.execute("SELECT value "
            "FROM kvpairs WHERE key = ?",(key,))
        existedValue = cur.fetchone()
        if existedValue != None:
            return flask.render_template("insert.html", **context)
        value = flask.request.form.get('value')
        connection.execute(
            "INSERT INTO kvpairs(key, value) "
            "VALUES (?, ?)", (key, value,))

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
    # if key does not exist, request ignored
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
        context = {"value": value}
    return flask.render_template("getvalue.html", **context)

@kvpair.app.route('/getfilelist/', methods=['GET', 'POST'])
def get_list():
    # Connect to database
    connection = kvpair.model.get_db()

    # Query database
    context = {}
    if flask.request.method == "POST":
        cur = connection.execute(
            "SELECT filename "
            "FROM files ",
        )
        files = cur.fetchall()
        context = {"files": files}
    return flask.render_template("fileupload/getfilelist.html", **context)

@kvpair.app.route('/uploadfile/', methods=['GET', 'POST'])
def upload_file():
    # source: https://www.geeksforgeeks.org/how-to-upload-file-in-python-flask/
    # Connect to database
    connection = kvpair.model.get_db()

    context = {}
    if flask.request.method == "POST":
        f = flask.request.files['file']
        # save file to root dir
        f.save(f.filename)
        # move file from root dir to /var/uploads
        updatedFilePath = os.path.join(kvpair.app.config["UPLOAD_FOLDER"], f.filename)
        shutil.move(f.filename, updatedFilePath)

        connection.execute(
            "INSERT INTO files(filename) "
            "VALUES (?)", (f.filename,))
    return flask.render_template("fileupload/uploadfile.html", **context)

@kvpair.app.route('/downloadfile/', methods=['GET', 'POST'])
def download_file():
    # Connect to database
    connection = kvpair.model.get_db()

    # Query database
    context = {}
    cur = connection.execute(
        "SELECT filename "
        "FROM files ",
    )
    files = cur.fetchall()
    context = {"files": files}
    if flask.request.method == "POST":
        filenameToDownload = flask.request.form.get('filename')
        return flask.redirect(flask.url_for('download', filename=filenameToDownload))
    return flask.render_template("fileupload/downloadfile.html", **context)

@kvpair.app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # source: https://www.educative.io/answers/how-to-download-files-in-flask

    uploadsFolder = kvpair.app.config['UPLOAD_FOLDER']
    # file downloaded
    return flask.send_from_directory(directory=uploadsFolder, path=filename, as_attachment=True)