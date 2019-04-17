# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import pytest

from gb2260_v2.division import Division
from gb2260_v2.revision import Revision


@pytest.fixture
def revision(mocker):
    mocked = mocker.MagicMock(spec=Revision)
    mocked.name = 'foo'
    return mocked


@pytest.fixture
def division(revision):
    return Division(code='999999', revision=revision, name='测试')


def test_equal(revision):
    a = Division(code='999999', revision=revision, name='测试')
    b = Division(code='999999', revision=revision, name='不同')
    assert a == b


def test_hash(revision):
    a = Division(code='999999', revision=revision, name='测试')
    b = Division(code='999999', revision=revision, name='不同')
    pool = {a: None}
    assert b in pool


def test_repr(division):
    expected = '<Division 999999 测试 rev=foo>'

    # repr is str in both PY2 and PY3
    import sys
    if sys.version_info[0] == 2:
        expected = expected.encode('utf-8')

    assert repr(division) == expected


def test_province(revision, division):
    division.province
    revision.get_province.assert_called_once_with(division.code)


def test_prefecture(revision, division):
    division.prefecture
    revision.get_prefecture.assert_called_once_with(division.code)


def test_description(revision, division):
    division.description
    revision.describe.assert_called_once_with(division.code)


def test_is_province(mocker, division):
    mocked = mocker.patch('gb2260_v2.code.PROVINCE_CODE_PATTERN')
    division.is_province
    mocked.match.assert_called_once_with(division.code)


def test_is_prefecture(mocker, division):
    mocked = mocker.patch('gb2260_v2.code.PREFECTURE_CODE_PATTERN')
    division.is_prefecture
    mocked.match.assert_called_once_with(division.code)


def test_is_county(mocker, division):
    mocked = mocker.patch('gb2260_v2.code.COUNTY_CODE_PATTERN')
    division.is_county
    mocked.match.assert_called_once_with(division.code)
