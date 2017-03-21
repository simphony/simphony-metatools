from six import StringIO

from simphony_metatools.python.keywords_generator import KeywordsGenerator
from simphony_metatools.tests import fixtures
from simphony_metatools.tests.base_test_case import BaseTestCase


class TestKeywordsGenerator(BaseTestCase):
    def setUp(self):
        self.ontology = fixtures.trivial_ontology()

    def test_generation(self):
        generator = KeywordsGenerator()
        output = StringIO()

        generator.generate(self.ontology, output)

        self.assertTextEqual(fixtures.trivial_ontology_keywords_output(),
                             output.getvalue())
