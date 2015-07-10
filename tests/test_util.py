# -*- coding: utf-8 -*-
import unittest

from operator import itemgetter

from pic2map.util import average


class AverageTest(unittest.TestCase):

    """Average function tests."""

    def test_identity(self):
        """Identifiy function used by default."""
        self.assertEqual(average([1, 2]), 1.5)

    def test_custom_function(self):
        """Custom function used if passed."""
        self.assertEqual(
            average(
                [
                    {'number': 1},
                    {'number': 2},
                ],
                itemgetter('number'),
            ),
            1.5,
        )

