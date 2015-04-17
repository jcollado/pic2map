# -*- coding: utf-8 -*-
"""Command Line Interface."""

import argparse
import logging
import os
import sys

from pic2map.db import LocationDB
from pic2map.fs import TreeExplorer
from pic2map.gps import filter_gps_metadata


logger = logging.getLogger(__name__)


def main(argv):
    """Entry point for the pic2map.py script."""
    args = parse_arguments(argv)
    configure_logging(args.log_level)
    args.func(args)


def add(args):
    """Add images from a directory to the map."""
    logger.info('Adding image files from %r...', args.directory)
    tree_explorer = TreeExplorer(args.directory)
    paths = tree_explorer.paths()

    gps_metadata_records = filter_gps_metadata(paths)
    logger.info(
        '%d picture files with GPS metadata found under %s',
        len(gps_metadata_records),
        args.directory)


def valid_directory(path):
    """Directory validation."""
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(
            '{!r} is not a valid directory'.format(path))

    if not os.access(path, os.R_OK | os.X_OK):
        raise argparse.ArgumentTypeError(
            'not enough permissions to explore {!r}'.format(path))

    return path


def configure_logging(log_level):
    """Configure logging based on command line argument.

    :param log_level: Log level passed form the command line
    :type log_level: int

    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Log to sys.stderr using log level
    # passed through command line
    log_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    log_handler.setFormatter(formatter)
    log_handler.setLevel(log_level)
    root_logger.addHandler(log_handler)


def parse_arguments(argv):
    """Parse command line arguments.

    :returns: Parsed arguments
    :rtype: argparse.Namespace

    """
    parser = argparse.ArgumentParser(
        description='Display pictures location in a map')
    log_levels = ['debug', 'info', 'warning', 'error', 'critical']
    parser.add_argument(
        '-l', '--log-level',
        dest='log_level',
        choices=log_levels,
        default='warning',
        help=('Log level. One of {0} or {1} '
              '(%(default)s by default)'
              .format(', '.join(log_levels[:-1]), log_levels[-1])))

    subparsers = parser.add_subparsers(help='Subcommands')

    add_parser = subparsers.add_parser(
        'add', help='Add images')
    add_parser.add_argument(
        'directory', type=valid_directory, help='Base directory')
    add_parser.set_defaults(func=add)

    args = parser.parse_args(argv)
    args.log_level = getattr(logging, args.log_level.upper())
    return args

if __name__ == '__main__':
    main(sys.argv[1:])
