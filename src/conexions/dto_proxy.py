#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# + Authors:	Ran#
# + Created:	2022/02/13 15:30:39.408208
# + Revised:	2026/03/11 08:02:35.676827
# ------------------------------------------------------------------------------

from dataclasses import dataclass

# ------------------------------------------------------------------------------


@dataclass
class ProxyDTO:
    ip: str
    port: str
    country_code: str
    country_name: str
    anonymity: str
    google: str
    https: str
    last_checked: str

    def __init__(self, lst_contents: list) -> None:
        """Initializes the ProxyDTO from a list of column values.

        Args:
            lst_contents: Ordered list of proxy fields: ip, port, country_code,
                country_name, anonymity, google, https, last_checked.
        """
        self.ip = lst_contents[0]
        self.port = lst_contents[1]
        self.country_code = lst_contents[2]
        self.country_name = lst_contents[3]
        self.anonymity = lst_contents[4]
        self.google = lst_contents[5]
        self.https = lst_contents[6]
        self.last_checked = lst_contents[7]

    def format(self) -> dict[str, str]:
        """Formats the proxy as a requests-compatible proxies dict.

        Returns:
            A dict with 'http' and 'https' keys pointing to the proxy URL.
        """
        return {
            "http": f"http://{self.ip}:{self.port}",
            "https": f"http://{self.ip}:{self.port}",
        }


# ------------------------------------------------------------------------------
