#! /usr/bin/env python3
# ------------------------------------------------------------------------------
# + Authors:	Ran#
# + Created:	2026/03/11 13:00:00.000000
# + Revised:	2026/03/16 18:57:44.102938
# ------------------------------------------------------------------------------
from conexions import Anonymity, ProxyClient

# ------------------------------------------------------------------------------

URL = "https://icanhazip.com"

client = ProxyClient(
    max_connections=0,
    retries=2,
    timeout=5,
    verbose=False,
    show_spinner=False,
    protocols=None,
    countries=None,
    anonymities=[Anonymity.ELITE],
    google=None,
)

print(f"Real IP:  {client.get_ip()}")

response = client.get(URL)
print(f"Proxy:    {client.proxy}")
print(f"Via proxy: {response.text.rstrip()}")
print(f"Connections — total: {client.total_connections}, proxied: {client.connection_count}")

# ------------------------------------------------------------------------------
