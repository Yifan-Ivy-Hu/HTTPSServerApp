import re
import bs4


def test_index(client):
    """Test homepage"""
    response = client.get(
        "/"
    )
    assert b"request all the current contents of the key-value structure" in response.data

def test_get_all(client):
    """Test if getall button is working ("keya valuea" is originally in db, refer to sql/data.sql)"""
    response = client.post(
        "/kvpair/getall/",
        data={
            "operation": "getall"
        }
    )
    assert b"keya valuea" in response.data

def test_insert_kvpair(client):
    """Test inserting a kvpair"""
    # insert a kvpair
    client.post(
        "/kvpair/insert/",
        data={
            "key": "test_key",
            "value": "test_value",
            "operation": "insert"
        }
    )
    # test if inserting is successful
    response = client.post(
        "/kvpair/getall/",
        data={
            "operation": "getall"
        }
    )
    assert b"test_key test_value" in response.data

    # insert the same key
    client.post(
        "/kvpair/insert/",
        data={
            "key": "test_key",
            "value": "test_value",
            "operation": "insert"
        }
    )
    # test if the request is ignored and server is not down
    response = client.post(
        "/kvpair/getall/",
        data={
            "operation": "getall"
        }
    )
    assert b"test_key test_value" in response.data