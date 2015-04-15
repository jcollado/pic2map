# -*- coding: utf-8 -*-
"""Filesystem functionality."""

import logging
import os

import exiftool
import magic

from voluptuous import (
    All,
    Any,
    Invalid,
    Length,
    Required,
    Schema,
)

logger = logging.getLogger(__name__)

GPS_TAGS = [
    'EXIF:GPSDateStamp',
    'EXIF:GPSLatitude',
    'EXIF:GPSLatitudeRef',
    'EXIF:GPSLongitude',
    'EXIF:GPSLongitudeRef',
    'EXIF:GPSTimeStamp',
]

character = All(unicode, Length(min=1, max=1))

GPS_SCHEMA = Schema({
    Required('EXIF:GPSLatitude'): Any(int, float),
    Required('EXIF:GPSLatitudeRef'): character,
    Required('EXIF:GPSLongitude'): Any(int, float),
    Required('EXIF:GPSLongitudeRef'): character,
    Required('SourceFile'): unicode,
    'EXIF:GPSDateStamp': unicode,
    'EXIF:GPSTimeStamp': unicode,
})


class TreeExplorer(object):

    """Look for image files in a tree and return them.

    :param directory: Base directory for the tree to be explored.
    :type directory: str

    """

    def __init__(self, directory):
        """Initialize tree explorer."""
        self.directory = directory

    def paths(self):
        """Return paths to picture files found under directory.

        :return: Paths to picture files
        :rtype: list(str)

        """
        paths = self._explore()
        logger.info(
            '%d picture files found under %s',
            len(paths),
            self.directory)

        valid_paths = filter_files_with_gps_metadata(paths)
        logger.info(
            '%d picture files with GPS metadata found under %s',
            len(valid_paths),
            self.directory)

        return valid_paths

    def _explore(self):
        """Walk from base directory and return files that match pattern.

        :returns: Image files found under directory
        :rtype: list(str)

        """
        paths = []
        for (dirpath, _dirnames, filenames) in os.walk(self.directory):
            logger.debug('Exploring %s...', dirpath)

            # Check if any filename is a picture file
            for filename in filenames:
                path = os.path.join(dirpath, filename)

                # Skip missing files like broken symbolic links
                if not os.path.isfile(path):
                    logger.warning('Unable to access file: %r', path)
                    continue

                if 'JPEG image data' in magic.from_file(path):
                    paths.append(path)

        return paths


def validate_gps_metadata(exif_metadata):
    """Validate GPS metadata using a schema.

    :param exif_metadata: Metadata to be validated
    :type exif_metadata: dict(str)
    :returns: Whether GPS metadata was found or not
    :rtype: bool

    """
    try:
        GPS_SCHEMA(exif_metadata)
    except Invalid as exception:
        logging.debug(
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
            GPS_TAGS,
            paths,
        )

    valid_paths = [
        path
        for path, exif_metadata in zip(paths, exif_metadata_paths)
        if validate_gps_metadata(exif_metadata)
    ]

    return valid_paths
