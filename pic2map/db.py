# -*- coding: utf-8 -*-
"""Location database."""

import logging
import os

import arrow

from sqlalchemy import (
    Column,
    MetaData,
    Table,
    create_engine,
    select,
)
from sqlalchemy.types import (
    DateTime,
    Float,
    String,
)
from xdg import BaseDirectory

logger = logging.getLogger(__name__)


class Database(object):

    """Generic database object.

    This class is subclassed to provide additional functionality specific to
    artifacts and/or documents.

    :param db_filename: Path to the sqlite database file
    :type db_filename: str

    """

    def __init__(self, db_filename):
        """Connect to database and create session object."""
        self.db_filename = db_filename
        self.engine = create_engine(
            'sqlite:///{}'.format(db_filename),
            connect_args={'check_same_thread': False},
        )
        self.connection = None
        self.metadata = MetaData(bind=self.engine)

    def connect(self):
        """Create connection."""
        logger.debug('Connecting to SQLite database: %r', self.db_filename)
        self.connection = self.engine.connect()

    def disconnect(self):
        """Close connection."""
        assert not self.connection.closed
        logger.debug(
            'Disconnecting from SQLite database: %r', self.db_filename)
        self.connection.close()

    def __enter__(self):
        """Connect on entering context."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Disconnect on exiting context."""
        self.disconnect()

    def __getitem__(self, table_name):
        """Get table object in database.

        :param table_name: Name of the table
        :type table_name: str
        :return: Table object that can be used in queries
        :rtype: sqlalchemy.schema.Table

        """
        if not isinstance(table_name, basestring):
            raise TypeError('Unexpected table name: {}'.format(table_name))
        table = self.metadata.tables.get(table_name)
        if table is None:
            table = Table(table_name, self.metadata, autoload=True)
        return table


class LocationDB(Database):

    """Location database.

    Store location information from picture files into a sqlite database.

    """

    def __init__(self):
        """Create database if needed."""
        base_directory = BaseDirectory.save_data_path('pic2map')
        db_filename = os.path.join(base_directory, 'location.db')
        Database.__init__(self, db_filename)

        if os.path.isfile(db_filename):
            self.location_table = self['location']
        else:
            logger.debug('Creating location database %r...', db_filename)

            self.location_table = Table(
                'location',
                self.metadata,
                Column('filename', String, unique=True),
                Column('latitude', Float),
                Column('longitude', Float),
                Column('datetime', DateTime),
            )
            self.location_table.create()

    def insert(self, rows):
        """Insert rows in location table.

        :param rows: Rows to be inserted in the database
        :type rows: list(dict(str))

        """
        insert_query = self.location_table.insert()
        result = self.connection.execute(insert_query, rows)
        logger.debug('%d rows inserted', result.rowcount)

    def select_all(self):
        """Get all rows from the location table.

        :returns: Location information rows
        :rtype: sqlalchemy.engine.result.ResultProxy

        """
        select_query = select([self.location_table])
        result = self.connection.execute(select_query)
        return result

    def delete(self, directory):
        """Delete rows with a filename under a given directory.

        :param directory: Directory to be used as prefix in the delete query
        :type directory: str

        """
        table = self.location_table
        delete_query = (
            table.delete()
            .where(table.c.filename.startswith(directory))
        )
        result = self.connection.execute(delete_query)
        logger.debug('%d rows deleted', result.rowcount)
        return result

    def count(self):
        """Get number of rows in the database.

        :return: Number of rows
        :rtype: int

        """
        select_query = self.location_table.count()
        result = self.connection.execute(select_query)
        return result.scalar()

def transform_metadata_to_row(metadata):
    """Transform GPS metadata in database rows.

    :param metadata: GPS metadata as returned by exiftool
    :type metadata: dict(str)
    :returns: Database row
    :rtype: dict(str)

    """
    new_metadata = {
        'filename': metadata['SourceFile'],
        'latitude': metadata['EXIF:GPSLatitude'],
        'longitude': metadata['EXIF:GPSLongitude'],
    }

    if metadata['EXIF:GPSLatitudeRef'] == u'S':
        new_metadata['latitude'] *= -1
    if metadata['EXIF:GPSLongitudeRef'] == u'W':
        new_metadata['longitude'] *= -1

    if ('EXIF:GPSDateStamp' in metadata and
            'EXIF:GPSTimeStamp' in metadata):
        datetime_str = u'{} {}'.format(
            metadata['EXIF:GPSDateStamp'],
            metadata['EXIF:GPSTimeStamp'],
        )

        new_metadata['datetime'] = arrow.get(
            datetime_str,
            ['YYYY:MM:DD HH:mm:ss.SSS', 'YYYY:MM:DD HH:mm:ss'],
        ).datetime

    return new_metadata
