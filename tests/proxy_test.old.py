#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/02/12 19:50:16.098183
#+ Editado:	2022/02/13 14:50:31.057445
# ------------------------------------------------------------------------------
import unittest
import requests

from src.conexions.proxy import Proxy
# ------------------------------------------------------------------------------

class TestProxy(unittest.TestCase):
    lig: str = 'https://icanhazip.com'
    ip_clara: str = requests.get(lig).text.rstrip()

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

# ------------------------------------------------------------------------------
