# -*- coding: utf-8 -*-
"""Location database."""

import logging
import os

from sqlalchemy import (
    MetaData,
    Table,
    create_engine,
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

        if not os.path.isfile(db_filename):
            logger.debug('Creating location database %r...', db_filename)
