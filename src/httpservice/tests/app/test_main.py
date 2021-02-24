import json
from flask import Response

# Malicious request should give a 401
def test_malicious_post(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'is_malicious': 'true',
    }

    result = client.post("/", data=json.dumps(data), headers=headers)
    print(result.status_code)
    assert result.status_code == 401

# Ensure service returns a simple response
def test_simple_post(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'foo': 'bar',
    }
    result = client.post("/", data=json.dumps(data), headers=headers)
    assert result.status_code == 200
    assert result.content_type == "application/json"
    assert "message" in result.json
    assert result.json["message"] == "Processed by the backend service!"