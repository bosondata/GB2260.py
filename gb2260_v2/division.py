# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import gb2260_v2.code as dcode
from gb2260_v2._compat import ensure_str


class Division(object):
    __slots__ = ['_code', '_name', '_revision']

    def __init__(self, code, name, revision):
        self._code = code
        self._name = name
        self._revision = revision

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    @property
    def revision(self):
        return self._revision.name

    def __repr__(self):
        message = '<Division {0} {1} rev={2}>'.format(
            self.code, self.name, self.revision)
        return ensure_str(message, 'utf-8')

    def __eq__(self, other):
        return (self.code, self.revision) == (other.code, other.revision)

    def __hash__(self):
        return hash((self.__class__, self._code, self._revision.name))

    @property
    def province(self):
        return self._revision.get_province(self._code)

    @property
    def prefecture(self):
        return self._revision.get_prefecture(self._code)

    @property
    def description(self):
        return self._revision.describe(self._code)

    @property
    def is_province(self):
        return bool(dcode.PROVINCE_CODE_PATTERN.match(self._code))

    @property
    def is_prefecture(self):
        return bool(dcode.PREFECTURE_CODE_PATTERN.match(self._code))

    @property
    def is_county(self):
        return bool(dcode.COUNTY_CODE_PATTERN.match(self._code))
