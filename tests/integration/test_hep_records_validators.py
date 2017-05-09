# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Test helpers."""

from inspirehep.modules.records.validators.rules import (
    check_if_isbn_exist_in_other_records
)

from inspirehep.modules.records.validators.helpers import (
    FIELD_DUPLICATE_VALUES_FOUND_TEMPLATE
)

import pytest
from invenio_db import db
from inspirehep.modules.records.api import InspireRecord


@pytest.fixture(scope='function')
def test_record(app):
    sample_record = {
        '$schema': 'http://localhost:5000/schemas/records/hep.json',
        'control_number': 111,
        'document_type': [
            'article',
        ],
        'isbns': [
            {'value': '9783598215001'},
        ],
        'report_numbers': [
            {'value': '11111'}
        ],
        'titles': [
            {'title': 'sample'},
        ],
        'self': {
            '$ref': 'http://localhost:5000/schemas/records/hep.json',
        }
    }
    dupl_sample_record = {
        '$schema': 'http://localhost:5000/schemas/records/hep.json',
        'control_number': 222,
        'document_type': [
            'article',
        ],
        'isbns': [
            {'value': '9783598215001'},
        ],
        'report_numbers': [
            {'value': '11111'}
        ],
        'titles': [
            {'title': 'another_sample'},
        ],
        'self': {
            '$ref': 'http://localhost:5000/schemas/records/hep.json',
        }
    }

    record_id = InspireRecord.create(sample_record).id
    dupl_record_id = InspireRecord.create(dupl_sample_record).id

    db.session.commit()

    yield

    InspireRecord.get_record(record_id)._delete(force=True)
    InspireRecord.get_record(dupl_record_id)._delete(force=True)

    db.session.commit()


def format_error(_error):
    path = '/' + '/'.join(str(el) for el in _error.path)
    if path == '/':
        path = 'globalErrors'
    return {
        path: [{
            'message': _error.message,
            'type': _error.cause or 'Error'
        }]
    }


def test_check_if_isbn_exist_in_other_records(app, test_record):
    sample_record = {
        '$schema': 'http://localhost:5000/schemas/records/hep.json',
        'control_number': 333,
        'document_type': [
            'book',
        ],
        'isbns': [
            {'value': '9783598215001'},
        ],
        'titles': [
            {'title': 'sample_record_title'},
        ],
        'self': {
            '$ref': 'http://localhost:5000/schemas/records/hep.json',
        }
    }

    expected = [{
        '/isbns/0/value': [{
            'message': FIELD_DUPLICATE_VALUES_FOUND_TEMPLATE.format(
                field='isbns',
                value='9783598215001'
            ),
            'type': 'Error'
        }]
    }]

    result = [format_error(e) for e in check_if_isbn_exist_in_other_records(sample_record)]
    assert result == expected
