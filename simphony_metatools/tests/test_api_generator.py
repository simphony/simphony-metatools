import unittest
from six import StringIO

from simphony_metatools.api_generator import APIGenerator
from simphony_metatools.tests import fixtures


class TestAPIGenerator(unittest.TestCase):
    def setUp(self):
        self.ontology = fixtures.trivial_ontology()

    def test_api_generator(self):
        generator = APIGenerator()

        output = StringIO()
        generator.generate(self.ontology, output)

        self.assertIn("from .cuds_root import CUDSRoot", output.getvalue())
