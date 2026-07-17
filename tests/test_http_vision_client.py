import json
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from typing import Any

import pytest

from observer.exporters import (
    HttpVisionClient,
    VisionClient,
    VisionClientError,
)


class VisionRequestHandler(BaseHTTPRequestHandler):
    """Minimal fake Ohanna-Vision HTTP endpoint."""

    response_status = 202
    response_body = b"{}"
    requests: list[dict[str, Any]] = []

    def do_POST(self) -> None:
        """Capture one HTTP POST request."""
        content_length = int(
            self.headers.get(
                "Content-Length",
                "0",
            )
        )
        request_body = self.rfile.read(content_length)

        self.__class__.requests.append(
            {
                "path": self.path,
                "headers": dict(self.headers),
                "body": request_body,
            }
        )

        self.send_response(self.__class__.response_status)
        self.send_header(
            "Content-Type",
            "application/json",
        )
        self.end_headers()
        self.wfile.write(self.__class__.response_body)

    def log_message(
        self,
        format: str,
        *args: object,
    ) -> None:
        """Disable test-server console logging."""


@contextmanager
def run_test_server(
    *,
    response_status: int = 202,
    response_body: bytes = b"{}",
) -> Iterator[str]:
    """Run a temporary local HTTP server."""
    VisionRequestHandler.response_status = response_status
    VisionRequestHandler.response_body = response_body
    VisionRequestHandler.requests = []

    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        VisionRequestHandler,
    )
    thread = Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    host, port = server.server_address

    try:
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def build_payload() -> dict[str, Any]:
    """Build a valid Ohanna-Vision request payload."""
    return {
        "capability_id": "dns.resolve",
        "service_id": "dns-primary",
        "node_id": "infra-01",
        "status": "healthy",
        "observed_at": "2026-07-15T12:30:00+00:00",
        "latency_ms": 12.5,
        "metadata": {
            "hostname": "example.com",
        },
    }


def test_http_client_can_be_created() -> None:
    client = HttpVisionClient(
        observation_url=("http://127.0.0.1:8000/api/observations"),
        timeout_seconds=3.0,
    )

    assert client.observation_url == ("http://127.0.0.1:8000/api/observations")
    assert client.timeout_seconds == 3.0


def test_http_client_rejects_empty_url() -> None:
    with pytest.raises(
        ValueError,
        match="observation_url must not be empty",
    ):
        HttpVisionClient(observation_url=" ")


def test_http_client_rejects_invalid_timeout() -> None:
    with pytest.raises(
        ValueError,
        match="timeout_seconds must be greater than zero",
    ):
        HttpVisionClient(
            observation_url=("http://127.0.0.1:8000/api/observations"),
            timeout_seconds=0,
        )


def test_http_client_posts_json_observation() -> None:
    with run_test_server() as server_url:
        client = HttpVisionClient(
            observation_url=(f"{server_url}/api/observations"),
        )

        client.send_observation(build_payload())

    assert len(VisionRequestHandler.requests) == 1

    request = VisionRequestHandler.requests[0]

    assert request["path"] == "/api/observations"
    assert request["headers"]["Content-Type"] == ("application/json")
    assert request["headers"]["Accept"] == "application/json"
    assert json.loads(request["body"]) == build_payload()


def test_http_client_accepts_202_response() -> None:
    with run_test_server(response_status=202) as server_url:
        client = HttpVisionClient(
            observation_url=(f"{server_url}/api/observations"),
        )

        result = client.send_observation(build_payload())

    assert result is None


def test_http_client_reports_http_error() -> None:
    with run_test_server(
        response_status=422,
        response_body=b'{"detail":"Invalid observation"}',
    ) as server_url:
        client = HttpVisionClient(
            observation_url=(f"{server_url}/api/observations"),
        )

        with pytest.raises(
            VisionClientError,
            match="HTTP status 422",
        ) as error:
            client.send_observation(build_payload())

    assert "Invalid observation" in str(error.value)


def test_http_client_rejects_unexpected_success_status() -> None:
    with run_test_server(response_status=200) as server_url:
        client = HttpVisionClient(
            observation_url=(f"{server_url}/api/observations"),
        )

        with pytest.raises(
            VisionClientError,
            match="unexpected HTTP status 200",
        ):
            client.send_observation(build_payload())


def test_http_client_reports_unavailable_server() -> None:
    client = HttpVisionClient(
        observation_url=("http://127.0.0.1:1/api/observations"),
        timeout_seconds=0.2,
    )

    with pytest.raises(
        VisionClientError,
        match="Unable to reach Ohanna-Vision",
    ):
        client.send_observation(build_payload())


def test_http_client_rejects_non_json_payload() -> None:
    client = HttpVisionClient(
        observation_url=("http://127.0.0.1:8000/api/observations"),
    )
    payload = build_payload()
    payload["metadata"] = {
        "invalid": object(),
    }

    with pytest.raises(
        VisionClientError,
        match="cannot be encoded as JSON",
    ):
        client.send_observation(payload)


def test_http_client_implements_vision_client_protocol() -> None:
    client = HttpVisionClient(
        observation_url=("http://127.0.0.1:8000/api/observations"),
    )

    assert isinstance(client, VisionClient)
