# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import pytest

from gb2260_v2.exceptions import RevisionNotFound, SourceNotFound
from gb2260_v2.revision import Revision, Source


@pytest.fixture
def mocked_source(mocker):
    source = mocker.patch('gb2260_v2.data.curated')
    source.revisions = ['198012', '200212']
    return source


@pytest.fixture
def mocked_revision(mocker, mocked_source):
    revision = mocker.patch('gb2260_v2.data.curated.revision_198012')
    revision.name = '198012'
    revision.division_schema = {
        '990000': '测试省',
        '999900': '测试市',
        '999999': '测试区',
    }

    mocked_source.revision_foo = revision
    return revision


class TestSource(object):

    def test_all_revisions(self, mocked_source):
        assert Source('curated').all_revisions == ['198012', '200212']

    def test_latest_revision(self, mocked_source):
        assert Source('curated').latest_revision == '198012'

    def test_source_not_found(self):
        with pytest.raises(SourceNotFound):
            Source('nothing')

    def test_load_revision(self, mocked_revision):
        revision = Source('curated').load_revision('198012')
        assert revision is not None
        assert revision.name == '198012'
        assert revision.division_schema == {
            '990000': '测试省',
            '999900': '测试市',
            '999999': '测试区',
        }

    def test_revision_not_found(self, mocked_source):
        source = Source('curated')
        with pytest.raises(RevisionNotFound):
            source.load_revision('foo')


class TestRevision(object):

    @pytest.fixture
    def revision(self):
        schema = {
            '990000': '测试省',
            '999900': '测试市',
            '999999': '测试区',
        }
        return Revision(name='测试', division_schema=schema)

    def test_get(self, revision):
        division = revision.get('999999')
        assert division is not None
        assert division.name == '测试区'
        assert division.code == '999999'
        assert division.revision == '测试'

        assert revision.get('320203') is None

    def test_provinces(self, revision):
        provinces = revision.provinces()
        assert len(provinces) == 1
        assert provinces[0].code == '990000'

    def test_prefectures(self, revision):
        prefectures = revision.prefectures('990000')
        assert len(prefectures) == 1
        assert prefectures[0].code == '999900'

    def test_counties(self, revision):
        counties = revision.counties('999900')
        assert len(counties) == 1
        assert counties[0].code == '999999'

    @pytest.mark.parametrize('code', ['999999', '999900', '990000'])
    def test_get_province(self, revision, code):
        province = revision.get_province(code)
        assert province.code == '990000'

    @pytest.mark.parametrize('code', ['999999', '999900'])
    def test_get_prefecture(self, revision, code):
        prefecture = revision.get_prefecture(code)
        assert prefecture.code == '999900'

    def test_get_prefecture_for_province(self, revision):
        prefecture = revision.get_prefecture('990000')
        assert prefecture is None

    @pytest.mark.parametrize('code, result', [
        ('999999', '测试省 测试市 测试区'),
        ('999900', '测试省 测试市'),
        ('990000', '测试省'),
    ])
    def test_describe(self, revision, code, result):
        assert revision.describe(code) == result
