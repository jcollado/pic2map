# -*- coding: utf-8 -*-
"""Utility functionality."""

def average(collection, function=None):
    """Calculate the average of values in a collection.

    :param collection: The collection with the data to be averaged
    :type collection: list | iterator
    :param function:
        Function used to retrieve data from each element. If not passed an
        identity function will be used by default.
    :type function: callable

    """
    if function is None:
        function = lambda x: x

    total = float(sum(function(element) for element in collection))
    return total / len(collection)
