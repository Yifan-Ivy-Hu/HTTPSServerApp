"""
fileuploader views.

URLs include:
/fileupload/getfilelist/
/fileupload/uploadfile/
/fileupload/downloadfile/
/fileupload/downloads/<path:filename>
"""
import flask
import httpsserver
from fileinput import filename
import shutil
import os

@httpsserver.app.route('/fileupload/getfilelist/', methods=['GET', 'POST'])
def get_list():
    # Connect to database
    connection = httpsserver.model.get_db()

    # Query database to get all filenames
    context = {}
    if flask.request.method == "POST":
        cur = connection.execute(
            "SELECT filename "
            "FROM files ",
        )
        files = cur.fetchall()
        context = {"files": files}
    return flask.render_template("fileupload/getfilelist.html", **context)

@httpsserver.app.route('/fileupload/uploadfile/', methods=['GET', 'POST'])
def upload_file():
    # source: https://www.geeksforgeeks.org/how-to-upload-file-in-python-flask/
    # Connect to database
    connection = httpsserver.model.get_db()

    context = {"fileExisted" : False}
    if flask.request.method == "POST":
        f = flask.request.files['file']

        # if filename already exists, request ignored
        cur = connection.execute("SELECT filename "
            "FROM files WHERE filename = ?",(f.filename,))
        existedFile = cur.fetchone()
        if existedFile != None:
            context = {"fileExisted" : True}
            return flask.render_template("fileupload/uploadfile.html", **context)
        
        # save file to root dir
        f.save(f.filename)
        # move file from root dir to /var/uploads
        updatedFilePath = os.path.join(httpsserver.app.config["UPLOAD_FOLDER"], f.filename)
        shutil.move(f.filename, updatedFilePath)
        # insert filename to database
        connection.execute(
            "INSERT INTO files(filename) "
            "VALUES (?)", (f.filename,))
    return flask.render_template("fileupload/uploadfile.html", **context)

@httpsserver.app.route('/fileupload/downloadfile/', methods=['GET', 'POST'])
def download_file():
    # Connect to database
    connection = httpsserver.model.get_db()

    # Query database to get all filenames
    context = {}
    cur = connection.execute(
        "SELECT filename "
        "FROM files ",
    )
    files = cur.fetchall()
    context = {"files": files}

    if flask.request.method == "POST":
        filenameToDownload = flask.request.form.get('filename')

        # if filename not found, request ignored
        cur = connection.execute(
            "SELECT filename "
            "FROM files "
            "WHERE filename = ?", (filenameToDownload,)
        )
        fileWithSameFilename = cur.fetchone()
        if fileWithSameFilename == None:
            return flask.render_template("fileupload/downloadfile.html", **context)
        # if file with the submitted file name exists, redirect to downloads/<path:filename> to download as attachment
        return flask.redirect(flask.url_for('download', filename=filenameToDownload))
    return flask.render_template("fileupload/downloadfile.html", **context)

@httpsserver.app.route('/fileupload/downloads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # /downloadfile/ will be redirected to /fileupload/downloads/<path:filename> for downloading a file as an attachment
    # source: https://www.educative.io/answers/how-to-download-files-in-flask

    uploadsFolder = httpsserver.app.config['UPLOAD_FOLDER']
    # file downloaded
    return flask.send_from_directory(directory=uploadsFolder, path=filename, as_attachment=True)