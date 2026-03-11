[🌐 English](../README.md)

[//]: # ( -*- coding: utf-8 -*- )
[//]: # ( ------------------------------------------------------------------------ )
[//]: # (+ Author: 	Ran# )
[//]: # (+ Created:	2022/02/26 13:27:57.000000 )
[//]: # (+ Revised:	2026/03/11 16:15:08.364777 )
[//]: # ( ------------------------------------------------------------------------ )

# Conexións
[![License](https://img.shields.io/github/license/Ran-n/conexions)](https://github.com/Ran-n/conexions/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12%20|%203.13-blue)](https://www.python.org/)
[![Issues](https://img.shields.io/github/issues/Ran-n/conexions)](https://github.com/Ran-n/conexions/issues)
[![Stars](https://img.shields.io/github/stars/Ran-n/conexions)](https://github.com/Ran-n/conexions/stargazers)

Módulo de conexións con rotación automática de proxies. Extrae proxies HTTPS de elite de [free-proxy-list.net](https://free-proxy-list.net/) e rótalos automaticamente.

## Instalación

```bash
pip install conexions
```

ou con uv:

```bash
uv add conexions
```

## Uso

```python
from conexions import ProxyClient

client = ProxyClient(max_connections=5, retries=3, timeout=15, verbose=True)

print(client.get_ip())                               # IP pública real
response = client.get("https://example.com")         # petición vía proxy
response = client.get_direct("https://example.com")  # petición directa
```

## Parámetros

| Parámetro | Por defecto | Descrición |
|-----------|-------------|------------|
| `max_connections` | `0` | Peticións por proxy antes de rotar. `0` = sen límite |
| `retries` | `5` | Intentos en caso de fallo |
| `timeout` | `30` | Tempo de espera en segundos |
| `verbose` | `False` | Mostrar mensaxes de estado |
| `show_spinner` | `False` | Mostrar spinner durante as peticións |

---

## [Doazóns 🙇🙇](https://github.com/Ran-n/doc/blob/main/doaz%C3%B3ns.md)

**Bitcoin** <img src="https://raw.githubusercontent.com/Ran-n/svgs/main/divisas/bitcoin/bitcoin_0.svg" width="20" alt="bitcoin logo" title="Bitcoin">
bc1q79vja8jzr27dxaf3ylu7e49ady8zq0jsm5qfk6

**Monero** <img src="https://raw.githubusercontent.com/Ran-n/svgs/main/divisas/monero/monero_0.svg" width="20" alt="monero logo" title="Monero">
88Rezd6ZQzaCb1s7K1tRCiCaDzuHrfYsn4q348jJuePpLs84JNsWEghMAZZgzpDPrqD4PBxk7hwMkSdNQ4CLqFHyPVLdX1D

**Wownero** <img src="https://raw.githubusercontent.com/Ran-n/svgs/main/divisas/wownero/wownero_0.svg" width="20" alt="wownero logo" title="Wownero">
WW2RheTNrq8goAi42Dz5AKUj1qLSaTSSgiH7sHR2qRqojg238EXP3MM3xuUgswriET7UrpkEoYaCkecBhnU49oxM1dZyYoSmm

## TODO — [actual](./TODO/current.gl.md) · [completo](./TODO/full.gl.md)
