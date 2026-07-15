import logging
import signal
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

from main import (
    configure_logging,
    install_signal_handlers,
    parse_arguments,
)


@dataclass
class FakeProductionAgent:
    """Minimal production agent used by signal tests."""

    stop_requested: bool = False

    def request_stop(self) -> None:
        self.stop_requested = True

def test_parse_arguments_uses_default_configuration_paths(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["ohanna-agent"],
    )

    arguments = parse_arguments()

    assert arguments.config == Path(
        "config/shikamaru.yaml"
    )
    assert arguments.infrastructure == Path(
        "config/infrastructure.yaml"
    )
    assert arguments.dns_config == Path(
        "config/plugins/dns.yaml"
    )
    assert arguments.log_level == "INFO"


def test_parse_arguments_accepts_custom_paths(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ohanna-agent",
            "--config",
            "custom/application.yaml",
            "--infrastructure",
            "custom/infrastructure.yaml",
            "--dns-config",
            "custom/dns.yaml",
            "--log-level",
            "DEBUG",
        ],
    )

    arguments = parse_arguments()

    assert arguments.config == Path(
        "custom/application.yaml"
    )
    assert arguments.infrastructure == Path(
        "custom/infrastructure.yaml"
    )
    assert arguments.dns_config == Path(
        "custom/dns.yaml"
    )
    assert arguments.log_level == "DEBUG"

@pytest.mark.parametrize(
    "level",
    [
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ],
)
def test_configure_logging_accepts_known_level(
    level: str,
) -> None:
    configure_logging(level)

    assert logging.getLogger().level == getattr(
        logging,
        level,
    )

def test_configure_logging_accepts_lowercase_level() -> None:
    configure_logging("debug")

    assert logging.getLogger().level == logging.DEBUG

def test_configure_logging_rejects_unknown_level() -> None:
    with pytest.raises(
        ValueError,
        match="Unsupported logging level",
    ):
        configure_logging("TRACE")

def test_parse_arguments_rejects_invalid_log_level(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ohanna-agent",
            "--log-level",
            "TRACE",
        ],
    )

    with pytest.raises(SystemExit):
        parse_arguments()

def test_install_signal_handlers_registers_sigint_and_sigterm(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registered_handlers: dict[
        signal.Signals,
        object,
    ] = {}

    def fake_signal(
        signal_number: signal.Signals,
        handler: object,
    ) -> None:
        registered_handlers[signal_number] = handler

    monkeypatch.setattr(
        signal,
        "signal",
        fake_signal,
    )

    agent = FakeProductionAgent()

    install_signal_handlers(agent)  # type: ignore[arg-type]

    assert signal.SIGINT in registered_handlers
    assert signal.SIGTERM in registered_handlers

def test_signal_handler_requests_agent_stop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registered_handlers: dict[
        signal.Signals,
        object,
    ] = {}

    def fake_signal(
        signal_number: signal.Signals,
        handler: object,
    ) -> None:
        registered_handlers[signal_number] = handler

    monkeypatch.setattr(
        signal,
        "signal",
        fake_signal,
    )

    agent = FakeProductionAgent()

    install_signal_handlers(agent)  # type: ignore[arg-type]

    handler = registered_handlers[signal.SIGTERM]

    assert callable(handler)

    handler(  # type: ignore[operator]
        signal.SIGTERM,
        None,
    )

    assert agent.stop_requested is True