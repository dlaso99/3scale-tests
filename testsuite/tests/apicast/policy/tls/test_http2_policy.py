"""
Default test for HTTP2 policy
"""
import pytest

from testsuite import rawobj, HTTP2 # noqa # pylint: disable=unused-import
from testsuite.echoed_request import EchoedRequest
from testsuite.gateways.gateways import Capability


# CFSSL instance is necessary
pytestmark = [
    pytest.mark.required_capabilities(Capability.STANDARD_GATEWAY),
    pytest.mark.issue("https://issues.redhat.com/browse/THREESCALE-4684")]


@pytest.fixture(scope="module")
def policy_settings():
    """Http2 policy"""
    return rawobj.PolicyConfig("grpc", {})


@pytest.fixture(scope="module")
def backends_mapping(custom_backend, private_base_url):
    """
    Create backends with paths "/http1" and "/http2"
    """
    return {
        "/http1": custom_backend("http1", private_base_url("httpbin_service")),
        "/http2": custom_backend("http2", private_base_url("httpbin_go_service"))
        }


@pytest.fixture(scope="module")
def client(api_client):
    """Make sure that api_client is using http2"""
    return api_client()


def test_full_http2(client):
    """
    Test full HTTP2 traffic
    client --> apicast --> backend
    """
    response = client.get("/http2/info")
    # client --> apicast
    assert response.status_code == 200
    assert response.raw.version.value == "HTTP/2"

    # apicast --> backend
    echoed_request = EchoedRequest.create(response)
    assert echoed_request.json.get("proto", "") == "HTTP/2.0"


# Skip because the test is using default api_client which is overridden by HTTP2 client
@pytest.mark.skipif("HTTP2")
def test_http1(api_client):
    """
    Test successful request
    [http1] client --> apicast
    [http2] apicast --> backend
    """
    api_client = api_client()

    # client --> apicast
    response = api_client.get("/http2/info")
    assert response.status_code == 200
    assert response.raw.version == 11, "Expected HTTP1.1 version"

    # apicast --> backend
    echoed_request = EchoedRequest.create(response)
    assert echoed_request.json.get("proto", "") == "HTTP/2.0"
