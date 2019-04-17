# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals


class GB2260Exception(Exception):
    pass


class SourceNotFound(GB2260Exception):
    pass


class RevisionNotFound(GB2260Exception):
    pass


class InvalidCode(GB2260Exception):
    pass
