#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# + Authors:	Ran#
# + Created:	2022/02/13 16:43:37.259437
# + Revised:	2026/03/11 07:57:13.101630
# ------------------------------------------------------------------------------
import requests
from requests.sessions import Session
from requests.models import Response
from requests.exceptions import ConnectionError

# import secrets
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from yaspin import yaspin
from yaspin.spinners import Spinners

from .dto_proxy import ProxyDTO
from .excepcions import PageChangedError


# ------------------------------------------------------------------------------
class Proxy:
    # Class attributes ---------------------------------------------------------
    __url: str = "https://sslproxies.org"
    __session: Session = None
    __verbose: bool = False
    __show_spinner: bool = False
    __max_connections: int = 0  # 0 means no predefined maximum
    # xFCR: merge connection counts into a single variable
    __total_connections: int = 0
    __connection_count: int = 0
    __direct_connection_count: int = 0
    __retries: int = 5
    __timeout: int = 30
    __header: dict[str, str]
    __proxy_list: list[ProxyDTO]  # Ordered oldest[0] to newest[len()]
    __proxy: ProxyDTO

    __ip_urls: list[str] = ["https://ip.me", "https://icanhazip.com"]
    # --------------------------------------------------------------------------

    def __init__(
        self,
        max_connections: int = 0,
        retries: int = 5,
        timeout: int = 30,
        verbose: bool = False,
        show_spinner: bool = False,
    ) -> None:
        self.__verbose = verbose
        self.__show_spinner = show_spinner
        self.__max_connections = max_connections
        self.__retries = retries
        self.__timeout = timeout
        self.__proxy_list = []
        self.__total_connections = 0
        self.__connection_count = 0
        self.__direct_connection_count = 0
        self.__spinner = yaspin(text="Connecting", spinner=Spinners.dots)

        self.set_header()  # Sets __header
        self.set_proxies()  # Fills __proxy_list
        self.set_proxy()  # Pops a proxy from the list into __proxy

    # --------------------------------------------------------------------------

    # Getters

    def get_url(self) -> str:
        return self.__url

    def get_session(self) -> Session | None:
        return self.__session

    def get_verbose(self) -> bool:
        return self.__verbose

    def get_show_spinner(self) -> bool:
        return self.__show_spinner

    def get_max_connections(self) -> int:
        return self.__max_connections

    def get_total_connections(self) -> int:
        return self.__total_connections

    def get_connection_count(self) -> int:
        return self.__connection_count

    def get_direct_connection_count(self) -> int:
        return self.__direct_connection_count

    def get_retries(self) -> int:
        return self.__retries

    def get_timeout(self) -> int:
        return self.__timeout

    def get_header(self, refresh: bool | int = False) -> dict[str, str]:
        try:
            return self.__header
        finally:
            if refresh:
                self.set_header()

    def get_proxies(self) -> list[ProxyDTO]:
        return self.__proxy_list

    def get_proxy(self) -> ProxyDTO:
        # if max connections reached, rotate to a new proxy
        if (self.get_max_connections() != 0) and (
            self.get_connection_count() >= self.get_max_connections()
        ):
            self.set_proxy()
        return self.__proxy

    def __get_proxy(self) -> dict[str, str]:
        try:
            return self.get_proxy().format()
        finally:
            self.__set_connection_count(self.get_connection_count() + 1)
            self.__set_total_connections(self.get_total_connections() + 1)

    def get_ip_urls(self) -> list[str]:
        return self.__ip_urls

    def get_spinner(self):
        return self.__spinner

    # Getters #

    # Setters

    def __set_url(self, url: str) -> None:
        self.__url = url

    def set_session(self, reset: bool | int = False) -> None:
        if reset:
            self.__session = None
        else:
            self.__session = requests.Session()

    def set_verbose(self, verbose: bool) -> None:
        self.__verbose = verbose

    def set_show_spinner(self, show_spinner: bool) -> None:
        self.__show_spinner = show_spinner

    def set_retries(self, retries: int) -> None:
        self.__retries = retries

    def set_max_connections(self, max_connections: int) -> None:
        self.__max_connections = max_connections

    def __set_total_connections(self, total_connections: int) -> None:
        self.__total_connections = total_connections

    def __set_connection_count(self, connection_count: int) -> None:
        self.__connection_count = connection_count

    def __set_direct_connection_count(self, direct_connection_count: int) -> None:
        self.__direct_connection_count = direct_connection_count

    def set_timeout(self, timeout: int) -> None:
        self.__timeout = timeout

    def set_header(self) -> None:
        self.__header = {"User-Agent": UserAgent().random}

    def set_proxies(self) -> None:
        """
        Fetches the proxy page and extracts all proxy information from it.
        """

        while True:
            try:
                page = requests.get(url=self.get_url(), headers=self.get_header())
            except ConnectionError:
                pass
            except Exception:
                raise
            else:
                if page.ok:
                    page.encoding = "utf-8"
                    break

        if self.get_verbose() and self.get_total_connections() > 0:
            print(f"{__name__}: Filling proxy list.")

        proxy_table = bs(page.text, "html.parser").find(class_="table")

        expected_cols = [
            "IP Address",
            "Port",
            "Code",
            "Country",
            "Anonymity",
            "Google",
            "Https",
            "Last Checked",
        ]
        obtained_cols = proxy_table.thead.find_all("th")

        if len(expected_cols) != len(obtained_cols):
            raise PageChangedError("Number of columns changed")

        for expected, obtained in zip(expected_cols, obtained_cols):
            if expected != obtained.text:
                raise PageChangedError("Column order or name changed")

        for row in proxy_table.tbody:
            new_proxy = ProxyDTO([col.text for col in row.find_all("td")])
            if (
                (new_proxy.anonymity == "elite proxy")
                and (new_proxy.google == "no")
                and (new_proxy.https == "yes")
            ):
                # insert at front so we pop from the back (newest last)
                self.__proxy_list.insert(0, new_proxy)

    def set_proxy(self) -> None:
        """
        Pops a proxy from the list and sets it as the active proxy.
        If the list is empty, re-scrapes the page to refill it.
        """

        try:
            self.__proxy = self.get_proxies().pop()
        except IndexError:
            self.set_proxies()
            self.set_proxy()  # recursion
        finally:
            self.__set_connection_count(0)

    # Setters #

    def get_ip(self, retries: int | None = None) -> str:
        if retries is None:
            retries = self.get_retries()

        try:
            return requests.get(self.get_ip_urls()[0]).text.rstrip()
        except ConnectionError:
            return self.get_ip(retries - 1)

    def get_direct(
        self,
        url: str,
        params: dict | None = None,
        cookies: dict | None = None,
        stream: bool = False,
        timeout: int | None = None,
        retries: int | None = None,
    ) -> Response:
        """
        Makes a direct request without a proxy (bare connection).
        """

        if timeout is None:
            timeout = self.get_timeout()

        if retries is None:
            retries = self.get_retries()

        if (self.get_max_connections() != 0) and (
            self.get_connection_count() >= self.get_max_connections()
        ):
            self.__set_direct_connection_count(0)
            retries = self.get_retries()

        try:
            if self.get_show_spinner():
                self.get_spinner().start()
            if self.get_session() is not None:
                return self.get_session().get(
                    url=url,
                    params=params,
                    headers=self.get_header(),
                    cookies=cookies,
                    stream=stream,
                    timeout=timeout,
                )
            else:
                return requests.get(
                    url=url,
                    params=params,
                    headers=self.get_header(refresh=True),
                    cookies=cookies,
                    stream=stream,
                    timeout=timeout,
                )
        except Exception:
            if retries <= 0:
                if self.get_verbose():
                    print(f"*{__name__}* Reached maximum number of retries.")
                retries = self.get_retries()
            if self.get_verbose():
                print(f"*{__name__}* Retry nº {self.get_retries() + 1 - retries}.")

            return self.get_direct(
                url=url,
                params=params,
                cookies=cookies,
                stream=stream,
                timeout=timeout,
                retries=retries - 1,
            )
        finally:
            self.__set_direct_connection_count(self.get_direct_connection_count() + 1)
            self.__set_total_connections(self.get_total_connections() + 1)
            if self.get_show_spinner():
                self.get_spinner().stop()

    def get(
        self,
        url: str,
        params: dict | None = None,
        cookies: dict | None = None,
        stream: bool = False,
        timeout: int | None = None,
        retries: int | None = None,
    ) -> Response:
        """
        Makes a request through the active proxy.
        """

        if timeout is None:
            timeout = self.get_timeout()

        if retries is None:
            retries = self.get_retries()

        if (self.get_max_connections() != 0) and (
            self.get_connection_count() >= self.get_max_connections()
        ):
            if self.get_verbose():
                print(
                    f"{__name__}: Reached max connections. Getting new proxy ({len(self.get_proxies())} remaining)"
                )
            self.set_proxy()
            self.__set_connection_count(0)
            retries = self.get_retries()

        try:
            if self.get_show_spinner():
                self.get_spinner().start()

            if self.get_session() is not None:
                return self.get_session().get(
                    url=url,
                    params=params,
                    proxies=self.__get_proxy(),
                    headers=self.get_header(),
                    cookies=cookies,
                    stream=stream,
                    timeout=timeout,
                )
            else:
                return requests.get(
                    url=url,
                    params=params,
                    proxies=self.__get_proxy(),
                    headers=self.get_header(refresh=True),
                    cookies=cookies,
                    stream=stream,
                    timeout=timeout,
                )
        except Exception:
            if retries <= 0:
                if self.get_verbose():
                    print(
                        f"{__name__}: Reached max retries. Getting new proxy ({len(self.get_proxies())} remaining)"
                    )
                self.set_proxy()
                retries = self.get_retries()
            if self.get_verbose():
                print(f"{__name__}: Retry nº {self.get_retries() + 1 - retries}.")

            return self.get(
                url=url,
                params=params,
                cookies=cookies,
                stream=stream,
                timeout=timeout,
                retries=retries - 1,
            )
        finally:
            if self.get_show_spinner():
                self.get_spinner().stop()


# ------------------------------------------------------------------------------
