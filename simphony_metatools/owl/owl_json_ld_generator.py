import json

from simphony_metaparser.nodes import VariableProperty
from simphony_metaparser.utils import traverse, without_cuba_prefix


ONTOLOGY_URI = "http://simphony"
ONTOLOGY_PREFIX = ONTOLOGY_URI+"#"
OWL_PREFIX = "http://www.w3.org/2002/07/owl#"
RDF_SCHEMA_PREFIX = "http://www.w3.org/2000/01/rdf-schema#"
XMLSCHEMA_PREFIX = "http://www.w3.org/2001/XMLSchema#"


class OWLJSONLDGenerator():
    """Creates a OWL representation of our data model in JSON-LD.
    """
    def generate(self, ontology, output_path, overwrite=False):
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

        for datatype in ontology.data_types:
            entry = {
                "@id": ONTOLOGY_PREFIX+without_cuba_prefix(datatype.name),
                "@type": OWL_PREFIX+"DatatypeProperty",
                RDF_SCHEMA_PREFIX+"range": [
                    {
                        "@id": XMLSCHEMA_PREFIX+str(datatype.type)
                    }
                ],
                RDF_SCHEMA_PREFIX+"comment": [{
                    "@value": datatype.definition
                }],

            }
            onto.append(entry)

        for s, p, o in self.extract_object_properties(ontology):
            entry = {
                "@id": ONTOLOGY_PREFIX+p,
                "@type": OWL_PREFIX+"ObjectProperty",
                RDF_SCHEMA_PREFIX+"domain": [
                     {
                        "@id": ONTOLOGY_PREFIX+s
                    }
                  ],
                RDF_SCHEMA_PREFIX+"range": [
                    {
                        "@id": ONTOLOGY_PREFIX+o
                    }
                ]
            }
            onto.append(entry)

        with open(output_path, "wb") as f:
            json.dump(onto, f, indent=4)

    def extract_object_properties(self, ontology):
        """Extracts the object properties, skipping the datatype properties,
        from our ontology"""
        data_types = [datatype.name for datatype in ontology.data_types]
        object_properties = []
        for item, _ in traverse(ontology.root_cuds_item):
            for prop in [p for p in item.properties.values()
                         if isinstance(p, VariableProperty)]:
                if prop.name not in data_types:
                    object_properties.append(
                        (without_cuba_prefix(item.name),
                         without_cuba_prefix(prop.name),
                         without_cuba_prefix(prop.name)))

        return object_properties
