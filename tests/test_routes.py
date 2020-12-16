import os
import json

import pytest

from app import app
import time


@pytest.fixture
def client():
    return app.test_client()


def test_get(client):
    """Expect a 200 response for supported GET operation"""
    response = client.get('/')
    assert response.status_code == 200


def test_post(client):
    """Expect a 200 response for supported POST operation"""
    response = client.post('/')
    assert response.status_code == 200


def test_rate_limiting(client):
    """Expect a subsequent response from the API to take longer than the defined rate limit time."""
    RATE_LIMITED_PAUSE_SECONDS: int = int(os.getenv("RATE_LIMITED_PAUSE_SECONDS"))
    first_request_start = time.time()
    client.get('/')
    first_request_end = time.time()
    second_request_start = time.time()
    client.get('/')
    second_request_end = time.time()

    assert first_request_end - first_request_start < RATE_LIMITED_PAUSE_SECONDS
    assert RATE_LIMITED_PAUSE_SECONDS < second_request_end - second_request_start


def test_malicious(client):
    """Expect a forbidden request when the key is_malicious exists in the JSON body"""
    data = {'is_malicious': True}
    json_data = json.dumps(data)
    response = client.post('/', json=json_data)
    assert response.status_code == 401


def test_nested_malicious(client):
    """Expect a forbidden request when the nested key is_malicious exists in the JSON body"""
    data = {"layer_1": {'is_malicious': True}}
    json_data = json.dumps(data)
    print(json_data)
    response = client.post('/', json=json_data)
    assert response.status_code == 401
