from __future__ import print_function

import os
import json

from simphony_metatools.owl.owl_json_ld_generator import OWLJSONLDGenerator
from simphony_metatools.tests import fixtures
from simphony_metatools.tests.base_test_case import BaseTestCase


class TestOWLJSONLDGenerator(BaseTestCase):
    def setUp(self):
        super(TestOWLJSONLDGenerator, self).setUp()
        self.ontology = fixtures.trivial_ontology()
        self.complex_ontology = fixtures.complex_ontology()

    def test_basic_creation(self):
        generator = OWLJSONLDGenerator()

        output_path = os.path.join(self.tempdir, "owl.json")

        generator.generate(self.ontology, output_path)

        with open(output_path) as f:
            data = f.read()

        d = json.loads(data)
        expected = [
            {
                "@id": "http://simphony#",
                "@type": "http://www.w3.org/2002/07/owl#Ontology"
            },
            {
                "@id": "http://simphony#CUDS_ROOT",
                "@type": "http://www.w3.org/2002/07/owl#Class"
            },
            {
                "http://www.w3.org/2000/01/rdf-schema#subClassOf": [
                    {
                        "@id": "http://simphony#CUDS_ROOT"
                    }
                ],
                "@id": "http://simphony#CUDS_C1",
                "@type": "http://www.w3.org/2002/07/owl#Class"
            },
            {
                "http://www.w3.org/2000/01/rdf-schema#subClassOf": [
                    {
                        "@id": "http://simphony#CUDS_ROOT"
                    }
                ],
                "@id": "http://simphony#CUDS_C2",
                "@type": "http://www.w3.org/2002/07/owl#Class"
            },
            {
                "http://www.w3.org/2000/01/rdf-schema#range": [
                    {
                        "@id": "http://www.w3.org/2001/XMLSchema#string"
                    }
                ],
                "@id": "http://simphony#CUBA_DATA_ONE",
                "@type": "http://www.w3.org/2002/07/owl#DatatypeProperty",
                "http://www.w3.org/2000/01/rdf-schema#comment": [
                    {
                        "@value": ""
                    }
                ]
            },
            {
                "http://www.w3.org/2000/01/rdf-schema#range": [
                    {
                        "@id": "http://www.w3.org/2001/XMLSchema#string"
                    }
                ],
                "@id": "http://simphony#CUBA_DATA_TWO",
                "@type": "http://www.w3.org/2002/07/owl#DatatypeProperty",
                "http://www.w3.org/2000/01/rdf-schema#comment": [
                    {
                        "@value": ""
                    }
                ]
            }
        ]

        self.assertEqual(d, expected)

    def test_complex_ontology(self):
        generator = OWLJSONLDGenerator()
        output_path = os.path.join(self.tempdir, "owl.json")
        generator.generate(self.complex_ontology, output_path)

        with open(output_path) as f:
            data = f.read()

        d = json.loads(data)
        expected = [
            {
                "@id": "http://simphony#",
                "@type": "http://www.w3.org/2002/07/owl#Ontology"
            },
            {
                "@id": "http://simphony#CUDS_ITEM",
                "@type": "http://www.w3.org/2002/07/owl#Class"
            },
            {
                "http://www.w3.org/2000/01/rdf-schema#subClassOf": [
                    {
                        "@id": "http://simphony#CUDS_ITEM"
                    }
                ],
                "@id": "http://simphony#CUDS_COMPONENT",
                "@type": "http://www.w3.org/2002/07/owl#Class"
            },
            {
                "http://www.w3.org/2000/01/rdf-schema#subClassOf": [
                    {
                        "@id": "http://simphony#CUDS_COMPONENT"
                    }
                ],
                "@id": "http://simphony#PHYSICS_EQUATION",
                "@type": "http://www.w3.org/2002/07/owl#Class"
            },
            {
                "http://www.w3.org/2000/01/rdf-schema#subClassOf": [
                    {
                        "@id": "http://simphony#PHYSICS_EQUATION"
                    }
                ],
                "@id": "http://simphony#GRAVITY_MODEL",
                "@type": "http://www.w3.org/2002/07/owl#Class"
            },
            {
                "http://www.w3.org/2000/01/rdf-schema#range": [
                    {
                        "@id": "http://simphony#UID"
                    }
                ],
                "@id": "http://simphony#UID",
                "@type": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            {
                "http://www.w3.org/2000/01/rdf-schema#range": [
                    {
                        "@id": "http://simphony#NAME"
                    }
                ],
                "@id": "http://simphony#NAME",
                "@type": "http://www.w3.org/2002/07/owl#ObjectProperty"
            },
            {
                "http://www.w3.org/2000/01/rdf-schema#range": [
                    {
                        "@id": "http://simphony#ACCELERATION"
                    }
                ],
                "@id": "http://simphony#ACCELERATION",
                "@type": "http://www.w3.org/2002/07/owl#ObjectProperty"
            }
        ]

        self.assertEqual(d, expected)

    def test_overwrite(self):
        generator = OWLJSONLDGenerator()
        output_path = os.path.join(self.tempdir, "owl.json")
        with open(output_path, "w"):
            pass

        self.assertEqual(os.path.getsize(output_path), 0)

        with self.assertRaises(OSError):
            generator.generate(self.complex_ontology, output_path)

        generator.generate(self.complex_ontology, output_path, overwrite=True)

        self.assertNotEqual(os.path.getsize(output_path), 0)
