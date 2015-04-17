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


def filter_files_with_gps_metadata(paths):
    """Filter paths that don't have GPS data.

    :param paths: Picture filenames to be filtered.
    :type paths: list(str)
    :returns: Picture files with GPS data
    :rtype: dict(str)

    """
    with exiftool.ExifTool() as tool:
        exif_metadata_paths = tool.get_tags_batch(
            TAGS,
            paths,
        )

    valid_paths = [
        path
        for path, exif_metadata in zip(paths, exif_metadata_paths)
        if validate_gps_metadata(exif_metadata)
    ]

    return valid_paths
