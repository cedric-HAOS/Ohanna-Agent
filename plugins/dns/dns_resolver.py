import dns.exception
import dns.resolver

from plugins.dns.dns_result import DNSResult


class DNSResolver:
    """Resolve hostnames using an explicit DNS server when provided."""

    def resolve(
        self,
        hostname: str,
        server: str | None = None,
    ) -> DNSResult:
        resolver = dns.resolver.Resolver(configure=server is None)

        if server is not None:
            resolver.nameservers = [server]

        try:
            answers = resolver.resolve(hostname, "A")
            address = answers[0].to_text()
        except (dns.exception.DNSException, OSError) as exc:
            return DNSResult(
                hostname=hostname,
                server=server,
                success=False,
                error=str(exc),
            )

        return DNSResult(
            hostname=hostname,
            server=server,
            success=True,
            address=address,
        )
