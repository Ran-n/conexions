[🌐 English](../README.md)

[//]: # ( -*- coding: utf-8 -*- )
[//]: # ( ------------------------------------------------------------------------ )
[//]: # (+ Author: 	Ran# )
[//]: # (+ Created:	2022/02/26 13:27:57.000000 )
[//]: # (+ Revised:	2026/03/16 14:54:04.947887 )
[//]: # ( ------------------------------------------------------------------------ )

# Conexións
[![License](https://img.shields.io/github/license/Ran-n/conexions)](https://github.com/Ran-n/conexions/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12%20|%203.13-blue)](https://www.python.org/)
[![Issues](https://img.shields.io/github/issues/Ran-n/conexions)](https://github.com/Ran-n/conexions/issues)
[![Stars](https://img.shields.io/github/stars/Ran-n/conexions)](https://github.com/Ran-n/conexions/stargazers)

Módulo de conexións con rotación automática de proxies. Extrae proxies de elite de [free-proxy-list.net](https://free-proxy-list.net/) e rota automaticamente en caso de fallo.

## Instalación

```bash
pip install conexions
```

ou con uv:

```bash
uv add conexions
```

## Uso

### Básico

```python
from conexions import ProxyClient

client = ProxyClient()

print(client.get_ip())                               # IP pública real
response = client.get("https://example.com")         # petición vía proxy
response = client.get_direct("https://example.com")  # petición directa (sen proxy)
```

### Filtrado de proxies

Extráense todos os proxies de elite. Podes filtrar cales se usan por protocolo e/ou país:

```python
from conexions import ProxyClient, Protocol, Country, Anonymity

# Só proxies HTTP
client = ProxyClient(protocols=[Protocol.HTTP])

# HTTP e HTTPS
client = ProxyClient(protocols=[Protocol.HTTP, Protocol.HTTPS])

# SOCKS5 (require unha fonte compatible — dispoñible nunha versión futura)
client = ProxyClient(protocols=[Protocol.SOCKS5])

# Só proxies de EE.UU. ou Alemaña
client = ProxyClient(countries=[Country.US, Country.DE])

# Só proxies de elite
client = ProxyClient(anonymities=[Anonymity.ELITE])

# Combinado
client = ProxyClient(protocols=[Protocol.HTTPS], countries=[Country.US, Country.JP, Country.NL])
```

Protocolos dispoñibles: `Protocol.HTTP`, `Protocol.HTTPS`, `Protocol.SOCKS4`, `Protocol.SOCKS5`.

Nota: os proxies `Protocol.HTTPS` tamén soportan HTTP — solicitar `Protocol.HTTP` aceptará proxies HTTP e HTTPS.

Os códigos de país seguen o estándar ISO 3166-1 alpha-2. Usa o enum `Country` (p.ex. `Country.US`, `Country.DE`, `Country.FR`).

Niveis de anonimato dispoñibles: `Anonymity.ELITE` (o sitio non detecta proxy), `Anonymity.ANONYMOUS` (proxy detectado, IP real oculta), `Anonymity.TRANSPARENT` (proxy detectado, IP real exposta).

### Tamaño do pool

```python
print(client.proxy_count)        # proxies do pool que coinciden co filtro actual
print(client.proxy_count_total)  # total de proxies no pool independentemente do filtro
print(client.proxies)            # lista de todos os proxies no pool
```

### Sesións

```python
client.open_session()
response = client.get("https://example.com")
client.close_session()
```

### Rotación de proxies

```python
client.rotate_proxy()    # rotar manualmente ao seguinte proxy
client.refill_proxies()  # volver raspar a fonte para encher o pool
client.refresh_header()  # rexenerar a cabeceira User-Agent
```

### Contadores e temporización

```python
client.total_connections        # total de peticións feitas (proxy + directas)
client.connection_count         # peticións feitas co proxy actual
client.direct_connection_count  # peticións feitas sen proxy
client.proxy_count              # proxies do pool que coinciden co filtro actual
client.proxy_count_total        # total de proxies no pool independentemente do filtro
client.last_elapsed             # segundos transcorridos na última petición
```

### Proxy activo

```python
proxy = client.proxy
print(proxy.ip)                    # p.ex. "123.45.67.89"
print(proxy.port)                  # p.ex. 8080
print(proxy.protocol)              # Protocol.HTTPS
print(proxy.country)               # Country.US
print(proxy.country.country_name)  # "United States of America"
print(proxy.anonymity)             # Anonymity.ELITE
print(proxy.google)                # False
print(proxy.last_checked)          # "1 minute ago"
```

## Parámetros

| Parámetro | Por defecto | Descrición |
|-----------|-------------|------------|
| `max_connections` | `0` | Peticións por proxy antes de rotar. `0` = sen límite |
| `retries` | `2` | Intentos en caso de fallo |
| `timeout` | `5` | Tempo de espera en segundos |
| `verbose` | `False` | Mostrar mensaxes de estado |
| `show_spinner` | `False` | Mostrar spinner durante as peticións |
| `protocols` | `None` | Protocolos a aceptar: `Protocol.HTTP`, `Protocol.HTTPS`, `Protocol.SOCKS4`, `Protocol.SOCKS5`. `None` = sen filtro |
| `countries` | `None` | Lista de valores `Country`. `None` = sen filtro |
| `anonymities` | `[Anonymity.ELITE]` | Lista de valores `Anonymity`: `Anonymity.ELITE`, `Anonymity.ANONYMOUS`, `Anonymity.TRANSPARENT`. `None` = sen filtro |
| `google` | `None` | `True` = só proxies compatibles con Google. `False` = só non compatibles. `None` = sen filtro |

---

## [Doazóns 🙇🙇](https://github.com/Ran-n/doc/blob/main/doaz%C3%B3ns.md)

| | | Enderezo |
|:---:|:---|:---|
| <img src="https://raw.githubusercontent.com/Ran-n/svgs/main/divisas/bitcoin/bitcoin_0.svg" width="20" alt="bitcoin logo" title="Bitcoin"> | **Bitcoin** | `bc1q79vja8jzr27dxaf3ylu7e49ady8zq0jsm5qfk6` |
| <img src="https://raw.githubusercontent.com/Ran-n/svgs/main/divisas/monero/monero_0.svg" width="20" alt="monero logo" title="Monero"> | **Monero** | `88Rezd6ZQzaCb1s7K1tRCiCaDzuHrfYsn4q348jJuePpLs84JNsWEghMAZZgzpDPrqD4PBxk7hwMkSdNQ4CLqFHyPVLdX1D` |
| <img src="https://raw.githubusercontent.com/Ran-n/svgs/main/divisas/wownero/wownero_0.svg" width="20" alt="wownero logo" title="Wownero"> | **Wownero** | `WW2RheTNrq8goAi42Dz5AKUj1qLSaTSSgiH7sHR2qRqojg238EXP3MM3xuUgswriET7UrpkEoYaCkecBhnU49oxM1dZyYoSmm` |

## [Changelog](./changelog/index.gl.md)
