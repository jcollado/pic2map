===============================
Pic2Map
===============================

.. image:: https://img.shields.io/pypi/l/pic2map.svg
    :target: https://pypi.python.org/pypi/pic2map/
    :alt: License

.. image:: https://img.shields.io/pypi/v/pic2map.svg
    :target: https://pypi.python.org/pypi/pic2map

.. image:: https://readthedocs.org/projects/pic2map/badge/?version=latest
    :target: http://pic2map.readthedocs.org/en/latest/
    :alt: Documentation

.. image:: https://requires.io/github/jcollado/pic2map/requirements.svg?branch=master
    :target: https://requires.io/github/jcollado/pic2map/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://landscape.io/github/jcollado/pic2map/master/landscape.svg?style=flat
    :target: https://landscape.io/github/jcollado/pic2map/master
    :alt: Code Health

.. image:: https://img.shields.io/travis/jcollado/pic2map.svg
    :target: https://travis-ci.org/jcollado/pic2map

.. image:: https://coveralls.io/repos/jcollado/pic2map/badge.svg
    :target: https://coveralls.io/r/jcollado/pic2map

.. image:: https://badge.waffle.io/jcollado/pic2map.svg?label=ready&title=Ready
    :target: https://waffle.io/jcollado/pic2map
    :alt: 'Stories in Ready'

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/jcollado/pic2map
   :target: https://gitter.im/jcollado/pic2map?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. image:: http://unmaintained.tech/badge.svg
   :alt: No Maintenance Intended
   :target: http://unmaintained.tech/


Pic2Map is tool to gather GPS metadata from picture files and display it in a map.


Features
--------

* Add location information for pictures under directory to database

.. code-block:: bash

    pic2map add <directory>

* Remove location information for pictures under directory from database

.. code-block:: bash

    pic2map remove <directory>

* Count how many files have been indexed

.. code-block:: bash

    pic2map count

* Launch web server to display map and a marker for each picture

.. code-block:: bash

    pic2map serve
