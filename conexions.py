#! /usr/bin/python3
#+ coding: utf-8
#------------------------------------------------------------------------------------------------
#+ Autor:	Ran#
#+ Creado:	19/05/2021 13:44:12
#+ Editado:	30/06/2021 13:47:53
#------------------------------------------------------------------------------------------------
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
#from proxy_requests import ProxyRequests, ProxyRequestBasicAuth
import requests
import json
import secrets
from stem import Signal
from stem.control import Controller
#------------------------------------------------------------------------------------------------
class porProxie:
    # constructor
    def __init__(self, verbose=False, maxCons=10):
        self.__verbose = verbose # variable que di se queres prints
        self.__ligazon_sslproxies = 'https://www.sslproxies.org'
        self.__ua = UserAgent() # Para xerar un UserAgent aleatorio
        self.__proxie_list = self.__getProxies() # Lista con todolos proxies
        self.__proxie_list_gardada = self.__proxie_list.copy()
        self.__proxie = self.__getProxieAleatorio() # Colle un proxie
        self.__conexions = 0 # Número de conexións feitas cun proxie
        self.__maxConexions = 10 # Número máximo de conexións cun proxie

    ## GETTERS ##
    # devolve unha header aleatoria
    def getCabeceiraAleatoria(self):
        return {'User-Agent': self.__ua.random}

    # devolve a lista de proxies
    def getProxies(self):
        return self.__proxie_list
    
    # devolve o proxie usado actualmente
    def getProxie(self):
        return self.__proxie
    
    # devolve cantas conexións se levan feito
    def getNumConexions(self):
        return self.__conexions

    # devolve o máximo de conexións actual
    def getMaxConexions(self):
        return self.__maxConexions

    # Devolve un proxie da lista de forma aleatoria
    def __getProxieAleatorio(self, eliminar=True):
        # se o que mandan non é booleano levantar excepción
        if type(eliminar) != bool: raise Exception('A variable debe ser te tipo booleano')

        cant_proxies = len(self.__proxie_list)
        # se non ten proxies colle a lista de novo
        while cant_proxies == 0:
            self.setProxieList()
            cant_proxies = len(self.__proxie_list)

        # un número aleatorio de 0 a N
        indice = secrets.randbelow(cant_proxies)

        Tproxie = self.__proxie_list[indice]
        # eliminar o proxie da lista a menos que se poña false explicito
        if eliminar: del(self.__proxie_list[indice])

        Tproxie = Tproxie['ip']+':'+Tproxie['porto']
        if self.__verbose: print('* Usando  proxie "{}" *'.format(Tproxie))

        return {'https': Tproxie, 'http': Tproxie}

    ## GETTERS ##
        
    ## SETTERS ##
    # set automático da lista de proxies
    def setProxieList(self):
        try:
            self.__proxie_list = self.__getProxies()
            self.__proxie_list_gardada = self.__proxie_list.copy()
        except:
            # con isto soamente sacame o erro orixinal
            raise 
            if self.__verbose: print('* ERRO: función "setProxieList" do obxecto "porProxie" do ficheiro "conexions.py" *')
        finally:
            return True

    # set automático dun novo proxie
    def setNovoProxie(self):
        try:
            self.__proxie = self.__getProxieAleatorio()
            self.__setConexions(resetear=True)
        except:
            # con isto soamente sacame o erro orixinal
            raise
            if self.__verbose: print('* ERRO: función "setNovoProxie" do obxecto "porProxie" do ficheiro "conexions.py" *')
        finally:
            return True

    # set de conexions. Ou engade 1 ou resetea a 0
    def __setConexions(self, resetear=False):
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
            if self.__verbose: print('* ERRO: función "setConexions" do obxecto "porProxie" do ficheiro "conexions" *')
        finally:
            return True

    # establece o máximo de conexións por proxie
    def setMaxConexions(self, novoMaxConexions):
        try:
            self.__maxConexions = int(novoMaxConexions)
        except:
            # con isto soamente sacame o erro orixinal
            raise
            if self.__verbose: print('* ERRO: función "setMaxConexions" do obxecto "porProxie" do ficheiro "conexions" *')
        finally:
            return True

    # establece o valor de verbose. True mostrar prints False non mostralos
    def setVerbose(self, novoVerbose):
        try:
            self.__verbose = bool(novoVerbose)
        except:
            # con isto soamente sacame o erro orixinal
            raise
            if self.__verbose: print('* ERRO: función "setVerbose" do obxecto "porProxie" do ficheiro "conexions" *')
        finally:
            return True

    ## SETTERS ##

    # saca a lista de proxies da páxina web sslproxies.org
    def __getProxies(self):
        # request á páxina
        paxina_proxies = requests.get(url=self.__ligazon_sslproxies, headers=self.getCabeceiraAleatoria()) 

        # bloque para sacar o texto en utf-8
        if paxina_proxies.encoding.lower() != 'utf-8':
            paxina_proxies.encoding = 'utf-8'
        paxina_proxies = paxina_proxies.text

        # uso de bs4 para sacar a táboa
        soup = BeautifulSoup(paxina_proxies, 'html.parser')
        taboa_proxies = soup.find(id='proxylisttable')

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

        if self.__verbose: print('* Lista de táboas de sslproxies.org scrapeada *\n')
        return temp_proxies
    

    # get usando proxies
    def get(self, url, params=None, stream=False, timeout=30):
        # de usar o proxie o max de veces coller un novo
        if self.getNumConexions() >= self.getMaxConexions():
            try:
                self.setNovoProxie()
            except:
                # con isto soamente sacame o erro orixinal
                raise
                if self.__verbose: print('* ERRO: función "get" do obxecto "porProxie" do ficheiro "conexions" *')

        try:
            resposta = requests.get(url=url, params=params, proxies=self.getProxie(), stream=stream, timeout=timeout).text
            self.__setConexions()
        except:
            if self.__verbose: print('* Erro do proxie "{}" *\n'.format(self.getProxie()['https']))
            self.__setConexions(resetear=True)
            self.setNovoProxie()
            resposta = self.get(url=url, params=params, stream=stream, timeout=timeout)
        return resposta
    
    # get sen o uso de proxies
    def getEspido(self, url, params=None, stream=False, timeout=30):
        return requests.get(url=url, params=params, stream=stream, timeout=timeout).text

#------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    conn = porProxie(True)
    #print(conn.getCabeceiraAleatoria())
    #print(conn.getProxies())
    #print(conn.getEspido('https://icanhazip.com'))
    print(conn.get('https://icanhazip.com'))
    print(conn.getNumConexions())
    print(conn.get('https://icanhazip.com'))
    print(conn.getNumConexions())
#------------------------------------------------------------------------------------------------
