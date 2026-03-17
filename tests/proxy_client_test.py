#! /usr/bin/env python3
# ------------------------------------------------------------------------------
# + Authors:	Ran#
# + Created:	2022/02/12 19:50:16.098183
# + Revised:	2026/03/11 11:27:46.318346
# ------------------------------------------------------------------------------
import pytest
import requests

from conexions.proxy import Proxy
from conexions.proxy_client import ProxyClient

# ------------------------------------------------------------------------------

PROXY_URL: str = "https://free-proxy-list.net/"
IP_URLS: list[str] = ["https://ip.me", "https://icanhazip.com"]
URL: str = "https://icanhazip.com"

# ------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def real_ip() -> str:
    return requests.get(URL).text.rstrip()


@pytest.fixture
def client() -> ProxyClient:
    return ProxyClient()


# ------------------------------------------------------------------------------

# Config attributes


def test_default_config() -> None:
    c = ProxyClient()
    assert c.max_connections == 0
    assert c.retries == 5
    assert c.timeout == 30
    assert not c.verbose
    assert not c.show_spinner


def test_custom_config() -> None:
    c = ProxyClient(max_connections=5, retries=10, timeout=60, verbose=True, show_spinner=True)
    assert c.max_connections == 5
    assert c.retries == 10
    assert c.timeout == 60
    assert c.verbose
    assert c.show_spinner


def test_config_is_mutable(client) -> None:
    client.max_connections = 11
    assert client.max_connections == 11

    client.retries = 111
    assert client.retries == 111

    client.timeout = 1411
    assert client.timeout == 1411

    client.verbose = True
    assert client.verbose

    client.show_spinner = True
    assert client.show_spinner


# Counters (read-only properties)


def test_initial_counters(client) -> None:
    assert client.total_connections == 0
    assert client.connection_count == 0
    assert client.direct_connection_count == 0


# Header


def test_header_is_set(client) -> None:
    assert client._header is not None
    assert "User-Agent" in client._header


def test_refresh_header(client) -> None:
    h1 = client._header
    client.refresh_header()
    assert client._header != h1


# Session


def test_session_defaults_to_none(client) -> None:
    assert client._session is None


def test_open_session(client) -> None:
    assert client._session is None
    client.open_session()
    assert client._session is not None


def test_close_session(client) -> None:
    client.open_session()
    assert client._session is not None
    client.close_session()
    assert client._session is None


def test_close_session_when_already_none(client) -> None:
    assert client._session is None
    client.close_session()
    assert client._session is None


# Class constants


def test_url_constant(client) -> None:
    assert client._URL == PROXY_URL


def test_ip_urls_constant(client) -> None:
    assert client._IP_URLS == IP_URLS


# Proxy list


def test_proxy_list_is_populated(client) -> None:
    assert isinstance(client._proxy_list, list)
    assert len(client._proxy_list) > 0
    assert all(isinstance(p, Proxy) for p in client._proxy_list)


def test_refill_proxies(client) -> None:
    client._proxy_list = []
    assert client._proxy_list == []

    client.refill_proxies()
    assert len(client._proxy_list) > 0


# Active proxy and rotation


def test_proxy_returns_proxy(client) -> None:
    assert isinstance(client.proxy, Proxy)


def test_proxy_stable_without_rotation(client) -> None:
    assert client.connection_count == 0
    p1 = client.proxy
    p2 = client.proxy
    assert p1 == p2


def test_proxy_auto_rotates_at_max_connections(client) -> None:
    client.max_connections = 1
    p1 = client.proxy
    client._connection_count = 1
    p2 = client.proxy
    assert p1 != p2
    assert client.connection_count == 0


def test_rotate_proxy_changes_proxy(client) -> None:
    p1 = client.proxy
    client.rotate_proxy()
    p2 = client.proxy
    assert p1 != p2


def test_rotate_proxy_resets_connection_count(client) -> None:
    client._connection_count = 5
    assert client.connection_count == 5
    client.rotate_proxy()
    assert client.connection_count == 0


def test_rotate_proxy_refills_when_empty(client) -> None:
    while client._proxy_list:
        client.rotate_proxy()
    assert len(client._proxy_list) == 0

    client.rotate_proxy()
    assert len(client._proxy_list) > 0


# get_ip


def test_get_ip(client, real_ip) -> None:
    assert client.get_ip() == real_ip


# get_direct


def test_get_direct(client, real_ip) -> None:
    ip = client.get_direct(URL).text.rstrip()
    assert ip == real_ip
    assert client.direct_connection_count == 1
    assert client.connection_count == 0
    assert client.total_connections == 1

    ip2 = client.get_direct(URL).text.rstrip()
    assert ip2 == real_ip
    assert client.direct_connection_count == 2
    assert client.total_connections == 2


def test_get_direct_with_session(client, real_ip) -> None:
    client.open_session()
    assert client._session is not None
    ip = client.get_direct(URL).text.rstrip()
    assert ip == real_ip
    assert client.direct_connection_count >= 1


def test_get_direct_does_not_affect_connection_count(client) -> None:
    client.get_direct(URL)
    assert client.connection_count == 0


# get (proxied)


def test_get(client, real_ip) -> None:
    ip = client.get(URL).text.rstrip()
    assert client.proxy.https == "yes"
    assert ip != real_ip
    assert client.connection_count >= 1


def test_get_rotates_at_max_connections(client, real_ip) -> None:
    len_before = len(client._proxy_list)
    client.max_connections = 1

    ip1 = client.get(URL).text.rstrip()
    ip2 = client.get(URL).text.rstrip()
    assert ip1 != real_ip
    assert ip2 != real_ip
    assert ip1 != ip2
    assert len(client._proxy_list) != len_before
    assert client.connection_count <= 1


def test_get_total_connections_across_methods(client) -> None:
    client.get(URL)
    client.get(URL)
    client.get_direct(URL)
    assert client.total_connections >= 3


# Session lifecycle


def test_session_lifecycle(real_ip) -> None:
    c = ProxyClient()

    assert c._session is None
    c.open_session()
    assert c._session is not None

    ip = c.get(URL).text.rstrip()
    assert ip != real_ip
    assert c.connection_count == 1

    ip2 = c.get(URL).text.rstrip()
    assert ip2 != real_ip
    if ip != ip2:
        assert c.connection_count == 1
    else:
        assert c.connection_count == 2

    ip3 = c.get(URL).text.rstrip()
    assert ip3 != real_ip
    if ip3 == ip2:
        assert c.connection_count == 3
    else:
        assert c.connection_count == 1

    c.close_session()
    assert c._session is None


# ------------------------------------------------------------------------------
