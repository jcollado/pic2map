# -*- coding: utf-8 -*-
"""Test database functionality."""

import os
import shutil
import sqlite3
import tempfile
import unittest

from contextlib import closing
from datetime import datetime

from dateutil.tz import tzutc
from mock import patch

from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.types import (
    INTEGER,
    TEXT,
)


from pic2map.db import (
    Database,
    LocationDB,
    transform_metadata_to_row,
)


class DatabaseTest(unittest.TestCase):

    """Database wrapper test cases."""

    def test_get_table_metadata(self):
        """Table metadata can be retrieved using index notation."""
        with tempfile.NamedTemporaryFile() as db_file:
            with closing(sqlite3.connect(db_file.name)) as connection:
                with closing(connection.cursor()) as cursor:
                    cursor.execute(
                        'CREATE TABLE messages (id INTEGER, message TEXT)')

            database = Database(db_file.name)
            table = database['messages']
            schema = {column.name: type(column.type)
                      for column in table.columns}
            self.assertDictEqual(
                schema,
                {'id': INTEGER, 'message': TEXT})

    def test_get_unknown_table_metadata(self):
        """NoSuchTableError raised when table name is not found."""
        with tempfile.NamedTemporaryFile() as db_file:
            with closing(sqlite3.connect(db_file.name)) as connection:
                with closing(connection.cursor()) as cursor:
                    cursor.execute(
                        'CREATE TABLE messages (id INTEGER, message TEXT)')

            database = Database(db_file.name)

            with self.assertRaises(NoSuchTableError):
                database['unknown']

    def test_type_error_on_wrong_table_name(self):
        """TypeError raised when table name is not a string."""
        with tempfile.NamedTemporaryFile() as db_file:
            with closing(sqlite3.connect(db_file.name)) as connection:
                with closing(connection.cursor()) as cursor:
                    cursor.execute(
                        'CREATE TABLE messages (id INTEGER, message TEXT)')

            database = Database(db_file.name)

            with self.assertRaises(TypeError):
                database[0]

    def test_context_manager(self):
        """Connection is opened/closed when used as a context manager."""
        database = Database(':memory:')

        # Connection is None when database object is created
        self.assertIsNone(database.connection)

        with database:
            # Connection is not closed inside the context
            self.assertFalse(database.connection.closed)

        # Connection is closed outside the context
        self.assertTrue(database.connection.closed)


class LocationDBTest(unittest.TestCase):

    """Location database tests."""

    def setUp(self):
        """Create temporary directory."""
        self.directory = tempfile.mkdtemp()
        self.base_directory_patcher = patch('pic2map.db.BaseDirectory')
        base_directory = self.base_directory_patcher.start()
        base_directory.save_data_path.return_value = self.directory

    def tearDown(self):
        """Remove temporary directory."""
        self.base_directory_patcher.stop()
        shutil.rmtree(self.directory)

    def test_database_exists(self):
        """Database not create if exists."""
        filename = os.path.join(self.directory, 'location.db')
        with closing(sqlite3.connect(filename)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                    'CREATE TABLE location (column_1 TEXT, column_2 TEXT)')

        location_db = LocationDB()
        self.assertListEqual(
            location_db.location_table.columns.keys(),
            ['column_1', 'column_2'],
        )

    def test_create_database(self):
        """Create database file."""
        LocationDB()
        filename = os.path.join(self.directory, 'location.db')
        self.assertTrue(os.path.isfile(filename))

    def test_insert(self):
        """Insert records in database."""
        rows = [
            {
                'filename': 'a.jpg',
                'latitude': 1.2,
                'longitude': 2.1,
                'datetime': datetime(2015, 1, 1, 12, 34, 56)
            },
            {
                'filename': 'b.jpg',
                'latitude': 3.4,
                'longitude': 4.3,
                'datetime': datetime(2015, 1, 1, 12, 34, 56)
            },
        ]
        with LocationDB() as location_db:
            location_db.insert(rows)

        filename = os.path.join(self.directory, 'location.db')
        with closing(sqlite3.connect(filename)) as connection:
            with closing(connection.cursor()) as cursor:
                result = cursor.execute('SELECT COUNT(*) FROM location')
                self.assertListEqual(result.fetchall(), [(2,)])

    def test_select_all(self):
        """Select all rows from location table."""
        filename = os.path.join(self.directory, 'location.db')
        with closing(sqlite3.connect(filename)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                    'CREATE TABLE location (name TEXT)')
                cursor.execute(
                    'INSERT INTO location VALUES ("Hello world!")')
            connection.commit()

        with LocationDB() as location_db:
            result = location_db.select_all()
            rows = result.fetchall()
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertSequenceEqual(row, (u'Hello world!',))

    def test_remove(self):
        """Delete rows for files under a given directory."""
        file_count = 10

        filename = os.path.join(self.directory, 'location.db')
        with closing(sqlite3.connect(filename)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                    'CREATE TABLE location (filename TEXT)')

                for directory in ['a', 'b']:
                    for index in range(file_count):
                        cursor.execute(
                            'INSERT INTO location VALUES ("{}/{}.jpg")'
                            .format(directory, index))
            connection.commit()

        with LocationDB() as location_db:
            result = location_db.delete('a')
            self.assertEqual(result.rowcount, file_count)

    def test_count(self):
        """Count rows in database."""
        file_count = 10

        filename = os.path.join(self.directory, 'location.db')
        with closing(sqlite3.connect(filename)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                    'CREATE TABLE location (filename TEXT)')

                for index in range(file_count):
                    cursor.execute(
                        'INSERT INTO location VALUES ("{}.jpg")'.format(index))
            connection.commit()

        with LocationDB() as location_db:
            result = location_db.count()
            self.assertEqual(result, file_count)


class TransformMetadataToRowTest(unittest.TestCase):

    """EXIF metadata to database row transformation tests."""

    def test_transform_metadata(self):
        """Transform metadata to row."""
        metadata = {
            'SourceFile': 'a.jpg',
            'EXIF:GPSLatitude': 1.2,
            'EXIF:GPSLatitudeRef': 'N',
            'EXIF:GPSLongitude': 2.1,
            'EXIF:GPSLongitudeRef': 'E',
            'EXIF:GPSDateStamp': '2015:01:01',
            'EXIF:GPSTimeStamp': '12:34:56',
        }
        expected_row = {
            'filename': 'a.jpg',
            'latitude': 1.2,
            'longitude': 2.1,
            'datetime': datetime(2015, 1, 1, 12, 34, 56, tzinfo=tzutc()),
        }

        row = transform_metadata_to_row(metadata)
        self.assertEqual(row, expected_row)

    def test_transform_metadata_negative(self):
        """Transform metadata with negative latitude/longitude to row."""
        metadata = {
            'SourceFile': 'a.jpg',
            'EXIF:GPSLatitude': 1.2,
            'EXIF:GPSLatitudeRef': 'S',
            'EXIF:GPSLongitude': 2.1,
            'EXIF:GPSLongitudeRef': 'W',
            'EXIF:GPSDateStamp': '2015:01:01',
            'EXIF:GPSTimeStamp': '12:34:56',
        }
        expected_row = {
            'filename': 'a.jpg',
            'latitude': -1.2,
            'longitude': -2.1,
            'datetime': datetime(2015, 1, 1, 12, 34, 56, tzinfo=tzutc()),
        }

        row = transform_metadata_to_row(metadata)
        self.assertEqual(row, expected_row)

    def test_transform_metadata_no_datetime(self):
        """Transform metadata to row."""
        metadata = {
            'SourceFile': 'a.jpg',
            'EXIF:GPSLatitude': 1.2,
            'EXIF:GPSLatitudeRef': 'N',
            'EXIF:GPSLongitude': 2.1,
            'EXIF:GPSLongitudeRef': 'E',
        }
        expected_row = {
            'filename': 'a.jpg',
            'latitude': 1.2,
            'longitude': 2.1,
        }

        row = transform_metadata_to_row(metadata)
        self.assertEqual(row, expected_row)
