#! /usr/bin/python3
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------
#+ Autor:	Ran#
#+ Creado:	19/05/2021 13:44:12
#+ Editado:	2022/02/12 19:44:05.712905
#------------------------------------------------------------------------------------------------
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
#from proxy_requests import ProxyRequests, ProxyRequestBasicAuth
import requests
import json
import secrets
from stem import Signal
from stem.control import Controller
from halo import Halo
#------------------------------------------------------------------------------------------------
class Proxy:
    # constructor
    def __init__(self, verbose=False, max_cons=20):
        self.__verbose = verbose                                    # variable que di se queres prints
        self.__ligazon_sslproxies = 'https://www.sslproxies.org'
        self.__sesion = None                                        # se se crea unha session de requests
        self.__proxy_list = self.__get_proxies()                    # Lista con todolos proxies
        self.__proxy_list_gardada = self.__proxy_list.copy()
        self.__proxy = self.__get_proxie_aleatorio()                # Colle un proxie
        self.__conexions = 0                                        # Número de conexións feitas cun proxie
        self.__conexions_espido = 0                                 # Número de conexións feitas sen proxie
        self.__max_conexions = max_cons                              # Número máximo de conexións cun proxie

    ## GETTERS ##

    # Devolve un proxie da lista de forma aleatoria
    def __get_proxie_aleatorio(self, eliminar=True):
        # xFCR uteis
        # se o que mandan non é booleano levantar excepción
        if type(eliminar) != bool: raise Exception('A variable debe ser te tipo booleano')

        cant_proxies = len(self.__proxy_list)
        # se non ten proxies colle a lista de novo
        while cant_proxies == 0:
            self.set_proxie_list()
            cant_proxies = len(self.__proxy_list)

        # un número aleatorio de 0 a N
        indice = secrets.randbelow(cant_proxies)

        Tproxie = self.__proxy_list[indice]
        # eliminar o proxie da lista a menos que se poña false explicito
        if eliminar: del(self.__proxy_list[indice])

        Tproxie = Tproxie['ip']+':'+Tproxie['porto']
        return {'http': 'http://'+Tproxie, 'https': 'http://'+Tproxie}

    # devolve o valor de verbose
    def __get_verbose(self):
        return self.__verbose

    # devolve o obxecto session de requests
    def get_sesion(self):
        return self.__sesion

    # devolve unha header aleatoria
    def get_cabeceira_aleatoria(self):
        return {'User-Agent': UserAgent().random}

    # devolve a lista de proxies
    def get_proxies(self):
        return self.__proxy_list

    # devolve o proxie usado actualmente
    def get_proxy(self):
        return self.__proxy

    # devolve cantas conexións se levan feito
    def get_num_conexions(self):
        return self.__conexions

    # devolve cantas conexións se levan feito espidas
    def get_num_conexionsEspido(self):
        return self.__conexions_espido

    # devolve o máximo de conexións actual
    def get_max_conexions(self):
        return self.__max_conexions

    ## GETTERS ##

    ## SETTERS ##

    # set de conexions. Ou engade 1 ou resetea a 0
    def __set_conexions(self, resetear=False):
        # mira se o metido é booleano, se non manda excepción
        if type(resetear) != bool: raise Exception('A variable debe ser te tipo booleano')
        try:
            # este if da erro non sei por que
            #self.__conexions = 0 if resetear else self.__conexions += 1
            if resetear:
                self.__conexions = 0
            else:
                self.__conexions += 1
        except:
            # con isto soamente sacame o erro orixinal
            raise
            if self.__get_verbose(): print('* ERRO: función "__set_conexions" do obxecto "Proxy" do ficheiro "conexions" *')
            return False
        finally:
            return True

    # set de aumento en +1 do número de conexións feitas espido
    def __set_conexions_espido(self):
        try:
            self.__conexions_espido += 1
        except:
            # con isto soamente sacame o erro orixinal
            raise
            if self.__get_verbose(): print('* ERRO: función "__set_conexions_espido" do obxecto "Proxy" do ficheiro "conexions" *')
            return False
        finally:
            return True

    # crea o obxecto session de requests
    def __set_sesion(self, resetear=False):
        try:
            if resetear:
                self.__sesion = None
            else:
                self.__sesion = requests.Session()
        except:
            # con isto soamente sacame o erro orixinal
            raise
            if self.__get_verbose(): print('* ERRO: función "__set_sesion" do obxecto "Proxy" do ficheiro "conexions" *')
            return False
        finally:
            return True

    # set automático da lista de proxies
    def set_proxie_list(self):
        try:
            self.__proxy_list = self.__get_proxies()
            self.__proxy_list_gardada = self.__proxy_list.copy()
        except:
            # con isto soamente sacame o erro orixinal
            raise
            if self.__get_verbose(): print('* ERRO: función "set_proxie_list" do obxecto "Proxy" do ficheiro "conexions.py" *')
            return False
        finally:
            return True

    # set automático dun novo proxie
    def set_novo_proxy(self):
        try:
            self.__proxy = self.__get_proxie_aleatorio()
            self.__set_conexions(resetear=True)
        except:
            # con isto soamente sacame o erro orixinal
            raise
            if self.__get_verbose(): print('* ERRO: función "set_novo_proxy" do obxecto "Proxy" do ficheiro "conexions.py" *')
            return False
        finally:
            return True

    # establece o máximo de conexións por proxie
    def set_max_conexions(self, novoMaxConexions):
        try:
            self.__max_conexions = int(novoMaxConexions)
        except:
            # con isto soamente sacame o erro orixinal
            raise
            if self.__get_verbose(): print('* ERRO: función "set_max_conexions" do obxecto "Proxy" do ficheiro "conexions" *')
            return False
        finally:
            return True

    # establece o valor de verbose. True mostrar prints False non mostralos
    def set_verbose(self, novoVerbose):
        # está ben así porque se non me mandan o novoVerbose saca TypeError de que lle falta unha variable
        # se o que mandan non é booleano levantar excepción
        if type(novoVerbose) != bool: raise Exception('A variable debe ser te tipo booleano')

        try:
            self.__verbose = novoVerbose
        except:
            # con isto soamente sacame o erro orixinal
            raise
            if self.__get_verbose(): print('* ERRO: función "set_verbose" do obxecto "Proxy" do ficheiro "conexions" *')
            return False
        finally:
            return True

    ## SETTERS ##

    # saca a lista de proxies da páxina web sslproxies.org
    def __get_proxies(self):
        # request á páxina
        paxina_proxies = requests.get(url=self.__ligazon_sslproxies, headers=self.get_cabeceira_aleatoria())

        # bloque para sacar o texto en utf-8
        if paxina_proxies.encoding.lower() != 'utf-8':
            paxina_proxies.encoding = 'utf-8'
        paxina_proxies = paxina_proxies.text

        # uso de bs4 para sacar a táboa
        soup = BeautifulSoup(paxina_proxies, 'html.parser')
        #taboa_proxies = soup.find(id='proxylisttable')  #Vello nome
        #taboa_proxies = soup.find(class_='table table-striped table-bordered')  #Nova opción con class
        taboa_proxies = soup.find(id='list')  #Nova opción con id

        # ir buscando na táboa as columnas e gardalas na lista de dicionarios
        temp_proxies = []
        for fila in taboa_proxies.tbody.find_all('tr'):
            temp_proxies.append({
                'ip': fila.find_all('td')[0].string,
                'porto': fila.find_all('td')[1].string,
                'codigo estado': fila.find_all('td')[2].string,
                'nome estado': fila.find_all('td')[3].string,
                'tipo': fila.find_all('td')[4].string,
                'google': fila.find_all('td')[5].string,
                'https': fila.find_all('td')[6].string,
                'dende': fila.find_all('td')[7].string
                })

        # buscamos os proxies da lista que non cumplan as espectativas e eliminamolos
        for indice, Bproxie in enumerate(temp_proxies):
            if (Bproxie['tipo'] != 'elite proxy') & (Bproxie['google'] != 'no') & (Bproxie['https'] != 'yes'):
                del temp_proxies[indice]

        if self.__get_verbose(): print('* Lista de táboas de sslproxies.org scrapeada *\n')
        return temp_proxies

    # forma de crear unha session como en requests
    def sesion(self):
        try:
            self.__set_sesion()
        except:
            # con isto soamente sacame o erro orixinal
            raise
            if self.__get_verbose(): print('* ERRO: función "sesion" do obxecto "Proxy" do ficheiro "conexions" *')
            return False
        finally:
            if self.__get_verbose(): print('* Iniciando unha sesión *')
            return True

    # fai que se elimine a sesión actual
    def sesion_fin(self):
        try:
            #self.__set_sesion(resetar=True)
            self.__sesion = None
        except:
            # con isto soamente sacame o erro orixinal
            raise
            if self.__get_verbose(): print('* ERRO: función "sesion" do obxecto "Proxy" do ficheiro "conexions" *')
            return False
        finally:
            if self.__get_verbose(): print('* Rematando a sesión *')
            return True

    # get usando proxies
    @Halo(text='Conectando', spinner='dots')
    def get(self, url, params=None, bolacha=None, stream=False, timeout=30):
        # de usar o proxie o max de veces coller un novo
        if self.get_num_conexions() >= self.get_max_conexions():
            try:
                self.set_novo_proxy()
            except:
                # con isto soamente sacame o erro orixinal
                raise
                if self.__get_verbose(): print('* ERRO: función "get" do obxecto "Proxy" do ficheiro "conexions" *')
                return False

        try:
            if self.__get_verbose(): print('* Usando  proxie "{}" *'.format(self.get_proxy()['https']))
            # de ter creada unha sesión usala para facer o get
            if (self.get_sesion()):
                resposta = self.get_sesion().get(url=url, params=params, proxies=self.get_proxy(),
                                                headers=self.get_cabeceira_aleatoria(), cookies=bolacha,
                                                stream=stream, timeout=timeout)
            else:
                resposta = requests.get(url=url, params=params, proxies=self.get_proxy(),
                                        headers=self.get_cabeceira_aleatoria(), cookies=bolacha,
                                        stream=stream, timeout=timeout)
            self.__set_conexions()
        except:
            if self.__get_verbose(): print('* Erro do proxie "{}" *\n'.format(self.get_proxy()['https']))
            self.__set_conexions(resetear=True)
            self.set_novo_proxy()
            resposta = self.get(url=url, bolacha=bolacha, params=params, stream=stream, timeout=timeout)
        return resposta

    # get sen o uso de proxies
    @Halo(text='Conectando', spinner='dots')
    def get_espido(self, url, params=None, bolacha=None, cabeceira=None, stream=False, timeout=30):
        try:
            # de ter creada unha sesión usala para facer o get
            if (self.get_sesion()):
                return self.get_sesion().get(url=url, params=params, headers=cabeceira, cookies=bolacha, stream=stream, timeout=timeout)
            else:
                return requests.get(url=url, params=params, headers=cabeceira, cookies=bolacha, stream=stream, timeout=timeout)
        except:
            # con isto soamente sacame o erro orixinal
            raise
            if self.__get_verbose(): print('* ERRO: función "get_espido" do obxecto "Proxy" do ficheiro "conexions" *')
        finally:
            if self.__get_verbose(): print('* CONEXIÓN SEN PROXY *')
            # aumentamos o num de conexs sen proxie
            self.__set_conexions_espido()

    def get_ip(self, tipo='proxy', params=None, bolacha=None, cabeceira=None, stream=False, timeout=30):
        lig = 'https://icanhazip.com'

        if tipo == 'proxy':
            return self.get(lig)
        else:
            return self.get_espido(lig)

#------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    ligazon_get_ip = 'https://icanhazip.com'

    print('> TEST\n')
    conn = Proxy(False)
    #print(conn.get_cabeceira_aleatoria())
    #print(conn.get_proxies())

    print('> IP espida usada {} vez {}\n'.format(conn.get_espido(ligazon_get_ip).text.rstrip(), conn.get_num_conexionsEspido()))

    print('> IP proxie usada {} vez {}\n'.format(conn.get(ligazon_get_ip).text.rstrip(), conn.get_num_conexions()))
    print('> IP proxie usada {} vez {}\n'.format(conn.get(ligazon_get_ip).text.rstrip(), conn.get_num_conexions()))

    print('> Sesión actual = {}'.format(conn.get_sesion()))
    print('> Inicio de sesión')
    conn.sesion()
    print('> Sesión actual = {}\n'.format(conn.get_sesion()))
    print('> IP proxie usada {} vez {}\n'.format(conn.get(ligazon_get_ip).text.rstrip(), conn.get_num_conexions()))
    print('> IP proxie usada {} vez {}\n'.format(conn.get(ligazon_get_ip).text.rstrip(), conn.get_num_conexions()))
    conn.sesion_fin()
    print('> Fin de sesión')
    print('> Sesión actual = {}\n'.format(conn.get_sesion()))

    print('> IP proxie usada {} vez {}\n'.format(conn.get(ligazon_get_ip).text.rstrip(), conn.get_num_conexions()))

    print('> IP espida usada {} vez {}\n'.format(conn.get_espido(ligazon_get_ip).text.rstrip(), conn.get_num_conexionsEspido()))

#------------------------------------------------------------------------------------------------
