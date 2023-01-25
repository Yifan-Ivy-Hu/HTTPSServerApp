import io

def test_get_file_list(client):
    """Test if getting file list is working.
    test.txt is originally in db, refer to sql/data.sql"""
    response = client.post(
        "/fileupload/getfilelist/",
        data={
            "operation": "getfilelist"
        }
    )
    assert b"test.txt" in response.data

def test_upload_file(client):
    """Test if uploading file is working.
    source: https://stackoverflow.com/questions/35684436/testing-file-uploads-in-flask"""
    # upload a file
    response = client.post(
        "/fileupload/uploadfile/",
        data={
            "file": (io.BytesIO(b"abcdef"), 'test.jpg'),
            "operation": "upload"
        }
    )
    # test if the file is uploaded successfully
    response = client.post(
        "/fileupload/getfilelist/",
        data={
            "operation": "getfilelist"
        }
    )
    assert b"test.jpg" in response.data

    # upload a file with the same filename
    response = client.post(
        "/fileupload/uploadfile/",
        data={
            "file": (io.BytesIO(b"abcdef"), 'test.jpg'),
            "operation": "upload"
        }
    )
    # test if the request is ignored and server is not down
    response = client.post(
        "/fileupload/getfilelist/",
        data={
            "operation": "getfilelist"
        }
    )
    assert b"test.jpg" in response.data
    assert response.status_code == 200

def test_download_file(client):
    """Test if downloading file is working."""
    # download a file
    response = client.post(
        "/fileupload/downloadfile/",
        data={
            "filename": "test.txt",
            "operation": "getfile"
        }
    )
    # test if redirection happens
    assert response.status_code == 302
    assert response.location == "/fileupload/downloads/test.txt"

    # ask to download a file that does not exist
    response = client.post(
        "/fileupload/downloadfile/",
        data={
            "filename": "fileNotExist.txt",
            "operation": "getfile"
        }
    )
    # test if the request is ignored and server is not down
    assert response.status_code == 200