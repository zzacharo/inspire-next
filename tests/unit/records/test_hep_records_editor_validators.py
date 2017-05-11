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

from inspirehep.modules.records.validators.helpers import (
    FIELD_REQUIRE_FIELD_VALUES_TEMPLATE,
    FIELD_REQUIRE_FIELD_TEMPLATE,
    FIELD_VALUE_REQUIRE_FIELD_TEMPLATE
)

from inspirehep.modules.records.validators.warning_rules import (
    check_date_present_in_record,
    check_affiliations_if_authors_exist,
    check_thesis_info_if_doctype_value_thesis_present,
    check_cnum_if_doctype_value_proceedings_present,
    check_cnum_if_doctype_value_conference_paper_present,
    check_if_2_cnum_exist_in_publication_info,
    check_doctype_values_if_cnum_present,
    check_accelerator_experiments_if_collaborations_exist,
    check_accelerator_experiments_for_experiment,
    check_thesis_info_and_supervisor_to_exist_in_thesis,
    check_if_no_pages_for_publication_info
)
from collections import defaultdict


def format_warning(_error):
    return [{
            'message': _error.message,
            'type': _error.cause or 'Warning'
    }]


def json_pointer_format(path):
    path = '/' + '/'.join(str(el) for el in path)
    if path == '/':
        path = 'globalErrors'
    return path


def validate(validator_fn, record):
    result = defaultdict(list)
    for e in validator_fn(record):
        result[json_pointer_format(e.path)].extend(format_warning(e))
    return result


def test_check_date_present_in_record():
    sample_valid_record = {
        'thesis_info': {
            'date': ''
        }
    }

    result = validate(check_date_present_in_record, sample_valid_record)

    assert result == {}

    sample_invalid_record = {
        'not_date_field': {
            'not_date_field_key': 'value'
        }
    }

    expected = {
        'globalErrors': [{
            'message': 'No date present.',
            'type': 'Warning'
        }]
    }
    result = validate(check_date_present_in_record, sample_invalid_record)
    assert result == expected


def test_check_affiliations_if_authors_exist():
    sample_record = {
        'authors': [
            {
                'not_affiliations_field': []
            },
            {
                'affiliations': []
            },
            {
                'affiliations': [{
                    'key': 'value'
                }]
            }
        ]
    }
    expected = {
        '/authors/0': [{
            'message': FIELD_REQUIRE_FIELD_TEMPLATE.format(
                field='authors',
                required='affiliations'),
            'type': 'Warning'
        }],
        '/authors/1': [{
            'message': FIELD_REQUIRE_FIELD_TEMPLATE.format(
                field='authors',
                required='affiliations'),
            'type': 'Warning'
        }]

    }
    result = validate(check_affiliations_if_authors_exist, sample_record)
    assert result == expected


def test_check_thesis_info_if_doctype_value_thesis_present():
    sample_record = {
        'document_type': [
            'thesis'
        ],
        'not_thesis_info_field': 'value'
    }
    expected = {
        'globalErrors': [{
            'message': FIELD_VALUE_REQUIRE_FIELD_TEMPLATE.format(
                field='document_type',
                value='thesis',
                required='thesis_info'),
            'type': 'Warning'
        }]
    }
    result = validate(check_thesis_info_if_doctype_value_thesis_present, sample_record)
    assert result == expected


def test_cnum_if_doctype_value_proceedings_present():
    sample_record = {
        'document_type': [
            'proceedings'
        ],
        'publication_info': [{
            'not_cnum_field': 'value'
        }]
    }
    expected = {
        'globalErrors': [{
            'message': FIELD_VALUE_REQUIRE_FIELD_TEMPLATE.format(
                field='document_type',
                value='proceedings',
                required='cnum'),
            'type': 'Warning'
        }]
    }
    result = validate(check_cnum_if_doctype_value_proceedings_present, sample_record)
    assert result == expected


def test_check_cnum_if_doctype_value_conference_paper_present():
    sample_record = {
        'document_type': [
            'conference paper'
        ],
        'publication_info': [{
            'not_cnum_field': 'value'
        }]
    }
    expected = {
        'globalErrors': [{
            'message': FIELD_VALUE_REQUIRE_FIELD_TEMPLATE.format(
                field='document_type',
                value='conference paper',
                required='cnum'),
            'type': 'Warning'
        }]
    }
    result = validate(check_cnum_if_doctype_value_conference_paper_present, sample_record)
    assert result == expected


def test_check_if_2_cnum_exist_in_publication_info():
    sample_record = {
        'publication_info': [
            {
                'cnum': 'value'
            },
            {
                'cnum': 'value'
            },
            {
                'not_cnum': 'value'
            }
        ]
    }
    expected = {
        'globalErrors': [{
            'message': "2 cnums found in 'publication info' field.",
            'type': 'Warning'
        }]
    }
    result = validate(check_if_2_cnum_exist_in_publication_info, sample_record)
    assert result == expected


def test_check_doctype_values_if_cnum_present():
    sample_record = {
        'publication_info': [{
                'cnum': 'value'
        }],
        'document_type': [
            'not_one_of_the_required_values',
            'another_not_one_of_the_required_values'
        ]
    }
    required_values = ['proceedings', 'conference_paper']
    expected = {
        'globalErrors': [{
            'message': FIELD_REQUIRE_FIELD_VALUES_TEMPLATE.format(
                field='cnum',
                required='document_type',
                values=required_values),
            'type': 'Warning'
        }]
    }
    result = validate(check_doctype_values_if_cnum_present, sample_record)
    assert result == expected


def test_check_accelerator_experiments_if_collaborations_exist():
    sample_record = {
        'collaborations': [{
            'cnum': 'value'
        }],
        'not_accelerator_experiments': []
    }
    expected = {
        'globalErrors': [{
            'message': FIELD_REQUIRE_FIELD_TEMPLATE.format(
                field='collaborations',
                required='accelerator_experiments'),
            'type': 'Warning'
        }]
    }
    result = validate(check_accelerator_experiments_if_collaborations_exist, sample_record)
    assert result == expected


def test_check_accelerator_experiments_for_experiment():
    sample_record = {
        'accelerator_experiments': [{
            'not_experiment_field': 'value'
        }]
    }
    expected = {
        'globalErrors': [{
           'message': "'accelerator_experiments' field should have at least "
                       "one experiment",
            'type': 'Warning'
        }]
    }
    result = validate(check_accelerator_experiments_for_experiment, sample_record)
    assert result == expected


def test_check_thesis_info_and_supervisor_to_exist_in_thesis():
    sample_record = {
        'not_thesis_info': 'value',
        'inspire_roles': ['not_supervisor'],
        'document_type': [
            'thesis'
        ]
    }
    expected = {
        'globalErrors': [{
            'message': "Thesis should have both 'thesis_info' and "
                       "'supervisor' field.",
            'type': 'Warning'
        }]
    }
    result = validate(check_thesis_info_and_supervisor_to_exist_in_thesis, sample_record)
    assert result == expected


def test_check_if_no_pages_for_publication_info():
    sample_record = {
        'publication_info': [
            {
                'page_start': 'value'
            },
            {
                'page_end': 'value'
            },
            {
                'not_page_start_or_end_field': 'value'
            },
            {
                'page_start': 'value',
                'page_end': 'value'
            }
        ]
    }
    expected = {
        '/publication_info/2': [{
            'message': "Missing 'page_start' or 'page_end' field.",
            'type': 'Warning'
        }]
    }
    result = validate(check_if_no_pages_for_publication_info, sample_record)
    assert result == expected

