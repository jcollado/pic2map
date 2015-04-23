# -*- coding: utf-8 -*-
"""Web application server tests."""

import json
import unittest

from datetime import datetime

from mock import patch

from pic2map.server.app import (
    index,
    row_to_serializable,
)

class RouteTest(unittest.TestCase):

    """Route function tests."""

    def test_index(self):
        """Index page."""
        render_template_patcher = patch('pic2map.server.app.render_template')
        location_db_patcher = patch('pic2map.server.app.LocationDB')
        row_to_serializable_patcher = patch('pic2map.server.app.row_to_serializable')
        with render_template_patcher as render_template, \
                location_db_patcher as location_db_cls, \
                row_to_serializable_patcher as row_to_serializable_mock:
            location_db = location_db_cls().__enter__()
            rows = [
                {'datetime': datetime(2015, 1, 1, 12, 34, 56)},
            ]
            location_db.select_all.return_value = rows
            new_row = {'datetime': 'some datetime'}
            row_to_serializable_mock.return_value = new_row
            index()
            render_template.assert_called_once_with(
                'index.html', rows=json.dumps([new_row]))


class RowToSerializableTest(unittest.TestCase):

    """Row to serializable tests."""

    def test_datetime(self):
        """Datetime field is converted to a string."""
        row = {'datetime': datetime(2015, 1, 1, 12, 34, 56)}
        new_row = row_to_serializable(row)
        self.assertDictEqual(
            new_row,
            {'datetime': '2015/01/01 12:34:56'},
        )
