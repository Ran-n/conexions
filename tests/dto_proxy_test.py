#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Authors:	Ran#
#+ Created:	2026/03/11 07:55:18.174519
#+ Revised:	2026/03/11 07:55:18.174519
# ------------------------------------------------------------------------------
import pytest

from conexions.dto_proxy import ProxyDTO
# ------------------------------------------------------------------------------

SAMPLE: list[str] = [
        '192.168.1.1',
        '8080',
        'US',
        'United States',
        'elite proxy',
        'no',
        'yes',
        '1 minute ago'
        ]

# ------------------------------------------------------------------------------

@pytest.fixture
def dto() -> ProxyDTO:
    return ProxyDTO(SAMPLE)

# ------------------------------------------------------------------------------

def test_init_fields(dto) -> None:
    assert dto.ip           == '192.168.1.1'
    assert dto.port         == '8080'
    assert dto.country_code == 'US'
    assert dto.country_name == 'United States'
    assert dto.anonymity    == 'elite proxy'
    assert dto.google       == 'no'
    assert dto.https        == 'yes'
    assert dto.last_checked == '1 minute ago'

def test_format_keys(dto) -> None:
    fmt = dto.format()
    assert isinstance(fmt, dict)
    assert 'http' in fmt
    assert 'https' in fmt

def test_format_values(dto) -> None:
    fmt = dto.format()
    assert fmt['http']  == 'http://192.168.1.1:8080'
    assert fmt['https'] == 'http://192.168.1.1:8080'

def test_equality() -> None:
    d1 = ProxyDTO(SAMPLE)
    d2 = ProxyDTO(SAMPLE)
    assert d1 == d2

def test_inequality() -> None:
    other = SAMPLE.copy()
    other[0] = '10.0.0.1'
    assert ProxyDTO(SAMPLE) != ProxyDTO(other)
# ------------------------------------------------------------------------------
