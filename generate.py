# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A script to generate the data module.
"""

from __future__ import print_function, unicode_literals

import io
import itertools
import json
import os
import sys

if sys.version_info[0] == 2:
    imap = itertools.imap
else:
    imap = map

TAB_CHAR = ' ' * 4


def generate_revision_source_code(data_dir, source, revision):
    src_lines = [
        '# -*- coding: utf-8 -*-',
        '# this source code is auto-generated',
        'from __future__ import unicode_literals',
        '',
        "name = '{0}'".format(revision),
        'division_schema = {',
    ]
    for code, name in iter_divisions(data_dir, source, revision):
        src_lines.append(TAB_CHAR + "'{0}': '{1}',".format(code, name))
    src_lines.append('}')

    return '\n'.join(src_lines) + '\n'


def generate_source_source_code(revisions):
    src_lines = [
        '# -*- coding: utf-8 -*-',
        '# this source code is auto-generated',
        'from __future__ import unicode_literals',
        '',
        'revisions = [',
    ]
    for revision in sorted(revisions, reverse=True):
        src_lines.append(TAB_CHAR + "'{0}',".format(revision))
    src_lines.append(']')

    return '\n'.join(src_lines) + '\n'


def iter_divisions(data_dir, source, revision):
    filename = revision + '.tsv'
    path = os.path.join(data_dir, source if source != 'gb' else '', filename)

    with io.open(path, 'r', encoding='utf-8') as f:
        for line in itertools.islice(f, 1, None):  # skip first line
            _, _, code, name = line.strip().split('\t')
            yield code, name


def main():
    if len(sys.argv) < 2:
        print('Usage: {.argv[0]} [MANIFEST]'.format(sys),
              file=sys.stderr)
        sys.exit(1)

    manifest_path = sys.argv[1]
    data_dir = os.path.dirname(manifest_path)
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    # combine sources into a dummy 'curated' source
    # precedence: gb > stats > mca

    gb_revisions = set(manifest['gb'])
    stats_revisions = set(manifest['stats']) - gb_revisions
    mca_revisions = set(manifest['mca']) - gb_revisions - stats_revisions

    revisions_gen = itertools.chain(
        imap(lambda x: ('gb', x), gb_revisions),
        imap(lambda x: ('stats', x), stats_revisions),
        imap(lambda x: ('mca', x), mca_revisions),
    )

    revisions = gb_revisions | stats_revisions | mca_revisions

    output_dir = os.path.join('gb2260_v2', 'data')
    source_dir = os.path.join(output_dir, 'curated')

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    if not os.path.exists(source_dir):
        os.mkdir(source_dir)
    source_code = generate_source_source_code(revisions)
    path = os.path.join(source_dir, '__init__.py')
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(source_code)
    print('Metadata has been generated.', file=sys.stderr)

    for source, revision in revisions_gen:
        source_code = generate_revision_source_code(data_dir, source, revision)
        filename = 'revision_{0}.py'.format(revision)
        path = os.path.join(source_dir, filename)
        with io.open(path, 'w', encoding='utf-8') as f:
            f.write(source_code)

        message = 'Revision {0} has been generated.'.format(revision)
        print(message, file=sys.stderr)

    path = os.path.join(output_dir, '__init__.py')
    if not os.path.exists(path):
        open(path, 'w').close()
    else:
        os.utime(path, None)
    print('Done.', file=sys.stderr)


if __name__ == '__main__':
    main()
