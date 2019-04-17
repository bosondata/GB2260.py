# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from gb2260_v2.revision import Source


# GB2260 is mainly a proxy object for Source & Revision


class GB2260(object):
    source = Source('curated')

    __slots__ = ['revision']

    def __init__(self, revision=None):
        revision = revision or self.source.latest_revision
        self.revision = self.source.load_revision(revision)

    @classmethod
    def revisions(cls):
        return cls.source.all_revisions

    def get(self, code):
        return self.revision.get(code)

    def provinces(self):
        return self.revision.provinces()

    def prefectures(self, province_code):
        return self.revision.prefectures(province_code)

    def counties(self, prefecture_code):
        return self.revision.counties(prefecture_code)
