========
Overview
========



A class based view for Django that can act as an receiver for GitHub webhooks. It is designed to validate all requests through their ``X-Hub-Signature``
headers.

Handling of GitHub events is done by implementing a class method with the same name as the event, e.g. ``ping``, ``push`` or ``fork``. See the documentation for
more in-depth information and examples.

* Free software: BSD license

Installation
============

::

    pip install django-github-webhook

Documentation
=============

https://django-github-webhook.readthedocs.org/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

0.1.0 (2016-01-29)
-----------------------------------------

* First release on PyPI.


