import json
import os

from simphony_metaparser.nodes import VariableProperty
from simphony_metaparser.utils import traverse, without_cuba_prefix


ONTOLOGY_URI = "http://simphony"
ONTOLOGY_PREFIX = ONTOLOGY_URI+"#"
OWL_PREFIX = "http://www.w3.org/2002/07/owl#"
RDF_SCHEMA_PREFIX = "http://www.w3.org/2000/01/rdf-schema#"
XMLSCHEMA_PREFIX = "http://www.w3.org/2001/XMLSchema#"


class OWLJSONLDGenerator(object):
    """Creates a OWL representation of our data model in JSON-LD.
    """
    def generate(self, ontology, output_path, overwrite=False):

        if os.path.exists(output_path):
            if overwrite:
                try:
                    os.remove(output_path)
                except OSError:
                    pass
            else:
                raise OSError('Generated files already present. '
                              'Will not overwrite without --overwrite')

        onto = [
            {
                "@id": ONTOLOGY_PREFIX,
                "@type": OWL_PREFIX+"Ontology"
            }
        ]

        for item, _ in traverse(ontology.root_cuds_item):
            entry = {
                "@id": ONTOLOGY_PREFIX+without_cuba_prefix(item.name),
                "@type": OWL_PREFIX+"Class",
            }

            if item.parent is not None:
                entry[RDF_SCHEMA_PREFIX+"subClassOf"] = [
                    {
                        "@id": ONTOLOGY_PREFIX+without_cuba_prefix(
                            item.parent.name),
                    }
                ]
            for prop in item.properties.values():
                if prop.name == "definition":
                    entry[RDF_SCHEMA_PREFIX+"comment"] = prop.default

            onto.append(entry)

        datatype_properties, object_properties = \
            self._extract_properties(ontology)

        datatype_domain_range = {}
        for s, p, o in datatype_properties:
            datatype_domain_range.setdefault(p, []).append((s, o))

        for datatype in ontology.data_types:
            entry = {
                "@id": ONTOLOGY_PREFIX+without_cuba_prefix(datatype.name),
                "@type": OWL_PREFIX+"DatatypeProperty",
                RDF_SCHEMA_PREFIX+"comment": [{
                    "@value": datatype.definition
                }],
            }

            entry.setdefault(RDF_SCHEMA_PREFIX+"range", []).append(
                {
                    "@id": XMLSCHEMA_PREFIX+datatype.type
                }
            )

            onto.append(entry)

        for s, p, o in object_properties:
            entry = {
                "@id": ONTOLOGY_PREFIX+p,
                "@type": OWL_PREFIX+"ObjectProperty",
                RDF_SCHEMA_PREFIX+"range": [
                    {
                        "@id": ONTOLOGY_PREFIX+o
                    }
                ]
            }
            onto.append(entry)

        with open(output_path, "wb") as f:
            json.dump(onto, f, indent=4)

    def _extract_properties(self, ontology):
        """Extracts the datatype and object properties from our ontology

        Parameters
        ----------
        ontology : Ontology
            The ontology

        Returns
        -------
        datatype_properties, object_properties
            The properties, each as a list of triples subject property object.
        """
        data_types = {datatype.name: datatype
                      for datatype in ontology.data_types}

        datatype_properties = []
        object_properties = []

        for item, _ in traverse(ontology.root_cuds_item):
            for prop in [p for p in item.properties.values()
                         if isinstance(p, VariableProperty)]:
                if prop.name in data_types:
                    datatype_properties.append(
                        (without_cuba_prefix(item.name),
                         without_cuba_prefix(prop.name),
                         data_types[prop.name].type)
                    )
                else:
                    object_properties.append(
                        (without_cuba_prefix(item.name),
                         without_cuba_prefix(prop.name),
                         without_cuba_prefix(prop.name)))

        return datatype_properties, object_properties
