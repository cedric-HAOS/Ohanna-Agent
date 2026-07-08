# plugins/dns/dns_check.py

from plugins.dns.dns_check_result import DNSCheckResult
from plugins.dns.dns_resolver import DNSResolver


class DNSCheck:
    """Check DNS capability by resolving a hostname."""

    def __init__(self, resolver: DNSResolver | None = None) -> None:
        self._resolver = resolver or DNSResolver()

    def check(
        self,
        hostname: str,
        server: str | None = None,
    ) -> DNSCheckResult:
        result = self._resolver.resolve(
            hostname=hostname,
            server=server,
        )

        return DNSCheckResult(
            hostname=result.hostname,
            server=result.server,
            healthy=result.success,
            address=result.address,
            error=result.error,
        )