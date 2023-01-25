"""
Source: wget https://eecs485staff.github.io/p2-insta485-serverside/starter_files.tar.gz
Source: https://stackoverflow.com/questions/22736850/flask-module-import-failure-from-test-folder

Shared test fixtures.

Pytest will automatically run the client_setup_teardown() function before a
test.  A test should use "client" as an input, because the name of the fixture
is "client".

EXAMPLE:
>>> def test_simple(client):
>>>     response = client.get("/")
>>>     assert response.status_code == 200

Pytest docs:
https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
"""
import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

import subprocess
import pytest
import httpsserver


@pytest.fixture(name="client")
def client_setup_teardown():
    """
    Start a Flask test server with a clean database.

    Flask docs: https://flask.palletsprojects.com/en/1.1.x/testing/#testing
    """
    # Reset the database
    subprocess.run(["bin/httpsserverdb", "reset"], check=True)

    # Configure Flask test server
    httpsserver.app.config["TESTING"] = True

    # Transfer control to test.  The code before the "yield" statement is setup
    # code, which is executed before the test.  Code after the "yield" is
    # teardown code, which is executed at the end of the test.  Teardown code
    # is executed whether the test passed or failed.
    with httpsserver.app.test_client() as client:
        yield client

    # Reset the database. After running any test any of the changes made
    # to the database should be undone.
    subprocess.run(["bin/httpsserverdb", "reset"], check=True)
