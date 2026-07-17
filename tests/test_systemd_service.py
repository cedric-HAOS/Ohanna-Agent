"""Tests for the Ohanna-Agent systemd service unit."""

from pathlib import Path

SERVICE_PATH = Path("deployment/systemd/ohanna-agent.service")


def read_service() -> str:
    """Return the systemd service definition."""
    return SERVICE_PATH.read_text(encoding="utf-8")


def test_systemd_service_file_exists() -> None:
    """Provide the reference systemd service unit."""
    assert SERVICE_PATH.is_file()


def test_systemd_service_uses_reference_executable_and_configuration() -> None:
    """Use the Linux filesystem paths defined by the deployment contract."""
    service = read_service()

    assert "/opt/ohanna-agent/venv/bin/ohanna-agent" in service
    assert "--config /etc/ohanna-agent/shikamaru.yaml" in service
    assert "--infrastructure /etc/ohanna-agent/infrastructure.yaml" in service
    assert "--dns-config /etc/ohanna-agent/plugins/dns.yaml" in service


def test_systemd_service_runs_as_dedicated_user() -> None:
    """Run Ohanna-Agent without root privileges."""
    service = read_service()

    assert "User=ohanna-agent" in service
    assert "Group=ohanna-agent" in service


def test_systemd_service_waits_for_network_and_restarts_on_failure() -> None:
    """Declare the runtime network and recovery requirements."""
    service = read_service()

    assert "Wants=network-online.target" in service
    assert "After=network-online.target" in service
    assert "Restart=on-failure" in service
    assert "RestartSec=5s" in service


def test_systemd_service_supports_graceful_shutdown() -> None:
    """Allow the existing SIGTERM handler to stop the agent cleanly."""
    service = read_service()

    assert "KillSignal=SIGTERM" in service
    assert "TimeoutStopSec=30s" in service


def test_systemd_service_uses_journald_and_basic_hardening() -> None:
    """Collect logs in journald and apply compatible protections."""
    service = read_service()

    assert "StandardOutput=journal" in service
    assert "StandardError=journal" in service
    assert "NoNewPrivileges=true" in service
    assert "PrivateTmp=true" in service
    assert "ProtectHome=true" in service
    assert "ProtectSystem=strict" in service


def test_systemd_service_starts_in_multi_user_target() -> None:
    """Enable the service during normal system startup."""
    service = read_service()

    assert "WantedBy=multi-user.target" in service
