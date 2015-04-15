# -*- coding: utf-8 -*-
"""Command Line Interface."""

import argparse
import sys

def main(argv):
    """Entry point for the pic2map.py script."""
    args = parse_arguments(argv)
    print args

def parse_arguments(argv):
    """Parse command line arguments.

    :returns: Parsed arguments
    :rtype: argparse.Namespace

    """
    parser = argparse.ArgumentParser(
        description='Display pictures location in a map')
    args = parser.parse_args(argv)
    return args

if __name__ == '__main__':
    main(sys.argv[1:])
