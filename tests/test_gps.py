# -*- coding: utf-8 -*-
"""GPS model and validation tests."""

import unittest

from voluptuous import Invalid

from pic2map.gps import SCHEMA


class SchemaTest(unittest.TestCase):

    """Schema validation test cases."""

    def test_valid_data(self):
        """Valid data with date/time stamp fields."""
        SCHEMA({
            'EXIF:GPSLatitude': 0,
            'EXIF:GPSLatitudeRef': 'N',
            'EXIF:GPSLongitude': 0,
            'EXIF:GPSLongitudeRef': 'E',
            'SourceFile': u'path',
            'EXIF:GPSDateStamp': u'1111:11:11',
            'EXIF:GPSTimeStamp': u'11:11:11',
        })

    def test_valid_data_no_timestamp(self):
        """Valid data without date/time stamp fields."""
        SCHEMA({
            'EXIF:GPSLatitude': 0,
            'EXIF:GPSLatitudeRef': 'N',
            'EXIF:GPSLongitude': 0,
            'EXIF:GPSLongitudeRef': 'E',
            'SourceFile': u'path',
        })

    def test_no_data(self):
        """No data."""
        with self.assertRaises(Invalid):
            SCHEMA({})
