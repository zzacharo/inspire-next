#
# This file is part of INSPIRE.
# Copyright (C) 2014, 2015, 2016, 2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from .helpers import (
    check_if_field_exists_in_dict_list_x_times,
    check_field_values_not_in_required_values_for_record,
    FIELD_REQUIRE_FIELD_VALUES_TEMPLATE,
    FIELD_VALUE_REQUIRE_FIELD_TEMPLATE,
    check_if_listfield_property_values_are_valid,
    query_db_for_duplicates_for_field_listitem_with_index,
    get_query_results_if_exceed_limit,
    FIELD_REQUIRE_FIELD_TEMPLATE,
    SCHEMA_DATE_PATHS,
    GET_RESULTS_FOR_FIELD_PROPERTY_QUERYSTRING_TEMPLATE
)

from jsonschema import ValidationError
from inspirehep.utils.record import get_value

'''
Warnings Validator Functions
'''


def check_date_present_in_record(record):
    for date_path in SCHEMA_DATE_PATHS:
        if get_value(record, date_path):
            return
    yield ValidationError(path=[''],
                          message='No date present.',
                          cause='Warning')


def check_if_journal_title_is_canonical(record):
    def _check_for_journal_title(field, prop, value, index, errortype):
        querystring = GET_RESULTS_FOR_FIELD_PROPERTY_QUERYSTRING_TEMPLATE.format(field=field,
                                                                                 prop=prop,
                                                                                 value=value)
        results = get_query_results_if_exceed_limit(querystring, 0)
        if not results:
            yield ValidationError(path=['{field}/{index}/{prop}'.format(field=field, index=index, prop=prop)],
                                  message="Journal title '{title}' doesn't exist.'".format(title=value),
                                  cause=errortype)
    for e in check_if_listfield_property_values_are_valid(record=record,
                                                          field='publication_info',
                                                          prop='journal_title',
                                                          checker=_check_for_journal_title):
        yield e


def check_affiliations_if_authors_exist(record):
    def _check_affiliations_for_author(author, index):
        if 'affiliations' not in author or len(author['affiliations']) == 0:
            yield ValidationError(path=['authors/{index}'.format(index=index)],
                                  message=FIELD_REQUIRE_FIELD_TEMPLATE.format(
                                      field='authors',
                                      required='affiliations'),
                                  cause='Warning')

    if 'authors' in record:
        for i, author in enumerate(record['authors']):
            for e in _check_affiliations_for_author(author, i):
                yield e


def check_thesis_info_if_doctype_value_thesis_present(record):
    doctype_values = record.get('document_type', [])
    if 'thesis' in doctype_values:
        if not 'thesis_info' in record:
            yield ValidationError(path=[''],
                                  message=FIELD_VALUE_REQUIRE_FIELD_TEMPLATE.format(
                                      field='document_type',
                                      value='thesis',
                                      required='thesis_info'),
                                  cause='Warning')


def check_cnum_if_doctype_value_proceedings_present(record):
    doctype_values = record.get('document_type', [])
    if 'proceedings' in doctype_values:
        if not check_if_field_exists_in_dict_list_x_times('cnum', record.get('publication_info', [])):
            yield ValidationError(path=[''],
                                  message=FIELD_VALUE_REQUIRE_FIELD_TEMPLATE.format(
                                      field='document_type',
                                      value='proceedings',
                                      required='cnum'),
                                  cause='Warning')


def check_cnum_if_doctype_value_conference_paper_present(record):
    doctype_values = record.get('document_type', [])
    if 'conference paper' in doctype_values:
        if not check_if_field_exists_in_dict_list_x_times('cnum', record.get('publication_info', [])):
            yield ValidationError(path=[''],
                                  message=FIELD_VALUE_REQUIRE_FIELD_TEMPLATE.format(
                                      field='document_type',
                                      value='conference paper',
                                      required='cnum'),
                                  cause='Warning')


def check_if_2_cnum_exist_in_publication_info(record):
    if check_if_field_exists_in_dict_list_x_times('cnum', record.get('publication_info', []), limit=2):
        yield ValidationError(path=[''],
                              message="2 cnums found in 'publication info' field.",
                              cause='Warning')


def check_doctype_values_if_cnum_present(record):
    if check_if_field_exists_in_dict_list_x_times('cnum', record.get('publication_info', [])):
        required_values = ['proceedings', 'conference_paper']
        if check_field_values_not_in_required_values_for_record(record, 'document_type', required_values):
            yield ValidationError(path=[''],
                                  message=FIELD_REQUIRE_FIELD_VALUES_TEMPLATE.format(
                                      field='cnum',
                                      required='document_type',
                                      values=required_values),
                                  cause='Warning')


def check_accelerator_experiments_if_collaborations_exist(record):
    if 'collaborations' in record:
        if not 'accelerator_experiments' in record:
            yield ValidationError(path=[''],
                                  message=FIELD_REQUIRE_FIELD_TEMPLATE.format(
                                      field='collaborations',
                                      required='accelerator_experiments'),
                                  cause='Warning')


def check_if_reportnumber_exist_in_other_records(record):
    for e in check_if_listfield_property_values_are_valid(record=record,
                                                          field='report_numbers',
                                                          prop='value',
                                                          checker=query_db_for_duplicates_for_field_listitem_with_index,
                                                          errortype='Warning'):
        yield e


def check_accelerator_experiments_for_experiment(record):
    if 'accelerator_experiments' in record:
        for experiment in record['accelerator_experiments']:
            if 'experiment' in experiment:
                return
        yield ValidationError(path=[''],
                              message="'accelerator_experiments' field should have at least one experiment",
                              cause='Warning')


def check_thesis_info_and_supervisor_to_exist_in_thesis(record):
    doctype_values = record.get('document_type', [])
    if 'thesis' in doctype_values:
        if 'thesis_info' not in record and 'supervisor' not in record.get('inspire_roles', []):
            yield ValidationError(path=[''],
                                  message="Thesis should have both 'thesis_info' and 'supervisor' field.",
                                  cause='Warning')


def check_if_no_pages_for_publication_info(record):
    def _check_for_pages(publication, index):
        if all(k not in publication for k in ['page_start', 'page_end']):
            yield ValidationError(path=['publication_info/{index}'.format(index=index)],
                                  message="Missing 'page_start' or 'page_end' field.",
                                  cause='Warning')

    for i, publication in enumerate(record.get('publication_info', [])):
        for e in _check_for_pages(publication, i):
            yield e


# def check_external_urls_if_work(record):
#     def _check_if_url_works(field, prop, value, index, errortype):
#         try:
#             resp = requests.get(value)
#             if not resp.ok:
#                 raise ConnectionError
#         except ConnectionError:
#             raise ValidationError(key='/{field}/{index}/{prop}'.format(field=field, prop=prop, index=index),
#                                   message=FIELD_VALIDATION_TEMPLATE.format(
#                                       field='urls',
#                                       value=value
#                                   ),
#                                   type=errortype)
#         return {}
#
#     check_if_listfield_property_values_are_valid(record=record,
#                                                  field='urls',
#                                                  prop='value',
#                                                  checker=_check_if_url_works,
#                                                  errortype='Error'
#                                                  )
#     return {}
#
#
# # TODO: Fix validation way because dosen't work for our dois
# def check_external_dois_if_exist(record):
#     def _check_if_doi_works(field, prop, value, index, errortype):
#         doi_url = DOI_VALIDATION_URL.format(doi=value)
#         try:
#             resp = requests.get(doi_url)
#             if not resp.ok:
#                 raise ConnectionError
#         except ConnectionError:
#             raise ValidationError(key='/{field}/{index}/{prop}'.format(field=field, prop=prop, index=index),
#                                   message=FIELD_VALIDATION_TEMPLATE.format(
#                                       field='dois',
#                                       value=value
#                                   ),
#                                   type=errortype)
#         return {}
#
#     try:
#         check_if_listfield_property_values_are_valid(record=record,
#                                                      field='dois',
#                                                      prop='value',
#                                                      checker=_check_if_doi_works,
#                                                      errortype='Warning'
#                                                      )
#     except ValidationError:
#         raise
#     return {}

