# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""INSPIREHEP Celery app instantiation."""

from __future__ import absolute_import, division, print_function

import logging
import pkg_resources
import requests_mock

from flask_celeryext import create_celery_app

from inspirehep.factory import create_app


def mock_requests():
    mymock = requests_mock.Mocker(real_http=True)
    mymock.__enter__()

    resource_package = __name__
    pdf_path = '../tests/acceptance/fixtures/1708.03207'
    tar_path = '../tests/acceptance/fixtures/1708.03072'

    mymock.register_uri(requests_mock.ANY, 'http://export.arxiv.org/pdf/hep-th/9711200',
                        content=pkg_resources.resource_string(resource_package, pdf_path))

    mymock.register_uri(requests_mock.ANY, 'http://export.arxiv.org/e-print/hep-th/9711200',
                        content=pkg_resources.resource_string(resource_package, tar_path))


# use `requests_mock.Mocker` in a way that the context manager never exits in order to mock celery application requests
mock_requests()
celery = create_celery_app(create_app())

# We don't want to log to Sentry backoff errors
logging.getLogger('backoff').propagate = 0
