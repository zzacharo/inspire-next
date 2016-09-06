# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2016 CERN.
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
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Pytest configuration for web tests."""

from __future__ import absolute_import, division, print_function

from os import environ
from time import sleep

import pytest

from selenium import webdriver

from inspirehep.config import SERVER_NAME

@pytest.yield_fixture(scope='session')
def driver():
    """Selenium driver."""

    if 'TRAVIS' in environ:
        desired_cap = desired_cap = {
            'platform': "Mac OS X 10.11",
            'browserName': "firefox",
            'version': "48",
            'tunnel-identifier': environ['TRAVIS_JOB_NUMBER']
        }

        driver = webdriver.Remote(
            command_executor='http://{SAUCE_USERNAME}:{SAUCE_ACCESSKEY}@localhost:4445/wd/hub'.format(environ),
            desired_capabilities=desired_cap)
    else:
        driver = webdriver.firefox()

    driver.implicitly_wait(10)
    driver.get("http://{0}".format(SERVER_NAME))

    yield driver
