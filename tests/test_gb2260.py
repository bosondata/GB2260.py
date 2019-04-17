# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import pytest

from gb2260_v2.gb2260 import GB2260
from gb2260_v2.revision import Revision, Source


@pytest.fixture
def mocked_source(mocker):
    mocked = mocker.MagicMock(spec=Source)
    GB2260.source = mocked
    return mocked


@pytest.fixture
def mocked_revision(mocker, mocked_source):
    mocked = mocker.MagicMock(spec=Revision)
    mocked_source.load_revision.return_value = mocked
    return mocked


def test_revisions(mocked_source):
    revisions = ['hello', 'world']
    mocked_source.all_revisions = revisions
    assert GB2260.revisions() == revisions


def test_init(mocked_source, mocked_revision):
    GB2260('foo')
    mocked_source.load_revision.assert_called_once_with('foo')


def test_default_revision(mocked_source, mocked_revision):
    mocked_source.latest_revision = 'hello'
    GB2260()
    mocked_source.load_revision.assert_called_once_with('hello')


def test_get(mocked_source, mocked_revision):
    GB2260('foo').get('999999')
    mocked_revision.get.assert_called_once_with('999999')


def test_provinces(mocked_source, mocked_revision):
    GB2260('foo').provinces()
    mocked_revision.provinces.assert_called_once()


def test_prefectures(mocked_source, mocked_revision):
    GB2260('foo').prefectures('320000')
    mocked_revision.prefectures.assert_called_once_with('320000')


def test_counties(mocked_source, mocked_revision):
    GB2260('foo').counties('320000')
    mocked_revision.counties.assert_called_once_with('320000')
