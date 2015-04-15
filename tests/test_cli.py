# -*- coding: utf-8 -*-
"""Command Line Interface test cases."""

import argparse
import logging
import os
import tempfile
import unittest

from mock import (
    MagicMock as Mock,
    patch,
)

from pic2map.cli import (
    add,
    main,
    parse_arguments,
    valid_directory,
)


class MainTests(unittest.TestCase):

    """Main function test cases."""

    def setUp(self):
        """Patch parse_arguments function."""
        self.parse_arguments_patcher = patch('pic2map.cli.parse_arguments')
        self.parse_arguments = self.parse_arguments_patcher.start()

        self.logging_patcher = patch('pic2map.cli.logging')
        self.logging_patcher.start()

    def test_func_called(self):
        """Command function is called."""
        argv = Mock()
        function = Mock()
        args = argparse.Namespace(
            log_level=logging.WARNING,
            func=function,
        )
        self.parse_arguments.return_value = args
        main(argv)
        function.assert_called_once_with(args)

    def tearDown(self):
        """Undo the patching."""
        self.parse_arguments_patcher.stop()
        self.logging_patcher.stop()


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
