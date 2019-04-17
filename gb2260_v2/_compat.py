# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import sys

PY2 = sys.version_info[0] == 2

if PY2:
    text_type = unicode
    binary_type = str

    def iteritems(d):
        return d.iteritems()
else:
    text_type = str
    binary_type = bytes

    def iteritems(d):
        return d.items()


def ensure_text(value, encoding):
    if isinstance(value, text_type):
        return value
    return value.decode(encoding)


def ensure_str(value, encoding):
    if isinstance(value, str):
        return value
    if PY2:
        return value.encode(encoding)
    else:
        return value.decode(encoding)
