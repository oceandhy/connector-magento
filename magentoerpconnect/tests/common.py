# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2013 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""
Helpers usable in the tests
"""

import mock
from contextlib import contextmanager
from .test_data import magento_base_responses
from ..unit.backend_adapter import call_to_key


def get_magento_response(method, arguments):
    key = call_to_key(method, arguments)
    assert key in magento_base_responses, (
        "%s not found in magento responses" % str(key))
    return magento_base_responses[key]


@contextmanager
def mock_api():
    with mock.patch('magento.API') as API:
        api_mock = mock.MagicMock(name='magento.api')
        API.return_value = api_mock
        api_mock.__enter__.return_value = api_mock
        api_mock.call.side_effect = get_magento_response
        yield


class MockResponseImage(object):
    def __init__(self, resp_data, code=200, msg='OK'):
        self.resp_data = resp_data
        self.code = code
        self.msg = msg
        self.headers = {'content-type': 'image/jpeg'}

    def read(self):
        return self.resp_data

    def getcode(self):
        return self.code


@contextmanager
def mock_urlopen_image():
    with mock.patch('urllib2.urlopen') as urlopen:
        api_mock = mock.MagicMock()
        urlopen.return_value = MockResponseImage('')
        # api_mock.__enter__.return_value = api_mock
        # api_mock.call.side_effect = get_magento_response
        yield
