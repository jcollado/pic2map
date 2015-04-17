# -*- coding: utf-8 -*-
"""Test cases for the filesystem functionaliy in search."""
import os
import shutil
import tempfile
import unittest

from PIL import Image

from pic2map.fs import TreeExplorer


class TreeExplorerTest(unittest.TestCase):

    """Tree explorer test cases."""

    def setUp(self):
        """Initialize internal status needed for test case."""
        # Directory where test data should be created
        self.directory = tempfile.mkdtemp()
        self.picture_filenames = []

    def tearDown(self):
        """Remove files created for the test case."""
        shutil.rmtree(self.directory)

    def create_directory(self, directory, metadata):
        """Create directory of test data based on metadata.

        :param directory: Directory under which files should be created
        :type directory: str
        :param metadata: File names, types and subdirectories to create
        :type metadata: dict(str)

        """
        for basename, value in metadata.iteritems():
            if isinstance(value, str):
                filename = os.path.join(directory, basename)
                create_method = getattr(
                    self, 'create_{}_file'.format(value))
                create_method(filename)
            elif isinstance(value, dict):
                subdirectory = os.path.join(directory, basename)
                os.mkdir(subdirectory)
                self.create_directory(subdirectory, value)
            else:
                raise TypeError(
                    'Unexpected metadata. {}: {}'.format(basename, value))

    def create_text_file(self, filename):
        """Create text file using the given name.

        :param filename: Path to the file that should be created
        :type filename: str

        """
        with open(filename, 'w') as file_:
            file_.write('this is a text file')

    def create_picture_file(self, filename):
        """Create picture file using the given name.

        :param filename: Path to the file that should be created
        :type filename: str

        """
        picture = Image.new('RGB', (1, 1))
        picture.save(filename, 'JPEG')
        self.picture_filenames.append(filename)

    def create_broken_symlink_file(self, filename):
        """Create a broken symlink using the given name.

        :param filename: Path to the file that should be created
        :type filename: str

        """
        # Create symlink pointing to a temporary file
        # that will be removed after exiting from the context manager
        with tempfile.NamedTemporaryFile() as source_file:
            os.symlink(source_file.name, filename)

    def test_paths(self):
        """Picture files are found under the given directory."""
        metadata = {
            'a': 'text',
            'b': 'picture',
            'subdir': {
                'c': 'text',
                'd': 'picture',
                'subsubdir': {
                    'e': 'text',
                    'f': 'picture',
                }
            },
        }
        self.create_directory(self.directory, metadata)

        tree_explorer = TreeExplorer(self.directory)
        self.assertListEqual(
            sorted(tree_explorer.paths()),
            sorted(self.picture_filenames),
        )

    def test_broken_symlink(self):
        """Broken symbolic links are skipped while exploring directory."""
        metadata = {
            'a': 'broken_symlink',
            'b': 'picture',
        }

        self.create_directory(self.directory, metadata)

        tree_explorer = TreeExplorer(self.directory)
        self.assertListEqual(
            sorted(tree_explorer.paths()),
            sorted(self.picture_filenames),
        )
