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
Test module for ontology format conversion functionality.

This module contains unit tests for converting ontologies between
different formats (Turtle, RDF/XML, etc.).

Classes
-------
TestOntologyConverter
    Test cases for format conversion operations.

Functions
---------
get_sha256_hash(file_path: str) -> str
    Calculates SHA256 hash of a file for comparison.

Test Cases
----------
test_convert
    Tests conversion between different ontology formats.
"""

import unittest
import hashlib
from rdflib import Graph
from libontology.ontology_convert import OntologyConverter


def get_sha256_hash(file_path):
    """Computes the SHA256 hash of a fil."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update the hash as 4K blocks
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


class TestOntologyConverter(unittest.TestCase):
    """
    A class to test the `OntologyConverter` class converting an ontology.

    Methods
    -------
    setUp()
        Initializes paths for test ontologies.
    test_convert()
        Tests to convert an ontology and verifies the resulting ontology.
    """
    def setUp(self):
        """
        Set up test paths for ontology.
        """
        self.source_ttl_path = "./tests/test_convert/test_onto.ttl"
        self.destination_xml_path = "/tmp/test_destination.xml"
        self.source_xml_path = "./tests/test_convert/test_onto.xml"
        self.destination_ttl_path = "/tmp/test_destination.ttl"

    def test_convert_ttl_to_xml(self):
        """
        Test a turtle to xml convertion.

        Ensures that the `OntologyConvert` class correctly converts a turtle
        ontology to an xml's one.
        """
        ontology_converter = OntologyConverter(self.source_ttl_path)
        ontology_converter.convert(self.destination_xml_path, "xml")

        # Parsing the two graphs for comparison
        graph_valid = Graph()
        graph_test = Graph()
        graph_valid.parse(self.source_ttl_path, format="ttl")
        graph_test.parse(self.destination_xml_path, format="xml")

        self.assertTrue(graph_test.isomorphic(graph_valid))

    def test_convert_xml_to_ttl(self):
        """
        Test a xml to turtle convertion.

        Ensures that the `OntologyConvert` class correctly converts an xml
        ontology to a turtle's one.
        """
        ontology_converter = OntologyConverter(self.source_xml_path)
        ontology_converter.convert(self.destination_ttl_path, "turtle")

        # Parsing the two graphs for comparison
        graph_valid = Graph()
        graph_test = Graph()
        graph_valid.parse(self.source_xml_path, format="xml")
        graph_test.parse(self.destination_ttl_path, format="ttl")

        self.assertTrue(graph_test.isomorphic(graph_valid))


if __name__ == "__main__":
    unittest.main()
