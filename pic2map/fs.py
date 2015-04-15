# -*- coding: utf-8 -*-
"""Filesystem functionality."""

import logging
import os

import exiftool
import magic

logger = logging.getLogger(__name__)

GPS_TAGS = [
    'EXIF:GPSDatestamp',
    'EXIF:GPSLatitude',
    'EXIF:GPSLatitudeRef',
    'EXIF:GPSLongitude',
    'EXIF:GPSLongitudeRef',
    'EXIF:GPSTimestamp',
]


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
        logger.debug(
            '%d picture files found under %s:\n%s',
            len(paths),
            self.directory,
            '\n'.join(os.path.relpath(path, self.directory)
                      for path in paths))

        valid_paths = filter_files_with_gps_data(paths)

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


def filter_files_with_gps_data(paths):
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
        # TBD: Validate metadata
    ]

    return valid_paths
