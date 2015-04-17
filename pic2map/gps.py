# -*- coding: utf-8 -*-
"""GPS data model and validation."""
import logging

import exiftool

from voluptuous import (
    All,
    Any,
    Invalid,
    Match,
    Range,
    Required,
    Schema,
)

logger = logging.getLogger(__name__)

# Interesting tags with GPS information
TAGS = [
    'EXIF:GPSDateStamp',
    'EXIF:GPSLatitude',
    'EXIF:GPSLatitudeRef',
    'EXIF:GPSLongitude',
    'EXIF:GPSLongitudeRef',
    'EXIF:GPSTimeStamp',
]

POSITIVE_NUMBER = All(Any(int, float), Range(min=0))

SCHEMA = Schema({
    Required('EXIF:GPSLatitude'): POSITIVE_NUMBER,
    Required('EXIF:GPSLatitudeRef'): Any(u'N', u'S'),
    Required('EXIF:GPSLongitude'): POSITIVE_NUMBER,
    Required('EXIF:GPSLongitudeRef'): Any(u'E', u'W'),
    Required('SourceFile'): unicode,
    'EXIF:GPSDateStamp': All(unicode, Match(r'\d{4}:\d{2}:\d{2}')),
    'EXIF:GPSTimeStamp': All(unicode, Match(r'\d{2}:\d{2}:\d{2}')),
})


def validate_gps_metadata(exif_metadata):
    """Validate GPS metadata using a schema.

    :param exif_metadata: Metadata to be validated
    :type exif_metadata: dict(str)
    :returns: Whether GPS metadata was found or not
    :rtype: bool

    """
    try:
        SCHEMA(exif_metadata)
    except Invalid as exception:
        logger.debug(
            'No GPS metadata found:\n%s\n%s', exif_metadata, exception)
        return False

    return True


def filter_gps_metadata(paths):
    """Filter out metadata records that don't have GPS information.

    :param paths: Picture filenames to get metadata from
    :type paths: list(str)
    :returns: Picture files with GPS data
    :rtype: list(dict(str))

    """
    with exiftool.ExifTool() as tool:
        metadata_records = tool.get_tags_batch(TAGS, paths)

    gps_metadata_records = [
        metadata_record
        for metadata_record in metadata_records
        if validate_gps_metadata(metadata_record)
    ]

    return gps_metadata_records
