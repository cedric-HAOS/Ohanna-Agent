"""HTTP client used to send observations to Ohanna-Vision."""

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from observer.exporters.vision_client_error import VisionClientError


@dataclass(frozen=True, slots=True)
class HttpVisionClient:
    """Send observation payloads to the Ohanna-Vision REST API."""

    observation_url: str
    timeout_seconds: float = 5.0

    def __post_init__(self) -> None:
        """Validate client configuration."""
        if not self.observation_url.strip():
            raise ValueError("observation_url must not be empty.")

        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero.")

    def send_observation(
        self,
        payload: dict[str, Any],
    ) -> None:
        """Send one observation payload to Ohanna-Vision."""
        request = Request(
            url=self.observation_url,
            data=self._encode_payload(payload),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(
                request,
                timeout=self.timeout_seconds,
            ) as response:
                status_code = response.status

        except HTTPError as error:
            response_body = self._read_error_body(error)

            raise VisionClientError(
                self._build_http_error_message(
                    status_code=error.code,
                    response_body=response_body,
                )
            ) from error

        except URLError as error:
            raise VisionClientError(
                "Unable to reach Ohanna-Vision at "
                f"{self.observation_url}: {error.reason}"
            ) from error

        except TimeoutError as error:
            raise VisionClientError(
                "Timed out while sending an observation to "
                f"Ohanna-Vision at {self.observation_url}."
            ) from error

        if status_code != 202:
            raise VisionClientError(
                "Ohanna-Vision returned unexpected HTTP status "
                f"{status_code}; expected 202."
            )

    @staticmethod
    def _encode_payload(
        payload: dict[str, Any],
    ) -> bytes:
        """Encode a payload as UTF-8 JSON."""
        try:
            serialized_payload = json.dumps(
                payload,
                ensure_ascii=False,
                separators=(",", ":"),
            )
        except (TypeError, ValueError) as error:
            raise VisionClientError(
                "The observation payload cannot be encoded as JSON."
            ) from error

        return serialized_payload.encode("utf-8")

    @staticmethod
    def _read_error_body(error: HTTPError) -> str:
        """Read an HTTP error response without hiding the initial error."""
        try:
            return error.read().decode(
                "utf-8",
                errors="replace",
            )
        except OSError:
            return ""

    @staticmethod
    def _build_http_error_message(
        *,
        status_code: int,
        response_body: str,
    ) -> str:
        """Build a useful HTTP failure message."""
        message = (
            f"Ohanna-Vision rejected the observation with HTTP status {status_code}."
        )

        if response_body:
            return f"{message} Response: {response_body}"

        return message
