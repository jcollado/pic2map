===============================
Pic2Map
===============================

.. image:: https://img.shields.io/pypi/v/pic2map.svg
    :target: https://pypi.python.org/pypi/pic2map

.. image:: https://readthedocs.org/projects/pic2map/badge/?version=latest
    :target: https://readthedocs.org/projects/pic2map/?badge=latest
    :alt: Documentation Status

.. image:: https://landscape.io/github/jcollado/pic2map/master/landscape.svg?style=flat
    :target: https://landscape.io/github/jcollado/pic2map/master
    :alt: Code Health

.. image:: https://img.shields.io/travis/jcollado/pic2map.svg
    :target: https://travis-ci.org/jcollado/pic2map

.. image:: https://coveralls.io/repos/jcollado/pic2map/badge.svg
    :target: https://coveralls.io/r/jcollado/pic2map


Pic2Map is tool to gather GPS metadata from picture files and display it in a map.

* Free software: MIT license
* Documentation: https://pic2map.readthedocs.org.


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
