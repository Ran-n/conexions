#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/02/12 19:50:16.098183
#+ Editado:	2022/02/19 16:21:34.813382
# ------------------------------------------------------------------------------
import unittest
import requests
from typing import List

from src.conexions.proxy import Proxy
# ------------------------------------------------------------------------------

class TestProxy(unittest.TestCase):
    lig_proxys: str = 'https://sslproxies.org'
    ligs_ip : List[str] = [
            'https://ip.me',
            'https://icanhazip.com'
            ]

    lig: str = 'https://icanhazip.com'
    ip_clara: str = requests.get(lig).text.rstrip()

    """
    def test_get_espido(self):
        r = Proxy(verbose=False)

        self.assertEqual(r.get_espido(self.lig).text.rstrip(), self.ip_clara)
        self.assertEqual(r.get_cant_conexions_espido(), 1)

        ip = r.get(self.lig).text.rstrip()
        self.assertNotEqual(ip, self.ip_clara)
        self.assertEqual(r.get_cant_conexions(), 1)

        self.assertEqual(r.get_espido(self.lig).text.rstrip(), self.ip_clara)
        self.assertEqual(r.get_cant_conexions_espido(), 2)

    def test_get_proxy(self):
        r = Proxy(verbose=False)

        ip = r.get(self.lig).text.rstrip()
        self.assertNotEqual(ip, self.ip_clara)
        #self.assertEqual(ip, r.get_proxy()['http'].split(':')[1][2:])
        self.assertEqual(r.get_cant_conexions(), 1)

        ip2 = r.get(self.lig).text.rstrip()
        self.assertNotEqual(ip2, self.ip_clara)
        #self.assertEqual(ip2, r.get_proxy()['http'].split(':')[1][2:])
        if ip != ip2:
            self.assertEqual(r.get_cant_conexions(), 1)
        else:
            self.assertEqual(r.get_cant_conexions(), 2)

    def test_get_espido_proxy(self):
        r = Proxy(verbose=False)

        self.assertEqual(r.get_espido(self.lig).text.rstrip(), self.ip_clara)
        self.assertEqual(r.get_cant_conexions_espido(), 1)

        ip = r.get(self.lig).text.rstrip()
        self.assertNotEqual(ip, self.ip_clara)
        #self.assertEqual(ip, r.get_proxy()['http'].split(':')[1][2:])
        self.assertEqual(r.get_cant_conexions(), 1)

    def test_conexion(self):
        r = Proxy(verbose=False)

        self.assertIsNone(r.get_sesion())
        r.sesion()
        self.assertIsNotNone(r.get_sesion())
        r.sesion_fin()
        self.assertIsNone(r.get_sesion())

    def test_get_proxy_conexion(self):
        r = Proxy(verbose=False)
        r.sesion()

        self.assertIsNotNone(r.get_sesion())

        ip = r.get(self.lig).text.rstrip()
        self.assertNotEqual(ip, self.ip_clara)
        self.assertEqual(r.get_cant_conexions(), 1)

        ip2 = r.get(self.lig).text.rstrip()
        self.assertNotEqual(ip2, self.ip_clara)
        if ip != ip2:
            self.assertEqual(r.get_cant_conexions(), 1)
        else:
            self.assertEqual(r.get_cant_conexions(), 2)

        ip3 = r.get(self.lig).text.rstrip()
        self.assertNotEqual(ip3, self.ip_clara)

        if ip3 == ip2:
            if ip3 == ip2:
                self.assertEqual(r.get_cant_conexions(), 3)
            else:
                self.assertEqual(r.get_cant_conexions(), 2)
        else:
            self.assertEqual(r.get_cant_conexions(), 1)

        r.sesion_fin()
        self.assertIsNone(r.get_sesion())
    """

    # Getters

    def test_get_ligazon(self) -> None:
        """
        """

        p = Proxy()

        self.assertEqual(p.get_ligazon(), self.lig_proxys)

    def test_get_sesion(self) -> None:
        """
        """

        p = Proxy()

        self.assertIsNone(p.get_sesion())

    def test_get_verbose(self) -> None:
        """
        """

        self.assertFalse(Proxy().get_verbose())
        self.assertTrue(Proxy(verbose= True).get_verbose())

    def test_get_max_cons(self) -> None:
        """
        """

        self.assertEqual(Proxy().get_max_cons(), 0)
        self.assertEqual(Proxy(max_cons= 5).get_max_cons(), 5)

    def test_get_cant_cons(self) -> None:
        """
        """

        p = Proxy()

        self.assertEqual(p.get_cant_cons(), 0)

    def test_get_cant_cons_espido(self) -> None:
        """
        """

        p = Proxy()

        self.assertEqual(p.get_cant_cons_espido(), 0)

    def test_get_reintentos(self) -> None:
        """
        """

        self.assertEqual(Proxy().get_reintentos(), 5)
        self.assertEqual(Proxy(reintentos= 50).get_reintentos(), 50)

    def test_get_timeout(self) -> None:
        """
        """

        self.assertEqual(Proxy().get_timeout(), 30)
        self.assertEqual(Proxy(timeout= 50).get_timeout(), 50)

    def test_get_cabeceira(self) -> None:
        """
        """

        p = Proxy()

        c1 = p.get_cabeceira()
        c2 = p.get_cabeceira(True)
        self.assertIsNotNone(c1)
        self.assertIsNotNone(c2)
        self.assertEqual(c1, c2)

        c3 = p.get_cabeceira(True)
        self.assertIsNotNone(c3)
        self.assertNotEqual(c1, c3)
        self.assertNotEqual(c2, c3)

        c4 = p.get_cabeceira()
        self.assertIsNotNone(c4)
        self.assertNotEqual(c1, c4)
        self.assertNotEqual(c2, c4)
        self.assertNotEqual(c3, c4)

    def test_get_proxys(self) -> None:
        """
        """

        self.assertIsNotNone(Proxy().get_proxys())

    def test_get_proxy(self) -> None:
        """
        """

        p = Proxy()

        self.assertEqual(p.get_cant_cons(), 0)
        self.assertEqual(p.get_proxy(), p.get_proxy())

    def test_priv_get_proxy(self) -> None:
        """
        """

        p = Proxy()

        self.assertEqual(p.get_cant_cons(), 0)
        self.assertEqual(p._Proxy__get_proxy(), p._Proxy__get_proxy())
        self.assertEqual(p.get_cant_cons(), 2)

        p.set_max_cons(2)
        self.assertEqual(p.get_cant_cons(), 2)
        self.assertEqual(p._Proxy__get_proxy(), p._Proxy__get_proxy())
        self.assertEqual(p.get_cant_cons(), 2)

        p.set_max_cons(1)
        self.assertNotEqual(p._Proxy__get_proxy(), p._Proxy__get_proxy())
        self.assertNotEqual(p._Proxy__get_proxy(), p._Proxy__get_proxy())
        self.assertEqual(p.get_cant_cons(), 1)

    def test_get_ligazons_ip(self) -> None:
        """
        """

        p = Proxy()

        self.assertEqual(p.get_ligazons_ip(), self.ligs_ip)

    # Getters #

    # Setters

    def test_priv_set_ligazon(self) -> None:
        """
        """

        p = Proxy()

        nova_lig = 'a'

        p._Proxy__set_ligazon(nova_lig)
        self.assertEqual(p.get_ligazon(), nova_lig)

    def test_priv_set_ligazon(self) -> None:
        """
        """

        p = Proxy()

        self.assertIsNone(p.get_sesion())

        p.set_sesion()
        self.assertIsNotNone(p.get_sesion())

    def test_set_verbose(self) -> None:
        """
        """

        p = Proxy()
        self.assertFalse(p.get_verbose())

        p.set_verbose(True)
        self.assertTrue(p.get_verbose())

    def test_set_max_cons(self) -> None:
        """
        """

        p = Proxy()
        self.assertEqual(p.get_max_cons(), 0)

        p.set_max_cons(11)
        self.assertEqual(p.get_max_cons(), 11)

    def test_priv_set_cant_cons(self) -> None:
        """
        """

        p = Proxy()
        p._Proxy__set_cant_cons(6)
        self.assertEqual(p.get_cant_cons(), 6)

    def test_priv_set_cant_cons_espido(self) -> None:
        """
        """

        p = Proxy()
        p._Proxy__set_cant_cons_espido(6)
        self.assertEqual(p.get_cant_cons_espido(), 6)

    def test_set_reintentos(self) -> None:
        """
        """

        p = Proxy()
        self.assertEqual(p.get_reintentos(), 5)

        p.set_reintentos(111)
        self.assertEqual(p.get_reintentos(), 111)

    def test_set_timeout(self) -> None:
        """
        """

        p = Proxy()
        self.assertEqual(p.get_timeout(), 30)

        p.set_timeout(1411)
        self.assertEqual(p.get_timeout(), 1411)

    def test_set_cabeceira(self) -> None:
        """
        """

        p = Proxy()

        c1 = p.get_cabeceira()
        c2 = p.get_cabeceira()
        p.set_cabeceira()
        c3 = p.get_cabeceira()
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)
        self.assertNotEqual(c2, c3)

    def test_set_proxys(self) -> None:
        """
        """

        p = Proxy()

        l1 = p.get_proxys()
        self.assertIsNotNone(l1)

        p._Proxy__lst_proxys = []
        self.assertEqual(p.get_proxys(), [])

        p.set_proxys()
        l2 = p.get_proxys()
        self.assertIsNotNone(l2)

    def test_set_proxy(self) -> None:
        """
        """

        p = Proxy()

        self.assertIsNotNone(p.get_proxy())

        proxy1 = p.get_proxy()
        p.set_proxy()
        self.assertNotEqual(proxy1, p.get_proxy())

        while len(p.get_proxys()) > 0:
            p.set_proxy()
        self.assertEqual(len(p.get_proxys()), 0)

        # ó tentar sacar un novo proxy da lista baleira fará un escrapeo da páxina e recheo da lista
        p.set_proxy()
        self.assertNotEqual(len(p.get_proxys()), 0)

    # Setters #

    def test_get_ip(self) -> None:
        """
        """

        p = Proxy()

        self.assertEqual(p.get_ip(), self.ip_clara)

    def test_get_espido(self) -> None:
        """
        """

        p = Proxy()

        ip_usada = p.get_espido(self.lig).text.rstrip()

        self.assertIsNotNone(ip_usada)
        self.assertEqual(ip_usada, self.ip_clara)

        self.assertTrue(p.get_cant_cons_espido() >= 1)

        p.set_max_cons(1)
        ip_usada2 = p.get_espido(self.lig).text.rstrip()
        self.assertEqual(ip_usada, ip_usada2)
        self.assertTrue(p.get_cant_cons() <= 1)

    def test_get(self) -> None:
        """
        """

        p = Proxy()

        ip_usada = p.get(self.lig).text.rstrip()

        self.assertEqual(p.get_proxy().https, 'yes')

        self.assertIsNotNone(ip_usada)
        self.assertNotEqual(ip_usada, self.ip_clara)
        self.assertEqual(ip_usada, p.get_proxy().ip)

        self.assertTrue(p.get_cant_cons() >= 1)

        p.set_max_cons(1)
        ip_usada2 = p.get(self.lig).text.rstrip()
        self.assertNotEqual(ip_usada, ip_usada2)
        self.assertTrue(p.get_cant_cons() <= 1)
# ------------------------------------------------------------------------------
