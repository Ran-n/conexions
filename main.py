#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# + Authors:	Ran#
# + Created:	2026/03/11 13:00:00.000000
# + Revised:	2026/03/16 15:35:19.726548
# ------------------------------------------------------------------------------
from conexions import ProxyClient

# ------------------------------------------------------------------------------

URL = "https://icanhazip.com"

client = ProxyClient()

print(f"Real IP:  {client.get_ip()}")
print(
    f"Proxy:    {client.proxy.ip}:{client.proxy.port} ({client.proxy.country}, {client.proxy.anonymity})"
)

response = client.get(URL)
print(f"Via proxy: {response.text.rstrip()}")
print(
    f"Connections — total: {client.total_connections}, proxied: {client.connection_count}"
)

# ------------------------------------------------------------------------------
