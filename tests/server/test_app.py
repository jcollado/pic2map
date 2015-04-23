# -*- coding: utf-8 -*-
"""Web application server tests."""

import unittest

from datetime import datetime

from pic2map.server.app import row_to_serializable


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
