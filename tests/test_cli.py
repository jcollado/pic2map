# -*- coding: utf-8 -*-
"""Command Line Interface test cases."""

import argparse
import logging
import os
import tempfile
import unittest

from StringIO import StringIO

from mock import (
    MagicMock as Mock,
    patch,
)

from pic2map.cli import (
    add,
    count,
    main,
    parse_arguments,
    remove,
    serve,
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


class CommandFunctionTests(unittest.TestCase):

    """Command function test cases."""

    def setUp(self):
        """Patch dependencies."""
        self.tree_explorer_patcher = patch('pic2map.cli.TreeExplorer')
        self.tree_explorer_cls = self.tree_explorer_patcher.start()

        self.filter_gps_metadata_patcher = (
            patch('pic2map.cli.filter_gps_metadata'))
        self.filter_gps_metadata = self.filter_gps_metadata_patcher.start()

        self.transform_metadata_to_row_patcher = (
            patch('pic2map.cli.transform_metadata_to_row'))
        self.transform_metadata_to_row = (
            self.transform_metadata_to_row_patcher.start())

        self.location_db_patcher = patch('pic2map.cli.LocationDB')
        self.location_cls = self.location_db_patcher.start()


    def tearDown(self):
        """Undo the patching."""
        self.tree_explorer_patcher.stop()
        self.filter_gps_metadata_patcher.stop()
        self.transform_metadata_to_row_patcher.stop()
        self.location_db_patcher.stop()


    def test_add(self):
        """Add command function."""
        tree_explorer = self.tree_explorer_cls()
        paths = Mock()
        tree_explorer.paths.return_value = paths
        metadata_record = Mock()
        metadata_records = [metadata_record]
        self.filter_gps_metadata.return_value = metadata_records
        row = Mock()
        self.transform_metadata_to_row.return_value = row
        database = self.location_cls().__enter__()

        directory = 'some directory'
        args = argparse.Namespace(directory=directory)
        add(args)
        self.tree_explorer_cls.assert_called_with(directory)
        self.filter_gps_metadata.assert_called_once_with(paths)
        self.transform_metadata_to_row.assert_called_once_with(metadata_record)
        database.insert.assert_called_with([row])

    def test_remove(self):
        """Remove command function."""
        directory = 'some directory'
        args = argparse.Namespace(directory=directory)
        remove(args)
        database = self.location_cls().__enter__()
        database.delete.assert_called_once_with(directory)

    def test_count(self):
        """Count command function."""
        file_count = 10

        database = self.location_cls().__enter__()
        database.count.return_value = file_count

        args = argparse.Namespace()

        with patch('sys.stdout', new_callable=StringIO) as stdout:
            count(args)
            self.assertEqual(stdout.getvalue(), '{}\n'.format(file_count))

    def test_serve(self):
        """Serve command function."""
        args = argparse.Namespace()
        with patch('pic2map.cli.app') as app:
            serve(args)
            app.run.assert_called_once_with(debug=True)


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

    def test_remove(self):
        """Remove command."""
        directory = 'some directory'
        with patch('pic2map.cli.valid_directory') as valid_directory_func:
            valid_directory_func.return_value = directory
            args = parse_arguments(['remove', directory])
            self.assertEqual(args.directory, directory)
            self.assertEqual(args.func, remove)

    def test_count(self):
        """Count command."""
        args = parse_arguments(['count'])
        self.assertEqual(args.func, count)

    def test_serve_command(self):
        """Serve command."""
        args = parse_arguments(['serve'])
        self.assertEqual(args.func, serve)
