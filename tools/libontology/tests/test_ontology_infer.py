# Copyright (c) 2023-2025 Orange. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#     1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#     3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
#     This product includes software developed by Orange.
#     4. Neither the name of Orange nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Orange "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Orange BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Test module for ontology inference functionality.

This module contains unit tests for different inference engines
(Hermit, Pellet, OWLRL) and their results.

Classes
-------
TestOntologyInfer
    Test cases for inference operations.

Functions
---------
replace_blank_nodes(ontology_path: str, namespace: str)
    Replaces blank node identifiers with deterministic IDs.
remove_blank_nodes(graph: Graph) -> Graph
    Removes blank nodes from a graph for comparison.

Test Cases
----------
test_infer_hermit
    Tests Hermit reasoner inference.
test_infer_pellet
    Tests Pellet reasoner inference.
test_infer_owlrl
    Tests OWLRL reasoner inference.
"""

import unittest
import tempfile
import re
import io
import os
from libontology.ontology_infer import (
    OntologyInferHermit,
    OntologyInferPellet,
    OntologyInferOwlrl,
)
from libontology.ontology_convert import OntologyConverter
from rdflib import Graph


def replace_blank_nodes(ontology_path, namespace):
    """A method to replace blank nodes for comparing owlrl results."""
    with open(ontology_path, "r", encoding='utf-8') as ontology_file:
        content = ontology_file.read()

    # Find blank nodes
    pattern = r"n[a-z0-9]{33,}\d"
    nodes = set(re.findall(pattern, content))

    # Replace blank node's name
    counter = 1
    for node in nodes:
        content = content.replace(node, f"{namespace}node_{counter}")
        counter += 1

    # Save changes
    with open(ontology_path, "w", encoding='utf-8') as ontology_file:
        ontology_file.write(content)


def remove_blank_nodes(graph):
    """A method to remove blank nodes for comparing owlrl results."""
    new_graph = Graph()
    pattern = r"n[a-z0-9]{33,}\d"

    # Keep only non-blank nodes
    for s, p, o in graph:
        if not (re.match(pattern, str(s)) or re.match(pattern, str(o))):
            new_graph.add((s, p, o))

    return new_graph


class TestOntologyInfer(unittest.TestCase):
    """
    A class to test the `OntologyInfer` class for performing inference.

    Methods
    -------
    setUp()
        Initializes paths for test ontologies.
    test_infer_hermit()
        Tests to perform inference on an ontology by using hermit reasoner.
    test_infer_hermit_in_memory()
        Tests to perform inference on an ontology by using hermit reasoner.
    test_infer_pellet()
        Tests to perform inference on an ontology by using pellet reasoner.
    test_infer_owlrl()
        Tests to perform inference on an ontology by using owlrl reasoner.
    """
    def setUp(self):
        """
        Set up test paths for ontology.
        """
        self.ontology_path = "./tests/test_infer/test_onto.ttl"
        self.ontology_infer_hermit_path = (
            "./tests/test_infer/test_onto_infer_hermit.ttl"
        )
        self.ontology_infer_pellet_path = (
            "./tests/test_infer/test_onto_infer_pellet.ttl"
        )
        self.ontology_infer_owlrl_path = (
            "./tests/test_infer/test_onto_infer_owlrl.ttl"
        )

    def test_infer_hermit(self):
        """
        Test to perform inference using hermit reasoner.

        Ensures that the `OntologyInferHermit` class correctly performs inference
        and that the output matches the expected result.
        """
        # Path for the temporary file where onto_infer will be saved
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".ttl").name

        # Paths where we'll save temporary XML prior/post convert files
        with (
            tempfile.NamedTemporaryFile(delete=True, suffix=".xml") as temp_source,
            tempfile.NamedTemporaryFile(delete=True, suffix=".xml") as temp_destination,
        ):

            temp_source_xml_path = temp_source.name
            temp_destination_xml_path = temp_destination.name

            ontology_converter = OntologyConverter(self.ontology_path)
            ontology_converter.convert(temp_source_xml_path, "xml")

            ontology_infer = OntologyInferHermit(temp_source_xml_path)
            ontology_infer.perform_inference(destination=temp_destination_xml_path)

            ontology_converter = OntologyConverter(temp_destination_xml_path)
            ontology_converter.convert(temp_path, "turtle")

            # Parsing the two graphs for comparison
            graph_valid = Graph()
            graph_test = Graph()
            graph_valid.parse(self.ontology_infer_hermit_path, format="turtle")
            graph_test.parse(temp_path, format="turtle")

            try:
                os.remove(temp_path)
            except FileNotFoundError:
                print(f"File '{temp_path}' not found.")
            self.assertTrue(graph_test.isomorphic(graph_valid))

    def test_infer_hermit_in_memory(self):
        """
        Test to perform inference using hermit reasoner.

        Ensures that the `OntologyInferHermit` class correctly performs inference
        by using in memory objects and that the output matches the expected result.
        """
        with tempfile.NamedTemporaryFile(delete=True, suffix=".xml") as temp_source:
            temp_source_xml_path = temp_source.name

            ontology_converter = OntologyConverter(self.ontology_path)
            ontology_converter.convert(temp_source_xml_path, "xml")

            ontology_infer = OntologyInferHermit(temp_source_xml_path)
            inference_bytes = io.BytesIO()
            ontology_infer.perform_inference(destination=inference_bytes)
            inference_content = inference_bytes.getvalue()

            inference_graph = Graph()
            inference_graph.parse(data=inference_content, format="xml")

            # Loading the reference graph for comparison
            graph_valid = Graph()
            graph_valid.parse(self.ontology_infer_hermit_path, format="turtle")

            # Check for graph isomorphism
            self.assertTrue(inference_graph.isomorphic(graph_valid))

    def test_infer_pellet(self):
        """
        Test to perform inference using pellet reasoner.

        Ensures that the `OntologyInferPellet` class correctly performs inference
        and that the output matches the expected result.
        """
        # Path for the temporary file where onto_infer will be saved
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".ttl").name

        # Paths where we'll save temporary XML prior/post convert files
        with (
            tempfile.NamedTemporaryFile(delete=True, suffix=".xml") as temp_source,
            tempfile.NamedTemporaryFile(delete=True, suffix=".xml") as temp_destination,
        ):

            temp_source_xml_path = temp_source.name
            temp_destination_xml_path = temp_destination.name

            ontology_converter = OntologyConverter(self.ontology_path)
            ontology_converter.convert(temp_source_xml_path, "xml")

            ontology_infer = OntologyInferPellet(temp_source_xml_path)
            ontology_infer.perform_inference(destination=temp_destination_xml_path)

            ontology_converter = OntologyConverter(temp_destination_xml_path)
            ontology_converter.convert(temp_path, "turtle")

            # Parsing the two graphs for comparison
            graph_valid = Graph()
            graph_test = Graph()
            graph_valid.parse(self.ontology_infer_pellet_path, format="turtle")
            graph_test.parse(temp_path, format="turtle")

            try:
                os.remove(temp_path)
            except FileNotFoundError:
                print(f"File '{temp_path}' not found.")
            self.assertTrue(graph_test.isomorphic(graph_valid))

    def test_infer_owlrl(self):
        """
        Test to perform inference using owlrl reasoner.

        Ensures that the `OntologyInferOwlrl` class correctly performs inference
        and that the output matches the expected result.
        """
        # Path for the temporary file where onto_infer will be saved
        temp_path = "./tests/test_infer/temp_file.ttl"

        # Paths where we'll save temporary XML prior/post convert files
        with (
            tempfile.NamedTemporaryFile(delete=True, suffix=".xml") as temp_source,
            tempfile.NamedTemporaryFile(delete=True, suffix=".xml") as temp_destination,
        ):

            temp_source_xml_path = temp_source.name
            temp_destination_xml_path = temp_destination.name

            ontology_converter = OntologyConverter(self.ontology_path)
            ontology_converter.convert(temp_source_xml_path, "xml")

            ontology_infer = OntologyInferOwlrl(temp_source_xml_path)
            ontology_infer.perform_inference(destination=temp_destination_xml_path)

            ontology_converter = OntologyConverter(temp_destination_xml_path)
            ontology_converter.convert(temp_path, "turtle")

            # Parsing the two graphs for comparison
            graph_valid = Graph()
            graph_test = Graph()
            graph_valid.parse(self.ontology_infer_owlrl_path, format="turtle")
            graph_test.parse(temp_path, format="turtle")

            graph_valid_without_blank_nodes = remove_blank_nodes(graph_valid)
            graph_test_without_blank_nodes = remove_blank_nodes(graph_test)

            try:
                os.remove(temp_path)
            except FileNotFoundError:
                print(f"File '{temp_path}' not found.")
            self.assertTrue(
                graph_test_without_blank_nodes.isomorphic(
                    graph_valid_without_blank_nodes
                )
            )


if __name__ == "__main__":
    unittest.main()
