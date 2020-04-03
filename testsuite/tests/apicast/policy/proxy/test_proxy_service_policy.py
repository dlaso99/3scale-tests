"""
Policy redirecting communication to the HTTP proxy service

Proxy service is simple camel route, that adds "Fuse-Camel-Proxy" header to the request
"""

import pytest
from testsuite import rawobj


@pytest.fixture(scope="module")
def policy_settings(testconfig):
    """Configure API with a http_proxy policy - proxy service is a Camel route deployed in OCP"""
    proxy_service = testconfig["integration"]["service"]["proxy_service"]
    proxy_config = {
        "https_proxy": "https://" + proxy_service,
        "http_proxy": "http://" + proxy_service,
        "all_proxy": "http://" + proxy_service
    }
    return rawobj.PolicyConfig("http_proxy", proxy_config)


@pytest.fixture(scope="module")
def backends_mapping(private_base_url, custom_backend):
    """
    Creates httpbin backend: "/"
    Proxy service used in this test does not support HTTP over TLS (https) protocol,
    therefore http is preferred instead
    """
    return {"/": custom_backend("netty-proxy", private_base_url("httpbin-nossl"))}


def test_http_proxy_policy(api_client):
    """
    Fuse proxy service should add extra Header: "Fuse-Camel-Proxy", when handling communication
    between Apicast and backend API
    """
    response = api_client.get("/get")
    assert "Fuse-Camel-Proxy" in response.headers
