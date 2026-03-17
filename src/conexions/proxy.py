#! /usr/bin/env python3
# ------------------------------------------------------------------------------
# + Authors:	Ran#
# + Created:	2022/02/13 15:30:39.408208
# + Revised:	2026/03/16 18:57:44.102938
# ------------------------------------------------------------------------------

from dataclasses import dataclass

from .anonymity import Anonymity
from .country import Country
from .protocol import Protocol

# ------------------------------------------------------------------------------


@dataclass
class Proxy:
    ip: str
    port: int
    country: Country | None
    anonymity: Anonymity
    google: bool
    protocol: Protocol
    last_checked: str

    @classmethod
    def from_list(cls, values: list[str]) -> "Proxy":
        """Constructs a Proxy from an ordered list of scraped column values.

        Args:
            values: Ordered list matching the source table columns:
                ip, port, country_code, country_name, anonymity, google,
                https ("yes"/"no"), last_checked.
                ``country_code`` is converted to ``Country``; unknown codes
                yield ``None``. ``google`` and ``https`` are converted to
                ``bool``. ``https`` maps to ``Protocol.HTTPS`` (True) or
                ``Protocol.HTTP`` (False).

        Returns:
            A new Proxy instance.
        """
        (
            ip,
            port,
            country_code,
            _country_name,
            anonymity,
            google,
            https,
            last_checked,
        ) = values
        try:
            country = Country(country_code)
        except ValueError:
            country = None
        return cls(
            ip=ip,
            port=int(port),
            country=country,
            anonymity=Anonymity(anonymity),
            google=google == "yes",
            protocol=Protocol.HTTPS if https == "yes" else Protocol.HTTP,
            last_checked=last_checked,
        )

    def __str__(self) -> str:
        country = self.country.value if self.country else "??"
        google = "google ✓" if self.google else "google ✗"
        return (
            f"{self.ip}:{self.port}"
            f"  {self.protocol.upper()}"
            f"  {country}"
            f"  {self.anonymity}"
            f"  {google}"
            f"  checked {self.last_checked}"
        )

    def as_proxies(self) -> dict[str, str]:
        """Returns a requests-compatible proxies dict.

        HTTP/HTTPS proxies from free-proxy-list speak plain HTTP for the proxy
        connection itself — "Https: yes" only means they support CONNECT
        tunneling for HTTPS targets. SOCKS proxies use their own scheme.

        HTTP-only proxies expose only the ``http`` key.
        HTTPS-capable and SOCKS proxies expose both ``http`` and ``https``.

        Returns:
            A dict mapping URL schemes to proxy URLs.
        """
        scheme = self.protocol.value if self.protocol in (Protocol.SOCKS4, Protocol.SOCKS5) else "http"
        proxy_url = f"{scheme}://{self.ip}:{self.port}"
        proxies = {"http": proxy_url}
        if self.protocol != Protocol.HTTP:
            proxies["https"] = proxy_url
        return proxies


# ------------------------------------------------------------------------------
