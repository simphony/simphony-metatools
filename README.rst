Simphony-metatools
==================

The native implementation of the SimPhoNy cuds objects and io code (http://www.simphony-project.eu/).
Provides two utilities:

- A YAML to python generator, used in simphony-common
- A linter that reports parsing or semantic errors in the YAML files.

Installation
------------

The package requires python 2.7.x, installation is based on setuptools::

    # build and install
    python setup.py install

or::

    # build for in-place development
    python setup.py develop

Testing
-------

To run the full test-suite run::

    python -m unittest discover -p test*

