[🌐 Galego](doc/README.gl.md)

[//]: # ( -*- coding: utf-8 -*- )
[//]: # ( ------------------------------------------------------------------------ )
[//]: # (+ Author: 	Ran# )
[//]: # (+ Created:	2021/06/30 13:06:09.000000 )
[//]: # (+ Revised:	2026/03/11 16:37:35.396023 )
[//]: # ( ------------------------------------------------------------------------ )

# Conexións
[![License](https://img.shields.io/github/license/Ran-n/conexions)](https://github.com/Ran-n/conexions/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12%20|%203.13-blue)](https://www.python.org/)
[![Issues](https://img.shields.io/github/issues/Ran-n/conexions)](https://github.com/Ran-n/conexions/issues)
[![Stars](https://img.shields.io/github/stars/Ran-n/conexions)](https://github.com/Ran-n/conexions/stargazers)

Unified web connection module with automatic proxy rotation. Scrapes elite HTTPS proxies from [free-proxy-list.net](https://free-proxy-list.net/) and rotates them automatically.

## Installation

```bash
pip install conexions
```

or with uv:

```bash
uv add conexions
```

## Usage

```python
from conexions import ProxyClient

client = ProxyClient(max_connections=5, retries=3, timeout=15, verbose=True)

print(client.get_ip())                               # real public IP
response = client.get("https://example.com")         # request via proxy
response = client.get_direct("https://example.com")  # direct request
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_connections` | `0` | Requests per proxy before rotating. `0` = unlimited |
| `retries` | `5` | Retry attempts on connection failure |
| `timeout` | `30` | Request timeout in seconds |
| `verbose` | `False` | Print status messages to stdout |
| `show_spinner` | `False` | Show a spinner during requests |

---

## [Donations 🙇🙇](https://github.com/Ran-n/doc/blob/main/doaz%C3%B3ns.md)

**Bitcoin** <img src="https://raw.githubusercontent.com/Ran-n/svgs/main/divisas/bitcoin/bitcoin_0.svg" width="20" alt="bitcoin logo" title="Bitcoin">
bc1q79vja8jzr27dxaf3ylu7e49ady8zq0jsm5qfk6

**Monero** <img src="https://raw.githubusercontent.com/Ran-n/svgs/main/divisas/monero/monero_0.svg" width="20" alt="monero logo" title="Monero">
88Rezd6ZQzaCb1s7K1tRCiCaDzuHrfYsn4q348jJuePpLs84JNsWEghMAZZgzpDPrqD4PBxk7hwMkSdNQ4CLqFHyPVLdX1D

**Wownero** <img src="https://raw.githubusercontent.com/Ran-n/svgs/main/divisas/wownero/wownero_0.svg" width="20" alt="wownero logo" title="Wownero">
WW2RheTNrq8goAi42Dz5AKUj1qLSaTSSgiH7sHR2qRqojg238EXP3MM3xuUgswriET7UrpkEoYaCkecBhnU49oxM1dZyYoSmm

## [Changelog](./doc/changelog/index.md)