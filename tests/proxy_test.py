#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/02/12 19:50:16.098183
#+ Editado:	2022/02/12 20:52:22.652884
# ------------------------------------------------------------------------------
import unittest

from src.conexions.proxy import Proxy
# ------------------------------------------------------------------------------

class TestProxy(unittest.TestCase):
    def test_primoxenio(self):
        ligazon_get_ip = 'https://icanhazip.com'
        conn = Proxy(False)

        # espido 1º
        self.assertEqual(conn.get_espido(ligazon_get_ip).text.rstrip(), conn.get_ip(tipo='espido').text.rstrip())
        self.assertEqual(conn.get_num_conexionsEspido(), 2)

        # proxy 1º
        self.assertEqual(conn.get(ligazon_get_ip).text.rstrip(), conn.get_ip(tipo='proxy').text.rstrip())
        self.assertEqual(conn.get_num_conexions(), 2)
        # proxy 2º
        self.assertEqual(conn.get(ligazon_get_ip).text.rstrip(), conn.get_ip(tipo='proxy').text.rstrip())
        self.assertEqual(conn.get_num_conexions(), 4)

        # espido 2º
        self.assertEqual(conn.get_espido(ligazon_get_ip).text.rstrip(), conn.get_ip(tipo='espido').text.rstrip())
        self.assertEqual(conn.get_num_conexionsEspido(), 4)

        self.assertEqual(conn.get_sesion(), None)
        conn.sesion()
        self.assertEqual(conn.get_sesion(), None)

        self.assertEqual(conn.get(ligazon_get_ip).text.rstrip(), conn.get_ip(tipo='proxy').text.rstrip())
        self.assertEqual(conn.get_num_conexions(), 3)
        """
        print('> IP proxie usada {} vez {}\n'.format(), ))
        print('> IP proxie usada {} vez {}\n'.format(conn.get(ligazon_get_ip).text.rstrip(), conn.get_num_conexions()))
        conn.sesion_fin()
        print('> Fin de sesión')
        print('> Sesión actual = {}\n'.format(conn.get_sesion()))

        print('> IP proxie usada {} vez {}\n'.format(conn.get(ligazon_get_ip).text.rstrip(), conn.get_num_conexions()))

        print('> IP espida usada {} vez {}\n'.format(conn.get_espido(ligazon_get_ip).text.rstrip(), conn.get_num_conexionsEspido()))
        """
# ------------------------------------------------------------------------------
