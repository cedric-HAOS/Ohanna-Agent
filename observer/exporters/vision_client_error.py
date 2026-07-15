"""Errors raised while communicating with Ohanna-Vision."""


class VisionClientError(RuntimeError):
    """Raised when an observation cannot be sent to Ohanna-Vision."""