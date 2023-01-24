import re
import bs4


def test_index(client):
    """Test homepage"""
    response = client.get(
        "/"
    )
    assert b"request all the current contents of the key-value structure" in response.data
    assert response.status_code == 200

def test_get_all_kvpairs(client):
    """Test if getall button is working 
    "keya valuea" is originally in db, refer to sql/data.sql"""
    response = client.post(
        "/kvpair/getall/",
        data={
            "operation": "getall"
        }
    )
    assert b"keya valuea" in response.data
    assert response.status_code == 200

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
            "value": "differnet_test_value",
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
    assert response.status_code == 200

def test_delete_kvpair(client):
    """Test deleting a kvpair"""
    # delete a kvpair
    client.post(
        "/kvpair/delete/",
        data={
            "key": "test_key",
            "operation": "delete"
        }
    )
    # test if deleting is successful
    response = client.post(
        "/kvpair/getall/",
        data={
            "operation": "getall"
        }
    )
    assert b"test_key test_value" not in response.data

    # delete a key that does not exist
    client.post(
        "/kvpair/delete/",
        data={
            "key": "test_key",
            "operation": "delete"
        }
    )
    # test if the request is ignored and server is not down
    assert response.status_code == 200

def test_delete_all_kvpairs(client):
    """Test deleting all kvpairs"""
    # insert two kvpairs
    client.post(
        "/kvpair/insert/",
        data={
            "key": "test_key_1",
            "value": "test_value_1",
            "operation": "insert"
        }
    )
    client.post(
        "/kvpair/insert/",
        data={
            "key": "test_key_2",
            "value": "test_value_2",
            "operation": "insert"
        }
    )
    # delete all kvpairs
    client.post(
        "/kvpair/deleteall/",
        data={
            "operation": "deleteall"
        }
    )
    # test if deleting is successful
    response = client.post(
        "/kvpair/getall/",
        data={
            "operation": "getall"
        }
    )
    assert b"test_key_1 test_value_1" not in response.data
    assert b"test_key_2 test_value_2" not in response.data

def test_get_value_for_key(client):
    """Test get value for a key that the user specified"""
    # insert a kvpair
    client.post(
        "/kvpair/insert/",
        data={
            "key": "test_key_3",
            "value": "test_value_3",
            "operation": "insert"
        }
    )
    # get value for key "test_key_3"
    response = client.post(
        "/kvpair/getvalue/",
        data={
            "key": "test_key_3",
            "operation": "getvalue"
        }
    )
    # test if the corresponding value is displayed
    assert b"test_value_3" in response.data
    # get value for key does not exist
    response = client.post(
        "/kvpair/getvalue/",
        data={
            "key": "key_not_existing",
            "operation": "getvalue"
        }
    )
    # test "None" is displayed and server is not down
    assert b"None" in response.data
    assert response.status_code == 200
