#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Authors:	Ran#
#+ Created:	2022/02/12 19:50:16.098183
#+ Revised:	2026/03/11 07:50:20.231819
# ------------------------------------------------------------------------------
import pytest
import requests

from conexions.proxy import Proxy
# ------------------------------------------------------------------------------

PROXY_URL: str = 'https://sslproxies.org'
IP_URLS: list[str] = [
        'https://ip.me',
        'https://icanhazip.com'
        ]
URL: str = 'https://icanhazip.com'

# ------------------------------------------------------------------------------

@pytest.fixture(scope='module')
def real_ip() -> str:
    return requests.get(URL).text.rstrip()

@pytest.fixture
def proxy() -> Proxy:
    return Proxy()

# ------------------------------------------------------------------------------

# Getters

def test_get_url(proxy) -> None:
    assert proxy.get_url() == PROXY_URL

def test_get_session(proxy) -> None:
    assert proxy.get_session() is None

def test_get_verbose() -> None:
    assert not Proxy().get_verbose()
    assert Proxy(verbose=True).get_verbose()

def test_get_show_spinner() -> None:
    assert not Proxy().get_show_spinner()
    assert Proxy(show_spinner=True).get_show_spinner()

def test_get_max_connections() -> None:
    assert Proxy().get_max_connections() == 0
    assert Proxy(max_connections=5).get_max_connections() == 5

def test_get_total_connections(proxy) -> None:
    assert proxy.get_total_connections() == 0

def test_get_connection_count(proxy) -> None:
    assert proxy.get_connection_count() == 0

def test_get_direct_connection_count(proxy) -> None:
    assert proxy.get_direct_connection_count() == 0

def test_get_retries() -> None:
    assert Proxy().get_retries() == 5
    assert Proxy(retries=50).get_retries() == 50

def test_get_timeout() -> None:
    assert Proxy().get_timeout() == 30
    assert Proxy(timeout=50).get_timeout() == 50

def test_get_header(proxy) -> None:
    h1 = proxy.get_header()
    h2 = proxy.get_header(True)
    assert h1 is not None
    assert h2 is not None
    assert h1 == h2

    h3 = proxy.get_header(True)
    assert h3 is not None
    assert h1 != h3
    assert h2 != h3

    h4 = proxy.get_header()
    assert h4 is not None
    assert h1 != h4
    assert h2 != h4
    assert h3 != h4

def test_get_proxies(proxy) -> None:
    assert proxy.get_proxies() is not None

def test_get_proxy(proxy) -> None:
    assert proxy.get_connection_count() == 0
    assert proxy.get_proxy() == proxy.get_proxy()

def test_priv_get_proxy(proxy) -> None:
    assert proxy.get_connection_count() == 0
    assert proxy._Proxy__get_proxy() == proxy._Proxy__get_proxy()
    assert proxy.get_connection_count() == 2

    proxy.set_max_connections(2)
    assert proxy.get_connection_count() == 2
    assert proxy._Proxy__get_proxy() == proxy._Proxy__get_proxy()
    assert proxy.get_connection_count() == 2

    proxy.set_max_connections(1)
    assert proxy._Proxy__get_proxy() != proxy._Proxy__get_proxy()
    assert proxy._Proxy__get_proxy() != proxy._Proxy__get_proxy()
    assert proxy.get_connection_count() == 1

def test_get_ip_urls(proxy) -> None:
    assert proxy.get_ip_urls() == IP_URLS

# Getters #

# Setters

def test_priv_set_url(proxy) -> None:
    new_url = 'a'
    proxy._Proxy__set_url(new_url)
    assert proxy.get_url() == new_url

def test_set_session(proxy) -> None:
    assert proxy.get_session() is None
    proxy.set_session()
    assert proxy.get_session() is not None

def test_set_verbose(proxy) -> None:
    assert not proxy.get_verbose()
    proxy.set_verbose(True)
    assert proxy.get_verbose()

def test_set_show_spinner(proxy) -> None:
    assert not proxy.get_show_spinner()
    proxy.set_show_spinner(True)
    assert proxy.get_show_spinner()

def test_set_max_connections(proxy) -> None:
    assert proxy.get_max_connections() == 0
    proxy.set_max_connections(11)
    assert proxy.get_max_connections() == 11

def test_priv_set_total_connections(proxy) -> None:
    proxy._Proxy__set_total_connections(60)
    assert proxy.get_total_connections() == 60

def test_priv_set_connection_count(proxy) -> None:
    proxy._Proxy__set_connection_count(6)
    assert proxy.get_connection_count() == 6

def test_priv_set_direct_connection_count(proxy) -> None:
    proxy._Proxy__set_direct_connection_count(6)
    assert proxy.get_direct_connection_count() == 6

def test_set_retries(proxy) -> None:
    assert proxy.get_retries() == 5
    proxy.set_retries(111)
    assert proxy.get_retries() == 111

def test_set_timeout(proxy) -> None:
    assert proxy.get_timeout() == 30
    proxy.set_timeout(1411)
    assert proxy.get_timeout() == 1411

def test_set_header(proxy) -> None:
    h1 = proxy.get_header()
    h2 = proxy.get_header()
    proxy.set_header()
    h3 = proxy.get_header()
    assert h1 == h2
    assert h1 != h3
    assert h2 != h3

def test_set_proxies(proxy) -> None:
    l1 = proxy.get_proxies()
    assert l1 is not None

    proxy._Proxy__proxy_list = []
    assert proxy.get_proxies() == []

    proxy.set_proxies()
    assert proxy.get_proxies() is not None

def test_set_proxy(proxy) -> None:
    assert proxy.get_proxy() is not None

    proxy1 = proxy.get_proxy()
    proxy.set_proxy()
    assert proxy1 != proxy.get_proxy()

    while len(proxy.get_proxies()) > 0:
        proxy.set_proxy()
    assert len(proxy.get_proxies()) == 0

    # trying to get a new proxy from an empty list triggers a re-scrape
    proxy.set_proxy()
    assert len(proxy.get_proxies()) != 0

# Setters #

def test_get_ip(proxy, real_ip) -> None:
    assert proxy.get_ip() == real_ip

def test_get_direct(proxy, real_ip) -> None:
    ip_used = proxy.get_direct(URL).text.rstrip()
    assert ip_used is not None
    assert ip_used == real_ip
    assert proxy.get_direct_connection_count() >= 1

    proxy.set_max_connections(1)
    ip_used2 = proxy.get_direct(URL).text.rstrip()
    assert ip_used == ip_used2
    assert proxy.get_connection_count() <= 1
    assert proxy.get_total_connections() == 2

def test_get(proxy, real_ip) -> None:
    ip_used = proxy.get(URL).text.rstrip()
    assert proxy.get_proxy().https == 'yes'
    assert ip_used is not None
    assert ip_used != real_ip

    len1 = len(proxy.get_proxies())
    assert proxy.get_connection_count() >= 1

    proxy.set_max_connections(1)
    ip_used2 = proxy.get(URL).text.rstrip()
    assert ip_used2 != real_ip
    assert len1 != len(proxy.get_proxies())
    assert ip_used != ip_used2
    assert proxy.get_connection_count() <= 1
    assert proxy.get_total_connections() >= 2

    proxy.get_direct(URL).text.rstrip()
    assert proxy.get_total_connections() >= 3

def test_session_lifecycle(real_ip) -> None:
    p = Proxy()

    assert p.get_session() is None
    p.set_session()
    assert p.get_session() is not None

    ip = p.get(URL).text.rstrip()
    assert ip != real_ip
    assert p.get_connection_count() == 1

    ip2 = p.get(URL).text.rstrip()
    assert ip2 != real_ip
    if ip != ip2:
        assert p.get_connection_count() == 1
    else:
        assert p.get_connection_count() == 2

    ip3 = p.get(URL).text.rstrip()
    assert ip3 != real_ip
    if ip3 == ip2:
        assert p.get_connection_count() == 3
    else:
        assert p.get_connection_count() == 1

    p.set_session(reset=True)
    assert p.get_session() is None
# ------------------------------------------------------------------------------
