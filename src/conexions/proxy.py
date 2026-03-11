#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# + Authors:	Ran#
# + Created:	2022/02/13 15:30:39.408208
# + Revised:	2026/03/11 10:15:00.000000
# ------------------------------------------------------------------------------

from dataclasses import dataclass

# ------------------------------------------------------------------------------


@dataclass
class Proxy:
    ip: str
    port: str
    country_code: str
    country_name: str
    anonymity: str
    google: str
    https: str
    last_checked: str

    @classmethod
    def from_list(cls, values: list[str]) -> "Proxy":
        """Constructs a Proxy from an ordered list of field values.

        Args:
            values: Ordered list: ip, port, country_code, country_name,
                anonymity, google, https, last_checked.

        Returns:
            A new Proxy instance.
        """
        return cls(*values)

    def as_proxies(self) -> dict[str, str]:
        """Returns a requests-compatible proxies dict.

        Returns:
            A dict with 'http' and 'https' keys pointing to the proxy URL.
        """
        return {
            "http": f"http://{self.ip}:{self.port}",
            "https": f"http://{self.ip}:{self.port}",
        }


# ------------------------------------------------------------------------------
