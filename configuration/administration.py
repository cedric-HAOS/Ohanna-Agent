"""Configuration of the authenticated Agent administration API."""

from pathlib import Path

from pydantic import Field, IPvAnyAddress

from configuration.base import Config


class DHCPAdministrationConfig(Config):
    """Paths used to manage the installed dnsmasq DHCP service."""

    enabled: bool = True
    server_node_id: str = "infra-01"
    main_config_path: Path = Path("/etc/dnsmasq.d/00-ohana.conf")
    infrastructure_reservations_path: Path = Path(
        "/etc/dnsmasq.d/10-infrastructure.conf"
    )
    server_reservations_path: Path = Path("/etc/dnsmasq.d/20-serveurs.conf")
    network_reservations_path: Path = Path(
        "/etc/dnsmasq.d/30-infrastructure-reseau.conf"
    )
    home_automation_reservations_path: Path = Path(
        "/etc/dnsmasq.d/40-passerelles-domotiques.conf"
    )
    critical_reservations_path: Path = Path(
        "/etc/dnsmasq.d/50-equipements-critiques.conf"
    )
    leases_path: Path = Path("/var/lib/misc/dnsmasq.leases")
    validation_command: tuple[str, ...] | None = (
        "/usr/sbin/dnsmasq",
        "--test",
    )
    reload_request_path: Path = Path("/run/ohana-agent/dhcp-reload.request")


class AdministrationConfig(Config):
    """Agent administration endpoint configuration."""

    enabled: bool = False
    host: IPvAnyAddress = IPvAnyAddress("127.0.0.1")
    port: int = Field(default=8765, ge=1, le=65535)
    token_file: Path = Path("/etc/ohana-agent/management.token")
    dhcp: DHCPAdministrationConfig = Field(default_factory=DHCPAdministrationConfig)
