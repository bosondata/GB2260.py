# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import pytest

import gb2260_v2.code as dcode
from gb2260_v2.exceptions import InvalidCode


class TestCodePattern(object):

    @pytest.mark.parametrize('code', ['000000', '320000', '320200', '320203'])
    def test_valid_code(self, code):
        assert dcode.CODE_PATTERN.match(code)

    @pytest.mark.parametrize('code', ['ab0000', '1234567', ''])
    def test_invalid_code(self, code):
        assert not dcode.CODE_PATTERN.match(code)

    def test_groups(self):
        match = dcode.CODE_PATTERN.match('320203')
        assert match
        assert match.group('province') == '32'
        assert match.group('prefecture') == '02'
        assert match.group('county') == '03'


class TestProvinceCodePattern(object):

    @pytest.mark.parametrize('code', ['320000', '3200', '32'])
    def test_valid_code(self, code):
        assert dcode.PROVINCE_CODE_PATTERN.match(code)

    @pytest.mark.parametrize('code', [
        '320203', '320200', '320', '32000', '000000',
    ])
    def test_invalid_code(self, code):
        assert not dcode.PROVINCE_CODE_PATTERN.match(code)

    def test_groups(self):
        match = dcode.PROVINCE_CODE_PATTERN.match('320000')
        assert match
        assert match.group('code') == '32'


class TestPrefectureCodePattern(object):

    @pytest.mark.parametrize('code', ['320200', '3202'])
    def test_valid_code(self, code):
        assert dcode.PREFECTURE_CODE_PATTERN.match(code)

    @pytest.mark.parametrize('code', ['320203', '320000', '32020', '000000'])
    def test_invalid_code(self, code):
        assert not dcode.PREFECTURE_CODE_PATTERN.match(code)

    def test_groups(self):
        match = dcode.PREFECTURE_CODE_PATTERN.match('320200')
        assert match
        assert match.group('code') == '3202'


class TestCountyCodePattern(object):

    @pytest.mark.parametrize('code', ['320203'])
    def test_valid_code(self, code):
        assert dcode.COUNTY_CODE_PATTERN.match(code)

    @pytest.mark.parametrize('code', ['320200', '320000', '000000'])
    def test_invalid_code(self, code):
        assert not dcode.COUNTY_CODE_PATTERN.match(code)

    def test_groups(self):
        match = dcode.COUNTY_CODE_PATTERN.match('320203')
        assert match
        assert match.group('code') == '320203'


class TestToProvince(object):

    @pytest.mark.parametrize('code, expected', [
        ('320203', '320000'),
        ('320200', '320000'),
        ('320000', '320000'),
    ])
    def test_success(self, code, expected):
        assert dcode.to_province(code) == expected

    @pytest.mark.parametrize('code, exc', [
        ('320', InvalidCode),
        ('000203', ValueError),
    ])
    def test_failure(self, code, exc):
        with pytest.raises(exc):
            dcode.to_province(code)


class TestToPrefecture(object):

    @pytest.mark.parametrize('code, expected', [
        ('320203', '320200'),
        ('320200', '320200'),
    ])
    def test_success(self, code, expected):
        assert dcode.to_prefecture(code) == expected

    @pytest.mark.parametrize('code, exc', [
        ('320', InvalidCode),
        ('320003', ValueError),
        ('000203', ValueError),
        ('000003', ValueError),
    ])
    def test_failure(self, code, exc):
        with pytest.raises(exc):
            dcode.to_prefecture(code)


class TestMakePrefecturePattern(object):

    def test_success(self):
        pattern = dcode.make_prefecture_pattern('320000')
        assert pattern.match('320200')
        assert not pattern.match('320203')
        assert not pattern.match('110101')

    @pytest.mark.parametrize('code', ['320200', '320203'])
    def test_failure(self, code):
        with pytest.raises(InvalidCode):
            dcode.make_prefecture_pattern(code)


class TestMakeCountyPattern(object):

    def test_success(self):
        pattern = dcode.make_county_pattern('320200')
        assert pattern.match('320203')
        assert not pattern.match('320581')

    @pytest.mark.parametrize('code', ['320000'])
    def test_failure(self, code):
        with pytest.raises(InvalidCode):
            dcode.make_county_pattern(code)


class TestSplit(object):

    @pytest.mark.parametrize('code, result', [
        ('320203', ['320000', '320200', '320203']),
        ('320200', ['320000', '320200', None]),
        ('320000', ['320000', None, None]),
    ])
    def test_success(self, code, result):
        assert dcode.split(code) == result

    @pytest.mark.parametrize('code', ['32'])
    def test_failure(self, code):
        with pytest.raises(InvalidCode):
            dcode.split(code)
