# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import re

from gb2260_v2.exceptions import InvalidCode

# GB/T 2260 conformant code pattern.
# Every two digits form a province / prefecture / county layer subcode.
# NOTE: Whether a code has a corresponding division has to be considered along
#       with a specific revision.
CODE_PATTERN = re.compile(
    r'^(?P<province>\d\d)(?P<prefecture>\d\d)(?P<county>\d\d)$')

# The following province / prefecture / county code patterns are from the Spec.
# Subcode 00 is considered special, denoting the upper level division.
# When used as an argument, trailing 00s can be ommited.

# Province code
# e.g. 320000 / 3200 / 32
# NOTE: Allowing 320000 is an extension to the Spec.
PROVINCE_CODE_PATTERN = re.compile(r'^(?P<code>(?!00)\d\d)(?:00){0,2}$')

# Prefecture code
# e.g. 320200 / 3202
PREFECTURE_CODE_PATTERN = re.compile(r'^(?P<code>(?:(?!00)\d\d){2})(?:00)?$')

# County code
# e.g. 320203
COUNTY_CODE_PATTERN = re.compile(r'^(?P<code>(?:(?!00)\d\d){3})$')


def to_province(code):
    """Returns the corresponding province level division code.
    :raises InvalidCode: if the code is not a valid GB/T 2260 code
    :raises ValueError: the province level subcode is 00
    """
    match = CODE_PATTERN.match(code)
    if not match:
        raise InvalidCode(code)
    province = match.group('province')
    if province == '00':
        raise ValueError(code)
    return '{0}0000'.format(province)


def to_prefecture(code):
    """Returns the corresponding prefecture level division code.
    :raises InvalidCode: if the code is not a valid GB/T 2260 code
    :raises ValueError: the province or prefecture level subcode is 00
    """
    match = CODE_PATTERN.match(code)
    if not match:
        raise InvalidCode(code)
    province = match.group('province')
    prefecture = match.group('prefecture')
    if province == '00' or prefecture == '00':
        raise ValueError(code)
    return '{0}{1}00'.format(province, prefecture)


def make_prefecture_pattern(province_code):
    """Returns a pattern for matching prefectures in the province.
    :raises InvalidCode: if the province_code is not a valid province code.
    """
    match = PROVINCE_CODE_PATTERN.match(province_code)
    if not match:
        raise InvalidCode(province_code)
    raw = r'{0}(?!00)\d\d00'.format(match.group('code'))
    return re.compile(raw)


def make_county_pattern(prefecture_code):
    """Returns a pattern for matching counties in the prefecture.
    :raises InvalidCode: if the prefecture_code is not a valid prefecture code.
    """
    match = PREFECTURE_CODE_PATTERN.match(prefecture_code)
    if not match:
        raise InvalidCode(prefecture_code)
    raw = r'{0}(?!00)\d\d'.format(match.group('code'))
    return re.compile(raw)


def split(code):
    """Returns codes for all the three level divisions.
    :raises InvalidCode: if the code is not a valid GB/T 2260 code
    """
    match = CODE_PATTERN.match(code)
    if not match:
        raise InvalidCode(code)
    subcodes = match.groups()
    province, prefecture, county = subcodes

    codes = [
        None if province == '00' else '{0}0000'.format(*subcodes),
        None if prefecture == '00' else '{0}{1}00'.format(*subcodes),
        None if county == '00' else '{0}{1}{2}'.format(*subcodes),
    ]
    return codes
