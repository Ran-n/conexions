#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# + Authors:	Ran#
# + Created:	2022/02/13 16:43:37.259437
# + Revised:	2026/03/11 11:12:50.671515
# ------------------------------------------------------------------------------
import requests
from requests.exceptions import ConnectionError
from requests.models import Response
from requests.sessions import Session

from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from yaspin import yaspin
from yaspin.spinners import Spinners

from .proxy import Proxy
from .excepcions import PageChangedError

# ------------------------------------------------------------------------------


class ProxyClient:
    """HTTP client with automatic proxy rotation sourced from free-proxy-list.net."""

    _URL: str = "https://free-proxy-list.net/"
    _IP_URLS: list[str] = ["https://ip.me", "https://icanhazip.com"]

    def __init__(
        self,
        max_connections: int = 0,
        retries: int = 5,
        timeout: int = 30,
        verbose: bool = False,
        show_spinner: bool = False,
    ) -> None:
        """Initializes the ProxyClient, scrapes the proxy list, and sets the first proxy.

        Args:
            max_connections: Max uses per proxy before rotating. 0 means unlimited.
            retries: Number of retry attempts on connection failure.
            timeout: Request timeout in seconds.
            verbose: If True, prints status messages to stdout.
            show_spinner: If True, shows a spinner during requests.
        """
        self.max_connections = max_connections
        self.retries = retries
        self.timeout = timeout
        self.verbose = verbose
        self.show_spinner = show_spinner

        self._session: Session | None = None
        self._total_connections: int = 0
        self._connection_count: int = 0
        self._direct_connection_count: int = 0
        self._spinner = yaspin(text="Connecting", spinner=Spinners.dots)

        self._header: dict[str, str] = self._new_header()
        self._proxy_list: list[Proxy] = []
        self._refill_proxies()
        self._active_proxy: Proxy = self._proxy_list.pop()

    # ── Read-only counters ────────────────────────────────────────────────────

    @property
    def total_connections(self) -> int:
        return self._total_connections

    @property
    def connection_count(self) -> int:
        return self._connection_count

    @property
    def direct_connection_count(self) -> int:
        return self._direct_connection_count

    # ── Active proxy (auto-rotates on access) ─────────────────────────────────

    @property
    def proxy(self) -> Proxy:
        """Active proxy; auto-rotates when max_connections is reached."""
        if self.max_connections != 0 and self._connection_count >= self.max_connections:
            self._rotate_proxy()
        return self._active_proxy

    # ── Session management ────────────────────────────────────────────────────

    def open_session(self) -> None:
        """Opens a persistent HTTP session."""
        self._session = requests.Session()

    def close_session(self) -> None:
        """Closes the persistent HTTP session."""
        self._session = None

    # ── Header management ─────────────────────────────────────────────────────

    def refresh_header(self) -> None:
        """Regenerates the User-Agent header, guaranteeing a different value."""
        new = self._new_header()
        while new == self._header:
            new = self._new_header()
        self._header = new

    # ── Proxy list management ─────────────────────────────────────────────────

    def rotate_proxy(self) -> None:
        """Manually rotates to the next available proxy."""
        self._rotate_proxy()

    def refill_proxies(self) -> None:
        """Re-scrapes the proxy source page to refill the proxy list."""
        self._refill_proxies()

    # ── Internal helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _new_header() -> dict[str, str]:
        return {"User-Agent": UserAgent().random}

    def _refill_proxies(self) -> None:
        """Scrapes the proxy source and fills the list with elite HTTPS proxies.

        Raises:
            PageChangedError: If the page structure no longer matches the expected format.
        """
        while True:
            try:
                page = requests.get(url=self._URL, headers=self._header)
            except ConnectionError:
                continue
            except Exception:
                raise
            else:
                if page.ok:
                    page.encoding = "utf-8"
                    break

        if self.verbose and self._total_connections > 0:
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
            proxy = Proxy.from_list([col.text for col in row.find_all("td")])
            if (
                proxy.anonymity == "elite proxy"
                and proxy.google == "no"
                and proxy.https == "yes"
            ):
                self._proxy_list.insert(0, proxy)

    def _rotate_proxy(self) -> None:
        """Pops a proxy from the list and sets it as active; refills if empty.

        Always resets the connection count to 0.
        """
        if not self._proxy_list:
            self._refill_proxies()
        self._active_proxy = self._proxy_list.pop()
        self._connection_count = 0

    # ── Public API ────────────────────────────────────────────────────────────

    def get_ip(self, retries: int | None = None) -> str:
        """Returns the current public IP address via a direct connection.

        Args:
            retries: Number of retry attempts. Defaults to self.retries.

        Returns:
            The public IP address as a string.
        """
        if retries is None:
            retries = self.retries
        try:
            return requests.get(self._IP_URLS[0]).text.rstrip()
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
        """Makes a direct HTTP GET request without routing through a proxy.

        Args:
            url: Target URL.
            params: Optional query parameters.
            cookies: Optional cookies to send.
            stream: If True, streams the response content.
            timeout: Request timeout in seconds. Defaults to self.timeout.
            retries: Retry attempts on failure. Defaults to self.retries.

        Returns:
            The HTTP response object.
        """
        if timeout is None:
            timeout = self.timeout
        if retries is None:
            retries = self.retries

        try:
            if self.show_spinner:
                self._spinner.start()

            if self._session is not None:
                return self._session.get(
                    url=url,
                    params=params,
                    headers=self._header,
                    cookies=cookies,
                    stream=stream,
                    timeout=timeout,
                )
            return requests.get(
                url=url,
                params=params,
                headers=self._new_header(),
                cookies=cookies,
                stream=stream,
                timeout=timeout,
            )
        except Exception:
            if retries <= 0:
                if self.verbose:
                    print(f"*{__name__}* Reached maximum number of retries.")
                retries = self.retries
            if self.verbose:
                print(f"*{__name__}* Retry nº {self.retries + 1 - retries}.")
            return self.get_direct(
                url=url,
                params=params,
                cookies=cookies,
                stream=stream,
                timeout=timeout,
                retries=retries - 1,
            )
        finally:
            self._direct_connection_count += 1
            self._total_connections += 1
            if self.show_spinner:
                self._spinner.stop()

    def get(
        self,
        url: str,
        params: dict | None = None,
        cookies: dict | None = None,
        stream: bool = False,
        timeout: int | None = None,
        retries: int | None = None,
    ) -> Response:
        """Makes an HTTP GET request routed through the active proxy.

        Rotates to a new proxy when max_connections is reached or on repeated failure.
        Without a session, a fresh User-Agent header is generated per request.
        With a session, the header is fixed for the lifetime of that session.

        Args:
            url: Target URL.
            params: Optional query parameters.
            cookies: Optional cookies to send.
            stream: If True, streams the response content.
            timeout: Request timeout in seconds. Defaults to self.timeout.
            retries: Retry attempts on failure. Defaults to self.retries.

        Returns:
            The HTTP response object.
        """
        if timeout is None:
            timeout = self.timeout
        if retries is None:
            retries = self.retries

        if self.max_connections != 0 and self._connection_count >= self.max_connections:
            if self.verbose:
                print(
                    f"{__name__}: Reached max connections. Getting new proxy"
                    f" ({len(self._proxy_list)} remaining)"
                )
            self._rotate_proxy()
            retries = self.retries

        try:
            if self.show_spinner:
                self._spinner.start()

            proxies = self.proxy.as_proxies()
            headers = self._header if self._session else self._new_header()

            if self._session is not None:
                response = self._session.get(
                    url=url,
                    params=params,
                    proxies=proxies,
                    headers=headers,
                    cookies=cookies,
                    stream=stream,
                    timeout=timeout,
                )
            else:
                response = requests.get(
                    url=url,
                    params=params,
                    proxies=proxies,
                    headers=headers,
                    cookies=cookies,
                    stream=stream,
                    timeout=timeout,
                )

            self._connection_count += 1
            self._total_connections += 1
            return response
        except Exception:
            if retries <= 0:
                if self.verbose:
                    print(
                        f"{__name__}: Reached max retries. Getting new proxy"
                        f" ({len(self._proxy_list)} remaining)"
                    )
                self._rotate_proxy()
                retries = self.retries
            if self.verbose:
                print(f"{__name__}: Retry nº {self.retries + 1 - retries}.")
            return self.get(
                url=url,
                params=params,
                cookies=cookies,
                stream=stream,
                timeout=timeout,
                retries=retries - 1,
            )
        finally:
            if self.show_spinner:
                self._spinner.stop()


# ------------------------------------------------------------------------------
