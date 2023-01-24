import re
import bs4


def test_get_all(client):
    response = client.get(
        "/"
    )
    assert b"request all the current contents of the key-value structure" in response.data

def get_all(client):
    response = client.post(
        "/getall/"
    )
    assert b"request all the current contents of the key-value structure" in response.data