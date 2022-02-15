#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/02/13 16:43:37.259437
#+ Editado:	2022/02/15 21:07:29.323023
# ------------------------------------------------------------------------------
import requests
from requests.models import Response
from typing import List, Union
#import secrets
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

#from .dto_proxy import ProxyDTO
from dto_proxy import ProxyDTO
#from .excepcions import CambioNaPaxinaErro
from excepcions import CambioNaPaxinaErro
# ------------------------------------------------------------------------------
class Proxy:
    __ligazon: str = 'https://sslproxies.org'
    __verbose: bool = False
    __max_cons: int = 0             # ó ser 0 implica que non ten un máximo predefinido
    # xFCR: xuntar as cant_cons nunha soa variable
    __cant_cons: int = 0
    __cant_cons_espido: int = 0
    __timeout: int = 30
    __cabeceira: dict[str, str]
    __lst_proxys: List[ProxyDTO]    # Ordeados de máis velho[0] a máis novo[len()]
    __proxy: ProxyDTO

    __ligazons_ip: List[str] = [
            'https://ip.me',
            'https://icanhazip.com'
            ]

    def __init__(self, verbose=False, max_cons=0, timeout= 30) -> None:
        self.__verbose = verbose
        self.__max_cons = max_cons
        self.__timeout = timeout
        self.__lst_proxys  = []

        self.set_cabeceira()    # Dalle valor a __cabeceira
        self.set_proxys()       # Enche a __lst_proxys
        self.set_proxy()        # Saca un proxy da lista e meteo como atributo

    # Getters
    def get_ligazon(self) -> str:
        return self.__ligazon

    def get_verbose(self) -> bool:
        return self.__verbose

    def get_max_cons(self) -> int:
        return self.__max_cons

    def get_cant_cons(self) -> int:
        return self.__cant_cons

    def get_cant_cons_espido(self) -> int:
        return self.__cant_cons_espido

    def get_timeout(self) -> int:
        return self.__timeout

    def get_cabeceira(self, set_nova: Union[bool, int] = False) -> dict[str, str]:
        try:
            return self.__cabeceira
        finally:
            if set_nova:
                self.set_cabeceira()

    def get_proxys(self) -> List[ProxyDTO]:
        return self.__lst_proxys

    def get_proxy(self) -> ProxyDTO:
        return self.__proxy

    def get_ligazons_ip(self) -> List[str]:
        return self.__ligazons_ip

    # Getters #

    # Setters
    def __set_ligazon(self, nova_ligazon: str) -> None:
        self.__ligazon = nova_ligazon

    def set_verbose(self, novo_verbose: bool) -> None:
        self.__verbose = novo_verbose

    def set_max_cons(self, novo_max_cons: int) -> None:
        self.__max_cons = novo_max_cons

    def __set_cant_cons(self, novo_cant_cons: int) -> None:
        self.__cant_cons = novo_cant_cons

    def __set_cant_cons_espido(self, novo_cant_cons_espido: int) -> None:
        self.__cant_cons_espido = novo_cant_cons_espido

    def set_timeout(self, novo_timeout: int) -> None:
        self.__timeout = novo_timeout

    def set_cabeceira(self) -> None:
        self.__cabeceira = {'User-Agent': UserAgent().random}

    def set_proxys(self) -> None:
        """
        Colle a páxina e saca toda a info sobre os proxys que contén.

        @entradas:
            Ningunha.

        @saidas:
            Ningunha.
        """

        while True:
            try:
                pax_web = requests.get(url= self.get_ligazon(),
                                        headers= self.get_cabeceira())
            except ConnectionError:
                pass
            except Exception:
                raise
            else:
                # se saiu todo ben sáese do bucle
                if pax_web.ok:
                    pax_web.encoding = 'utf-8'
                    break

        taboa_proxys = bs(pax_web.text, 'html.parser').find(class_='table')

        lst_nomes_cols_esperados = [
                'IP Address',
                'Port',
                'Code',
                'Country',
                'Anonymity',
                'Google',
                'Https',
                'Last Checked'
        ]
        lst_nomes_cols_obtidos = taboa_proxys.thead.find_all('th')

        if len(lst_nomes_cols_esperados) != len(lst_nomes_cols_obtidos):
            raise CambioNaPaxinaErro('Modificado o número de columnas')

        for esperado, obtido in zip(lst_nomes_cols_esperados, lst_nomes_cols_obtidos):
            if esperado != obtido.text:
                raise CambioNaPaxinaErro('Modificado o orde ou nome das columnas')

        for fila in taboa_proxys.tbody:
            # métoos desta forma na lista porque así vou sacando e eliminando dende atrás
            self.__lst_proxys.insert(0, ProxyDTO([atributo.text for atributo in fila.find_all('td')]))

    def set_proxy(self) -> None:
        """
        Devolve un proxy e automáticamente eliminao da lista.
        De non ter ningún proxy que devolver, escraperá a páxina
        por máis.

        @entradas:
            Ningunha.

        @saídas:
            ProxyDTO    -   Sempre
            └ O proxy a usar nas conexións.
        """

        try:
            self.__proxy = self.get_proxys().pop()
        # se a lista de proxys está baleira
        except IndexError:
            self.set_proxys()
            self.get_proxy()    # selfcall
        finally:
            self.__set_cant_cons(0)

    # Setters #

    def aumentar_cant_cons(self) -> None:
        self.__set_cant_cons(self.get_cant_cons()+1)

    def aumentar_cant_cons_espido(self) -> None:
        self.__set_cant_cons_espido(self.get_cant_cons_espido()+1)

    def get(self, ligazon: str, params: dict = None, bolachas: dict = None,
            stream: dict = False, timeout: int = 0) -> Response:

        # lazy_check_types

        #self.

        if timeout != self.get_timeout():
            timeout = self.get_timeout()

        return requests.get(url= ligazon, params= params, proxies= self.get_proxy(),
                headers= self.get_cabeceira(set_nova=True), cookies= bolachas,
                stream= stream, timeout= timeout)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    p = Proxy()
# ------------------------------------------------------------------------------
