#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# + Authors:	Ran#
# + Created:	2026/03/11 07:55:18.174519
# + Revised:	2026/03/11 10:15:00.000000
# ------------------------------------------------------------------------------
import pytest

from conexions.proxy import Proxy

# ------------------------------------------------------------------------------

SAMPLE: list[str] = [
    "192.168.1.1",
    "8080",
    "US",
    "United States",
    "elite proxy",
    "no",
    "yes",
    "1 minute ago",
]

# ------------------------------------------------------------------------------


@pytest.fixture
def dto() -> Proxy:
    return Proxy.from_list(SAMPLE)


# ------------------------------------------------------------------------------


def test_from_list_fields(dto) -> None:
    assert dto.ip == "192.168.1.1"
    assert dto.port == "8080"
    assert dto.country_code == "US"
    assert dto.country_name == "United States"
    assert dto.anonymity == "elite proxy"
    assert dto.google == "no"
    assert dto.https == "yes"
    assert dto.last_checked == "1 minute ago"


def test_direct_init_fields() -> None:
    dto = Proxy(
        ip="10.0.0.1",
        port="3128",
        country_code="DE",
        country_name="Germany",
        anonymity="elite proxy",
        google="no",
        https="yes",
        last_checked="5 minutes ago",
    )
    assert dto.ip == "10.0.0.1"
    assert dto.port == "3128"
    assert dto.country_code == "DE"


def test_as_proxies_keys(dto) -> None:
    result = dto.as_proxies()
    assert isinstance(result, dict)
    assert "http" in result
    assert "https" in result


def test_as_proxies_values(dto) -> None:
    result = dto.as_proxies()
    assert result["http"] == "http://192.168.1.1:8080"
    assert result["https"] == "http://192.168.1.1:8080"


def test_equality() -> None:
    d1 = Proxy.from_list(SAMPLE)
    d2 = Proxy.from_list(SAMPLE)
    assert d1 == d2


def test_inequality() -> None:
    other = SAMPLE.copy()
    other[0] = "10.0.0.1"
    assert Proxy.from_list(SAMPLE) != Proxy.from_list(other)


# ------------------------------------------------------------------------------
