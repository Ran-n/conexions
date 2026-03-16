#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# + Authors:	Ran#
# + Created:	2022/02/13 16:43:37.259437
# + Revised:	2026/03/16 15:38:39.227083
# ------------------------------------------------------------------------------

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from requests.exceptions import ConnectionError
from requests.models import Response
from requests.sessions import Session
from yaspin import yaspin
from yaspin.spinners import Spinners

from .anonymity import Anonymity
from .country import Country
from .excepcions import PageChangedError
from .protocol import Protocol
from .proxy import Proxy

# ------------------------------------------------------------------------------


class ProxyClient:
    """Web client with automatic proxy rotation sourced from free-proxy-list.net.

    Scrapes all proxies on initialisation. Each ``get()`` call races up to
    ``_REQUEST_BATCH`` filter-matching proxies in parallel and returns the first
    successful response. Failed proxies are discarded; surviving non-winners go
    back into the pool. Proxies are filtered by protocol, country, and
    google-compatibility at selection time.
    """

    _URL: str = "https://free-proxy-list.net/"
    _IP_URLS: list[str] = ["https://ip.me", "https://icanhazip.com"]
    _REQUEST_BATCH: int = 5

    def __init__(
        self,
        max_connections: int = 0,
        retries: int = 3,
        timeout: int = 10,
        verbose: bool = False,
        show_spinner: bool = False,
        protocols: list[Protocol] | None = None,
        countries: list[Country] | None = None,
        anonymities: list[Anonymity] | None = None,
        google: bool | None = True,
    ) -> None:
        """Initializes the ProxyClient, scrapes the proxy list, and sets the first proxy.

        Args:
            max_connections: Max uses per proxy before rotating. 0 means unlimited.
            retries: Number of retry attempts on connection failure. Defaults to 3.
            timeout: Request timeout in seconds. Defaults to 10.
            verbose: If True, prints status messages to stdout.
            show_spinner: If True, shows a spinner during requests. Defaults to False.
            protocols: Protocols to accept. Defaults to ``[Protocol.HTTPS]``.
            countries: Countries to filter by (e.g. ``[Country.US, Country.DE]``).
                ``None`` means no country filter.
            anonymities: Anonymity levels to accept (e.g. ``[Anonymity.ELITE]``).
                Defaults to ``[Anonymity.ELITE]``. ``None`` means no anonymity filter.
            google: If ``True``, only accept Google-compatible proxies (default). If
                ``False``, only accept non-Google-compatible proxies. ``None`` means no filter.
        """
        self.max_connections = max_connections
        self.retries: int = retries
        self.timeout: int = timeout
        self.verbose: bool = verbose
        self.show_spinner: bool = show_spinner
        self.protocols: list[Protocol] = protocols if protocols is not None else [Protocol.HTTPS]
        self.countries: list[Country] | None = countries
        self.anonymities: list[Anonymity] | None = anonymities if anonymities is not None else [Anonymity.ELITE]
        self.google: bool | None = google

        self._session: Session | None = None
        self._total_connections: int = 0
        self._connection_count: int = 0
        self._direct_connection_count: int = 0
        self._last_elapsed: float = 0.0
        self._spinner = yaspin(text="Connecting", spinner=Spinners.bouncingBall)

        self._header: dict[str, str] = self._new_header()
        self._proxy_list: list[Proxy] = []
        self._active_proxy: Proxy
        self._refill_proxies()
        self._rotate_proxy()

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

    @property
    def last_elapsed(self) -> float:
        """Elapsed seconds of the last get / get_direct call (retries included)."""
        return self._last_elapsed

    @property
    def proxy_count(self) -> int:
        """Number of proxies in the pool that match the current filter (excludes active proxy)."""
        return sum(1 for p in self._proxy_list if self._matches_filter(p))

    @property
    def proxy_count_total(self) -> int:
        """Total number of proxies in the pool regardless of filter (excludes active proxy)."""
        return len(self._proxy_list)

    @property
    def proxies(self) -> list[Proxy]:
        """All proxies currently in the pool (excludes active proxy)."""
        return list(self._proxy_list)

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
        """Manually rotates to the next filter-matching proxy."""
        self._rotate_proxy()

    def refill_proxies(self) -> None:
        """Re-scrapes the proxy source page to refill the proxy list."""
        self._refill_proxies()

    # ── Internal helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _new_header() -> dict[str, str]:
        return {"User-Agent": UserAgent().random}

    def _matches_filter(self, proxy: Proxy) -> bool:
        """Returns True if the proxy matches the configured protocol, country, and google filters.

        Protocol matching: an HTTPS proxy satisfies a ``Protocol.HTTP`` filter
        because HTTPS proxies also speak HTTP. The reverse is not true.
        """
        protocol_match = proxy.protocol in self.protocols or (
            Protocol.HTTP in self.protocols and proxy.protocol == Protocol.HTTPS
        )
        country_match = self.countries is None or (
            proxy.country is not None and proxy.country in self.countries
        )
        anonymity_match = self.anonymities is None or proxy.anonymity in self.anonymities
        google_match = self.google is None or proxy.google == self.google
        return protocol_match and country_match and anonymity_match and google_match

    def _refill_proxies(self) -> None:
        """Scrapes the proxy source and fills the list with all available proxies.

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
            self._proxy_list.insert(0, proxy)

    def _rotate_proxy(self) -> None:
        """Pops the next filter-matching proxy from the pool and sets it as active.

        Refills the pool automatically if it runs dry. Always resets the
        connection count to 0.
        """
        while True:
            if not self._proxy_list:
                self._refill_proxies()
            candidate = self._proxy_list.pop()
            if self._matches_filter(candidate):
                self._active_proxy = candidate
                break
        self._connection_count = 0

    def _get_via(
        self,
        proxy: Proxy,
        url: str,
        params: dict | None,
        cookies: dict | None,
        stream: bool,
        timeout: int,
    ) -> Response:
        """Performs a single GET request through the given proxy.

        Raises on any network error so the caller can treat it as a failure.
        """
        return requests.get(
            url=url,
            params=params,
            proxies=proxy.as_proxies(),
            headers=self._new_header(),
            cookies=cookies,
            stream=stream,
            timeout=timeout,
        )

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

        _start_time = time.perf_counter()
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
            self._last_elapsed = time.perf_counter() - _start_time
            if self.show_spinner:
                self._spinner.stop()

    def get(
        self,
        url: str,
        params: dict | None = None,
        cookies: dict | None = None,
        stream: bool = False,
        timeout: int | None = None,
    ) -> Response:
        """Makes an HTTP GET request by racing up to ``_REQUEST_BATCH`` proxies in parallel.

        Collects up to ``_REQUEST_BATCH`` filter-matching proxies from the pool
        and fires them all concurrently. The first successful response wins:
        that proxy becomes the active proxy and the response is returned.
        Proxies that fail are discarded; proxies that also succeed (but arrived
        later) go back into the pool. If every proxy in the batch fails, a new
        batch is tried immediately.

        Args:
            url: Target URL.
            params: Optional query parameters.
            cookies: Optional cookies to send.
            stream: If True, streams the response content.
            timeout: Request timeout in seconds. Defaults to self.timeout.

        Returns:
            The HTTP response object from the first proxy to succeed.
        """
        if timeout is None:
            timeout = self.timeout

        _start_time = time.perf_counter()
        try:
            if self.show_spinner:
                self._spinner.start()

            while True:
                # collect up to _REQUEST_BATCH filter-matching candidates
                candidates: list[Proxy] = []
                while len(candidates) < self._REQUEST_BATCH:
                    if not self._proxy_list:
                        self._refill_proxies()
                    candidate = self._proxy_list.pop()
                    if self._matches_filter(candidate):
                        candidates.append(candidate)

                if self.verbose:
                    print(f"{__name__}: Racing {len(candidates)} proxies.")

                winner: Proxy | None = None
                response: Response | None = None
                survivors: list[Proxy] = []

                with ThreadPoolExecutor(max_workers=len(candidates)) as executor:
                    future_to_proxy = {
                        executor.submit(
                            self._get_via, p, url, params, cookies, stream, timeout
                        ): p
                        for p in candidates
                    }
                    for future in as_completed(future_to_proxy):
                        proxy = future_to_proxy[future]
                        try:
                            result = future.result()
                            if winner is None:
                                winner = proxy
                                response = result
                            else:
                                survivors.append(proxy)
                        except Exception:
                            pass  # failed proxy — discard

                if winner is not None:
                    self._active_proxy = winner
                    self._proxy_list.extend(survivors)
                    self._connection_count += 1
                    self._total_connections += 1
                    return response  # type: ignore[return-value]

                if self.verbose:
                    print(f"{__name__}: All proxies in batch failed, retrying.")

        finally:
            self._last_elapsed = time.perf_counter() - _start_time
            if self.show_spinner:
                self._spinner.stop()


# ------------------------------------------------------------------------------
