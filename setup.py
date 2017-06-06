import os
import contextlib
from setuptools import setup, find_packages


# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()

# Setup version
VERSION = '0.1.0'


@contextlib.contextmanager
def cd(path):
    """Change directory and returns back to cwd once the operation is done."""
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def write_version_py(filename=None):
    if filename is None:
        filename = os.path.join(
            os.path.dirname(__file__), 'simphony_metatools', 'version.py')
    ver = """\
version = '%s'
"""
    fh = open(filename, 'wb')
    try:
        fh.write(ver % VERSION)
    finally:
        fh.close()


write_version_py()


# main setup configuration class
setup(
    name='simphony-metatools',
    version=VERSION,
    author='SimPhoNy, EU FP7 Project (Nr. 604005) www.simphony-project.eu',
    description='A set of tools to handle the simphony-metadata files',
    long_description=README_TEXT,
    install_requires=[
            "simphony_metaparser >= 0.2.0",
            "click >= 3.3",
            "yapf >= 0.16",
            "pyyaml >= 3.11",
            "six"
        ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            ('simphony-meta-generate = '
             'simphony_metatools.cli.generator:cli'),
            ('simphony-meta-linter = '
             'simphony_metatools.cli.linter:cli')
             ]},
    )
