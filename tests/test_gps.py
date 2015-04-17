# -*- coding: utf-8 -*-
"""GPS model and validation tests."""

import unittest

from mock import (
    MagicMock as Mock,
    patch,
)

from pic2map.gps import (
    filter_gps_metadata,
    validate_gps_metadata,
)

VALID_METADATA = {
    'EXIF:GPSLatitude': 0,
    'EXIF:GPSLatitudeRef': 'N',
    'EXIF:GPSLongitude': 0,
    'EXIF:GPSLongitudeRef': 'E',
    'SourceFile': u'path',
    'EXIF:GPSDateStamp': u'1111:11:11',
    'EXIF:GPSTimeStamp': u'11:11:11',
}

VALID_METADATA_NO_DATETIME ={
    'EXIF:GPSLatitude': 0,
    'EXIF:GPSLatitudeRef': 'N',
    'EXIF:GPSLongitude': 0,
    'EXIF:GPSLongitudeRef': 'E',
    'SourceFile': u'path',
}

INVALID_METADATA = {}


class ValidateGPSMetadataTest(unittest.TestCase):

    """GPS metadata validation test cases."""

    def test_valid_data(self):
        """Valid data with date/time stamp fields."""
        self.assertTrue(validate_gps_metadata(VALID_METADATA))

    def test_valid_data_no_datetime(self):
        """Valid data without date/time stamp fields."""
        self.assertTrue(validate_gps_metadata(VALID_METADATA_NO_DATETIME))

    def test_no_data(self):
        """No data."""
        self.assertFalse(validate_gps_metadata(INVALID_METADATA))


class FilterGPSMetadataTest(unittest.TestCase):

    """GPS metadata filtering test cases."""

    def test_filter_metadata(self):
        """Filter out pictures without GPS information."""
        with patch('pic2map.gps.exiftool') as exiftool:
            tool = exiftool.ExifTool().__enter__()
            tool.get_tags_batch.return_value = [
                VALID_METADATA,
                VALID_METADATA_NO_DATETIME,
                INVALID_METADATA,
            ]

            paths = Mock()
            metadata_records = filter_gps_metadata(paths)
            self.assertListEqual(
                metadata_records,
                [VALID_METADATA, VALID_METADATA_NO_DATETIME],
            )
