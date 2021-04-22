"""
Randori Code Challenge services tests module.
"""

from contextlib import nullcontext as does_not_raise
import json
from typing import Any, Optional

import pytest
import pytest_httpx

from code_challenge.services import proxy


@pytest.mark.parametrize(
    "request_method, request_payload, backend_url, backend_port, http_status_code, http_response_data, "
    "http_response_data_dict, expectation",
    [
        # GET succeeded
        (
            "GET",
            None,
            "https://some-backend/1234",
            8081,
            200,
            None,
            {"key": "value"},
            does_not_raise(),
        ),
        # GET returns a 404
        (
            "GET",
            None,
            "https://some-backend/9876",
            8081,
            404,
            "record does not exist",
            None,
            pytest.raises(proxy.CodeChallengeProxyRequestError),
        ),
        (
            "POST",
            json.dumps({"some_key": "some_value"}).encode("utf-8"),
            "https://some-backend",
            8081,
            201,
            None,
            {"id": "12345"},
            does_not_raise(),
        ),
        (
            "PUT",
            json.dumps({"some_other_key": "some_other_value"}).encode("utf-8"),
            "https://some-backend/34567",
            8081,
            200,
            None,
            {"id": "34567"},
            does_not_raise(),
        ),
    ],
)
@pytest.mark.asyncio
async def test_proxy_request(
    httpx_mock: pytest_httpx.HTTPXMock,
    request_method: str,
    request_payload: Optional[bytes],
    backend_url: str,
    backend_port: int,
    http_status_code: int,
    expectation: Any,
    http_response_data: Optional[str],
    http_response_data_dict: Optional[dict],
):
    """Test the proxy_request proxy method."""

    httpx_mock.add_response(
        method=request_method, status_code=http_status_code, data=http_response_data, json=http_response_data_dict
    )

    with expectation as exec_info:
        response_status_code, response_data = await proxy.proxy_request(
            request_method=request_method,
            backend_url=backend_url,
            backend_port=backend_port,
            request_payload=request_payload,
        )

        requests = httpx_mock.get_requests()

        assert response_status_code == http_status_code
        assert response_data == http_response_data_dict
        assert requests[0]
        assert requests[0].read() == request_payload if request_method != "GET" else True

    assert exec_info.value.status_code == http_status_code if exec_info else True
    assert exec_info.value.args[0] == http_response_data if exec_info else True
