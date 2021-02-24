
def test_service_up(client):
    """
        Simple test to ensure that the backend service is up and responding to simple messages
    """
    response = client.get('/')
    result = response.get_json()
    assert result is not None
    assert "message" in result
    assert result["message"] == "Processed by the backend service!"
