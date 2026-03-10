#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Authors:	Ran#
#+ Created:	2022/02/12 19:50:16.098183
#+ Revised:	2026/03/10 21:23:26.298045
# ------------------------------------------------------------------------------
import unittest
import requests

from conexions.proxy import Proxy
# ------------------------------------------------------------------------------

class TestProxy(unittest.TestCase):
    proxy_url: str = 'https://sslproxies.org'
    ip_urls: list[str] = [
            'https://ip.me',
            'https://icanhazip.com'
            ]

    url: str = 'https://icanhazip.com'
    real_ip: str = requests.get(url).text.rstrip()

    """
    def test_get_direct(self):
        r = Proxy(verbose=False)

        self.assertEqual(r.get_direct(self.url).text.rstrip(), self.real_ip)
        self.assertEqual(r.get_direct_connection_count(), 1)

        ip = r.get(self.url).text.rstrip()
        self.assertNotEqual(ip, self.real_ip)
        self.assertEqual(r.get_connection_count(), 1)

        self.assertEqual(r.get_direct(self.url).text.rstrip(), self.real_ip)
        self.assertEqual(r.get_direct_connection_count(), 2)

    def test_get_proxy(self):
        r = Proxy(verbose=False)

        ip = r.get(self.url).text.rstrip()
        self.assertNotEqual(ip, self.real_ip)
        #self.assertEqual(ip, r.get_proxy()['http'].split(':')[1][2:])
        self.assertEqual(r.get_connection_count(), 1)

        ip2 = r.get(self.url).text.rstrip()
        self.assertNotEqual(ip2, self.real_ip)
        #self.assertEqual(ip2, r.get_proxy()['http'].split(':')[1][2:])
        if ip != ip2:
            self.assertEqual(r.get_connection_count(), 1)
        else:
            self.assertEqual(r.get_connection_count(), 2)

    def test_get_direct_proxy(self):
        r = Proxy(verbose=False)

        self.assertEqual(r.get_direct(self.url).text.rstrip(), self.real_ip)
        self.assertEqual(r.get_direct_connection_count(), 1)

        ip = r.get(self.url).text.rstrip()
        self.assertNotEqual(ip, self.real_ip)
        #self.assertEqual(ip, r.get_proxy()['http'].split(':')[1][2:])
        self.assertEqual(r.get_connection_count(), 1)

    def test_session(self):
        r = Proxy(verbose=False)

        self.assertIsNone(r.get_session())
        r.set_session()
        self.assertIsNotNone(r.get_session())
        r.set_session(reset=True)
        self.assertIsNone(r.get_session())

    def test_get_proxy_session(self):
        r = Proxy(verbose=False)
        r.set_session()

        self.assertIsNotNone(r.get_session())

        ip = r.get(self.url).text.rstrip()
        self.assertNotEqual(ip, self.real_ip)
        self.assertEqual(r.get_connection_count(), 1)

        ip2 = r.get(self.url).text.rstrip()
        self.assertNotEqual(ip2, self.real_ip)
        if ip != ip2:
            self.assertEqual(r.get_connection_count(), 1)
        else:
            self.assertEqual(r.get_connection_count(), 2)

        ip3 = r.get(self.url).text.rstrip()
        self.assertNotEqual(ip3, self.real_ip)

        if ip3 == ip2:
            if ip3 == ip2:
                self.assertEqual(r.get_connection_count(), 3)
            else:
                self.assertEqual(r.get_connection_count(), 2)
        else:
            self.assertEqual(r.get_connection_count(), 1)

        r.set_session(reset=True)
        self.assertIsNone(r.get_session())
    """

    # Getters

    def test_get_url(self) -> None:
        p = Proxy()

        self.assertEqual(p.get_url(), self.proxy_url)

    def test_get_session(self) -> None:
        p = Proxy()

        self.assertIsNone(p.get_session())

    def test_get_verbose(self) -> None:
        self.assertFalse(Proxy().get_verbose())
        self.assertTrue(Proxy(verbose= True).get_verbose())

    def test_get_show_spinner(self) -> None:
        self.assertFalse(Proxy().get_show_spinner())
        self.assertTrue(Proxy(show_spinner= True).get_show_spinner())

    def test_get_max_connections(self) -> None:
        self.assertEqual(Proxy().get_max_connections(), 0)
        self.assertEqual(Proxy(max_connections= 5).get_max_connections(), 5)

    def test_get_total_connections(self) -> None:
        p = Proxy()

        self.assertEqual(p.get_total_connections(), 0)

    def test_get_connection_count(self) -> None:
        p = Proxy()

        self.assertEqual(p.get_connection_count(), 0)

    def test_get_direct_connection_count(self) -> None:
        p = Proxy()

        self.assertEqual(p.get_direct_connection_count(), 0)

    def test_get_retries(self) -> None:
        self.assertEqual(Proxy().get_retries(), 5)
        self.assertEqual(Proxy(retries= 50).get_retries(), 50)

    def test_get_timeout(self) -> None:
        self.assertEqual(Proxy().get_timeout(), 30)
        self.assertEqual(Proxy(timeout= 50).get_timeout(), 50)

    def test_get_header(self) -> None:
        p = Proxy()

        h1 = p.get_header()
        h2 = p.get_header(True)
        self.assertIsNotNone(h1)
        self.assertIsNotNone(h2)
        self.assertEqual(h1, h2)

        h3 = p.get_header(True)
        self.assertIsNotNone(h3)
        self.assertNotEqual(h1, h3)
        self.assertNotEqual(h2, h3)

        h4 = p.get_header()
        self.assertIsNotNone(h4)
        self.assertNotEqual(h1, h4)
        self.assertNotEqual(h2, h4)
        self.assertNotEqual(h3, h4)

    def test_get_proxies(self) -> None:
        self.assertIsNotNone(Proxy().get_proxies())

    def test_get_proxy(self) -> None:
        p = Proxy()

        self.assertEqual(p.get_connection_count(), 0)
        self.assertEqual(p.get_proxy(), p.get_proxy())

    def test_priv_get_proxy(self) -> None:
        p = Proxy()

        self.assertEqual(p.get_connection_count(), 0)
        self.assertEqual(p._Proxy__get_proxy(), p._Proxy__get_proxy())
        self.assertEqual(p.get_connection_count(), 2)

        p.set_max_connections(2)
        self.assertEqual(p.get_connection_count(), 2)
        self.assertEqual(p._Proxy__get_proxy(), p._Proxy__get_proxy())
        self.assertEqual(p.get_connection_count(), 2)

        p.set_max_connections(1)
        self.assertNotEqual(p._Proxy__get_proxy(), p._Proxy__get_proxy())
        self.assertNotEqual(p._Proxy__get_proxy(), p._Proxy__get_proxy())
        self.assertEqual(p.get_connection_count(), 1)

    def test_get_ip_urls(self) -> None:
        p = Proxy()

        self.assertEqual(p.get_ip_urls(), self.ip_urls)

    # Getters #

    # Setters

    def test_priv_set_url(self) -> None:
        p = Proxy()

        new_url = 'a'

        p._Proxy__set_url(new_url)
        self.assertEqual(p.get_url(), new_url)

    def test_set_session(self) -> None:
        p = Proxy()

        self.assertIsNone(p.get_session())

        p.set_session()
        self.assertIsNotNone(p.get_session())

    def test_set_verbose(self) -> None:
        p = Proxy()
        self.assertFalse(p.get_verbose())

        p.set_verbose(True)
        self.assertTrue(p.get_verbose())

    def test_set_show_spinner(self) -> None:
        p = Proxy()
        self.assertFalse(p.get_show_spinner())

        p.set_show_spinner(True)
        self.assertTrue(p.get_show_spinner())

    def test_set_max_connections(self) -> None:
        p = Proxy()
        self.assertEqual(p.get_max_connections(), 0)

        p.set_max_connections(11)
        self.assertEqual(p.get_max_connections(), 11)

    def test_priv_set_total_connections(self) -> None:
        p = Proxy()
        p._Proxy__set_total_connections(60)
        self.assertEqual(p.get_total_connections(), 60)

    def test_priv_set_connection_count(self) -> None:
        p = Proxy()
        p._Proxy__set_connection_count(6)
        self.assertEqual(p.get_connection_count(), 6)

    def test_priv_set_direct_connection_count(self) -> None:
        p = Proxy()
        p._Proxy__set_direct_connection_count(6)
        self.assertEqual(p.get_direct_connection_count(), 6)

    def test_set_retries(self) -> None:
        p = Proxy()
        self.assertEqual(p.get_retries(), 5)

        p.set_retries(111)
        self.assertEqual(p.get_retries(), 111)

    def test_set_timeout(self) -> None:
        p = Proxy()
        self.assertEqual(p.get_timeout(), 30)

        p.set_timeout(1411)
        self.assertEqual(p.get_timeout(), 1411)

    def test_set_header(self) -> None:
        p = Proxy()

        h1 = p.get_header()
        h2 = p.get_header()
        p.set_header()
        h3 = p.get_header()
        self.assertEqual(h1, h2)
        self.assertNotEqual(h1, h3)
        self.assertNotEqual(h2, h3)

    def test_set_proxies(self) -> None:
        p = Proxy()

        l1 = p.get_proxies()
        self.assertIsNotNone(l1)

        p._Proxy__proxy_list = []
        self.assertEqual(p.get_proxies(), [])

        p.set_proxies()
        l2 = p.get_proxies()
        self.assertIsNotNone(l2)

    def test_set_proxy(self) -> None:
        p = Proxy()

        self.assertIsNotNone(p.get_proxy())

        proxy1 = p.get_proxy()
        p.set_proxy()
        self.assertNotEqual(proxy1, p.get_proxy())

        while len(p.get_proxies()) > 0:
            p.set_proxy()
        self.assertEqual(len(p.get_proxies()), 0)

        # trying to get a new proxy from an empty list triggers a re-scrape
        p.set_proxy()
        self.assertNotEqual(len(p.get_proxies()), 0)

    # Setters #

    def test_get_ip(self) -> None:
        p = Proxy()

        self.assertEqual(p.get_ip(), self.real_ip)

    def test_get_direct(self) -> None:
        p = Proxy()

        ip_used = p.get_direct(self.url).text.rstrip()

        self.assertIsNotNone(ip_used)
        self.assertEqual(ip_used, self.real_ip)

        self.assertTrue(p.get_direct_connection_count() >= 1)

        p.set_max_connections(1)
        ip_used2 = p.get_direct(self.url).text.rstrip()
        self.assertEqual(ip_used, ip_used2)
        self.assertTrue(p.get_connection_count() <= 1)

        self.assertTrue(p.get_total_connections() == 2)

    def test_get(self) -> None:
        p = Proxy()

        ip_used = p.get(self.url).text.rstrip()

        self.assertEqual(p.get_proxy().https, 'yes')

        self.assertIsNotNone(ip_used)
        self.assertNotEqual(ip_used, self.real_ip)

        len1 = len(p.get_proxies())
        self.assertTrue(p.get_connection_count() >= 1)

        p.set_max_connections(1)
        ip_used2 = p.get(self.url).text.rstrip()

        self.assertNotEqual(ip_used2, self.real_ip)

        self.assertNotEqual(len1, len(p.get_proxies()))
        self.assertNotEqual(ip_used, ip_used2)
        self.assertTrue(p.get_connection_count() <= 1)

        self.assertTrue(p.get_total_connections() >= 2)

        p.get_direct(self.url).text.rstrip()
        self.assertTrue(p.get_total_connections() >= 3)
# ------------------------------------------------------------------------------
