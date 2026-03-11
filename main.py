#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# + Authors:	Ran#
# + Created:	2026/03/11 13:00:00.000000
# + Revised:	2026/03/11 13:00:00.000000
# ------------------------------------------------------------------------------
from conexions import ProxyClient

# ------------------------------------------------------------------------------

URL = "https://icanhazip.com"

client = ProxyClient(max_connections=2, retries=3, timeout=15, verbose=True)

print(f"Real IP:  {client.get_ip()}")
print(f"Proxy:    {client.proxy.ip}:{client.proxy.port} ({client.proxy.country_name})")

response = client.get(URL)
print(f"Via proxy: {response.text.rstrip()}")
print(f"Connections — total: {client.total_connections}, proxied: {client.connection_count}")

# ------------------------------------------------------------------------------
