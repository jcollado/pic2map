# -*- coding: utf-8 -*-
"""Command Line Interface test cases."""

import argparse
import os
import tempfile
import unittest

from mock import patch

from pic2map.cli import (
    add,
    parse_arguments,
    valid_directory,
)


class ValidDirectoryTest(unittest.TestCase):

    """Valid directory test cases."""

    def test_valid_directory(self):
        """Valid directory path."""
        temp_directory = tempfile.mkdtemp()
        try:
            self.assertTrue(
                valid_directory(temp_directory),
                temp_directory,
            )
        finally:
            os.rmdir(temp_directory)

    def test_invalid_directory(self):
        """Invalid directory."""
        with tempfile.NamedTemporaryFile() as temp_file:
            with self.assertRaises(argparse.ArgumentTypeError):
                valid_directory(temp_file.name)

    def test_unreadable_directory(self):
        """Unreadable diretory."""
        temp_directory = tempfile.mkdtemp()
        try:
            os.chmod(temp_directory, 0)
            with self.assertRaises(argparse.ArgumentTypeError):
                valid_directory(temp_directory)
        finally:
            os.rmdir(temp_directory)


class ParseArgumentsTest(unittest.TestCase):

    """Parse arguments test case."""

    def test_add_command(self):
        """Add command."""
        directory = 'some directory'
        with patch('pic2map.cli.valid_directory') as valid_directory_func:
            valid_directory_func.return_value = directory
            args = parse_arguments(['add', directory])
            self.assertEqual(args.directory, directory)
            self.assertEqual(args.func, add)
