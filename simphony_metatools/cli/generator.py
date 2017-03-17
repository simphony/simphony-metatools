from __future__ import print_function

import click

from simphony_metaparser.yamldirparser import YamlDirParser
from simphony_metatools.python.python_generator import PythonGenerator
from simphony_metatools.owl.owl_json_ld_generator import OWLJSONLDGenerator


@click.command()
@click.argument('yaml_dir', type=click.Path())
@click.argument('output_path', type=click.Path())
@click.option('-f', '--format', default="python")
@click.option('-O', '--overwrite', is_flag=True, default=False,
              help='Overwrite OUT_PATH')
def cli(yaml_dir, output_path, format, overwrite):
    """ Create the Simphony Metadata classes

    yaml_file:
        path to the simphony_metadata yaml file

    module_root_path:
        path to the root directory of the simphony module.
        Output files will be placed in the appropriate locations
        under this module.

    overwrite:
        Allow overwrite of the file.
    """

    parser = YamlDirParser()
    ontology = parser.parse(yaml_dir)

    if format == "python":
        generator = PythonGenerator()
    elif format == "owl-jsonld":
        generator = OWLJSONLDGenerator()
    else:
        raise click.BadOptionUsage("Supported output formats: "
                                   "python, owl-jsonld")

    generator.generate(ontology, output_path, overwrite=overwrite)
