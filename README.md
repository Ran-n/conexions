[🌐 Galego](doc/README.gl.md)

[//]: # ( -*- coding: utf-8 -*- )
[//]: # ( ------------------------------------------------------------------------ )
[//]: # (+ Author: 	Ran# )
[//]: # (+ Created:	2021/06/30 13:06:09.000000 )
[//]: # (+ Revised:	2026/03/16 14:54:04.947887 )
[//]: # ( ------------------------------------------------------------------------ )

# Conexións
[![License](https://img.shields.io/github/license/Ran-n/conexions)](https://github.com/Ran-n/conexions/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12%20|%203.13-blue)](https://www.python.org/)
[![Issues](https://img.shields.io/github/issues/Ran-n/conexions)](https://github.com/Ran-n/conexions/issues)
[![Stars](https://img.shields.io/github/stars/Ran-n/conexions)](https://github.com/Ran-n/conexions/stargazers)

Unified web connection module with automatic proxy rotation. Scrapes elite proxies from [free-proxy-list.net](https://free-proxy-list.net/) and rotates through them automatically on failure.

## Installation

```bash
pip install conexions
```

or with uv:

```bash
uv add conexions
```

## Usage

### Basic

```python
from conexions import ProxyClient

client = ProxyClient()

print(client.get_ip())                               # real public IP
response = client.get("https://example.com")         # request via proxy
response = client.get_direct("https://example.com")  # direct (no proxy)
```

### Filtering proxies

All elite proxies are scraped. You can filter which ones get used by protocol and/or country:

```python
from conexions import ProxyClient, Protocol, Country, Anonymity

# HTTP-only proxies
client = ProxyClient(protocols=[Protocol.HTTP])

# Both HTTP and HTTPS
client = ProxyClient(protocols=[Protocol.HTTP, Protocol.HTTPS])

# SOCKS5 (requires a SOCKS-capable source — coming in a future release)
client = ProxyClient(protocols=[Protocol.SOCKS5])

# Only proxies from the US or Germany
client = ProxyClient(countries=[Country.US, Country.DE])

# Only elite proxies
client = ProxyClient(anonymities=[Anonymity.ELITE])

# Combined
client = ProxyClient(protocols=[Protocol.HTTPS], countries=[Country.US, Country.JP, Country.NL])
```

Available protocols: `Protocol.HTTP`, `Protocol.HTTPS`, `Protocol.SOCKS4`, `Protocol.SOCKS5`.

Note: `Protocol.HTTPS` proxies also support HTTP — requesting `Protocol.HTTP` will accept both HTTP and HTTPS proxies.

Country codes follow the ISO 3166-1 alpha-2 standard. Use the `Country` enum (e.g. `Country.US`, `Country.DE`, `Country.FR`).

Available anonymity levels: `Anonymity.ELITE` (website can't detect a proxy), `Anonymity.ANONYMOUS` (proxy detected, real IP hidden), `Anonymity.TRANSPARENT` (proxy detected, real IP exposed).

### Pool size

```python
print(client.proxy_count)        # proxies in the pool matching the current filter
print(client.proxy_count_total)  # total proxies in the pool regardless of filter
print(client.proxies)            # list of all proxies currently in the pool
```

### Sessions

```python
client.open_session()
response = client.get("https://example.com")
client.close_session()
```

### Proxy rotation

```python
client.rotate_proxy()    # manually rotate to the next proxy
client.refill_proxies()  # re-scrape the source to refill the pool
client.refresh_header()  # regenerate the User-Agent header
```

### Counters and timing

```python
client.total_connections        # total requests made (proxy + direct)
client.connection_count         # requests made through the current proxy
client.direct_connection_count  # requests made without a proxy
client.proxy_count              # proxies in the pool matching the current filter
client.proxy_count_total        # total proxies in the pool regardless of filter
client.last_elapsed             # seconds elapsed during the last request
```

### Active proxy

```python
proxy = client.proxy
print(proxy.ip)                    # e.g. "123.45.67.89"
print(proxy.port)                  # e.g. 8080
print(proxy.protocol)              # Protocol.HTTPS
print(proxy.country)               # Country.US
print(proxy.country.country_name)  # "United States of America"
print(proxy.anonymity)             # Anonymity.ELITE
print(proxy.google)                # False
print(proxy.last_checked)          # "1 minute ago"
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_connections` | `0` | Requests per proxy before rotating. `0` = unlimited |
| `retries` | `2` | Retry attempts on connection failure |
| `timeout` | `5` | Request timeout in seconds |
| `verbose` | `False` | Print status messages to stdout |
| `show_spinner` | `False` | Show a spinner during requests |
| `protocols` | `None` | Proxy protocols to accept: `Protocol.HTTP`, `Protocol.HTTPS`, `Protocol.SOCKS4`, `Protocol.SOCKS5`. `None` = no filter |
| `countries` | `None` | List of `Country` values to filter by. `None` = no filter |
| `anonymities` | `[Anonymity.ELITE]` | List of `Anonymity` values to filter by: `Anonymity.ELITE`, `Anonymity.ANONYMOUS`, `Anonymity.TRANSPARENT`. `None` = no filter |
| `google` | `None` | `True` = only Google-compatible proxies. `False` = only non-Google. `None` = no filter |

---

## [Donations 🙇🙇](https://github.com/Ran-n/doc/blob/main/doaz%C3%B3ns.md)

| | | Address |
|:---:|:---|:---|
| <img src="https://raw.githubusercontent.com/Ran-n/svgs/main/divisas/bitcoin/bitcoin_0.svg" width="20" alt="bitcoin logo" title="Bitcoin"> | **Bitcoin** | `bc1q79vja8jzr27dxaf3ylu7e49ady8zq0jsm5qfk6` |
| <img src="https://raw.githubusercontent.com/Ran-n/svgs/main/divisas/monero/monero_0.svg" width="20" alt="monero logo" title="Monero"> | **Monero** | `88Rezd6ZQzaCb1s7K1tRCiCaDzuHrfYsn4q348jJuePpLs84JNsWEghMAZZgzpDPrqD4PBxk7hwMkSdNQ4CLqFHyPVLdX1D` |
| <img src="https://raw.githubusercontent.com/Ran-n/svgs/main/divisas/wownero/wownero_0.svg" width="20" alt="wownero logo" title="Wownero"> | **Wownero** | `WW2RheTNrq8goAi42Dz5AKUj1qLSaTSSgiH7sHR2qRqojg238EXP3MM3xuUgswriET7UrpkEoYaCkecBhnU49oxM1dZyYoSmm` |

## [Changelog](./doc/changelog/index.md)
