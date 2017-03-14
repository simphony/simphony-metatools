from __future__ import print_function

import click

from simphony_metaparser.yamldirparser import YamlDirParser


@click.command()
@click.argument('yaml_dir', type=click.Path())
def cli(yaml_dir):
    """ Perform linting of the yaml dir.

    yaml_dir:
        path to the directory containing the yaml files.
    """

    parser = YamlDirParser()
    parser.parse(yaml_dir)
