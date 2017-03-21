import os
import shutil

from simphony_metatools.python.api_generator import APIGenerator
from simphony_metatools.python.cuba_enum_generator import CUBAEnumGenerator
from simphony_metatools.python.keywords_generator import KeywordsGenerator
from simphony_metatools.python.meta_class_generator import MetaClassGenerator


class PythonGenerator(object):
    def generate(self, ontology, output_path, overwrite=False):
        """Generates python classes and files from the given ontology.

        Parameters
        ----------
        ontology: Ontology
            The ontology
        output_path: str
            a directory path where the various files will be created.
        overwrite: bool
            if the files are already present, set to True to overwrite.
            Otherwise, raises OSError.

        Raises
        ------
        OSError
            If the files are already present and overwrite is False
        """
        meta_class_output = os.path.join(output_path, "cuds", "meta")
        api_output = os.path.join(output_path, "cuds", "meta", "api.py")
        keyword_output = os.path.join(output_path, "core", "keywords.py")
        cuba_output = os.path.join(output_path, "core", "cuba.py")

        if any([os.path.exists(x) for x in [
            meta_class_output, keyword_output, cuba_output]
                ]):
            if overwrite:
                try:
                    shutil.rmtree(meta_class_output)
                except OSError:
                    pass
                try:
                    os.remove(keyword_output)
                except OSError:
                    pass
                try:
                    os.remove(cuba_output)
                except OSError:
                    pass
            else:
                raise OSError('Generated files already present. '
                              'Will not overwrite without --overwrite')

        try:
            os.mkdir(meta_class_output)
        except OSError:
            pass

        generator = KeywordsGenerator()
        with open(keyword_output, "wb") as f:
            generator.generate(ontology, f)

        generator = CUBAEnumGenerator()
        with open(cuba_output, "wb") as f:
            generator.generate(ontology, f)

        meta_class_generator = MetaClassGenerator()
        meta_class_generator.generate(ontology, meta_class_output)

        api_generator = APIGenerator()
        with open(api_output, "wb") as f:
            api_generator.generate(ontology, f)
