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
Test module for ontology SWRL rule addition functionality.

This module contains unit tests for the `OntologyAddSwrlRule` class, verifying
the correct addition of SWRL rules to ontologies.

Classes
-------
TestOntologyAddSwrlRule
    Test cases for adding SWRL rules to ontologies.

Test Cases
----------
test_add_swrl_rule
    Tests the addition of a SWRL rule and verifies the resulting ontology.
"""

import unittest
import os
from libontology.ontology_add_swrl_rule import OntologyAddSwrlRule
from libontology.ontology_convert import OntologyConverter
from rdflib import Graph


class TestOntologyAddSwrlRule(unittest.TestCase):
    """
    A class to test the `OntologyAddSwrlRule` class for SWRL rule addition.

    Methods
    -------
    setUp()
        Initializes paths for test ontologies and SWRL rules.
    test_add_swrl_rule()
        Tests the addition of a SWRL rule and verifies the resulting ontology.
    """

    def setUp(self):
        """
        Set up test paths for ontology and SWRL rule files.
        """
        self.ontology_path = "./tests/test_add_swrl_rule/test_onto.ttl"
        self.ontology_with_rule_path = (
            "./tests/test_add_swrl_rule/test_onto_with_rule.ttl"
        )
        self.swrl_rule_path = (
            "./tests/test_add_swrl_rule/human_is_hacked.swrl"
        )

    def test_add_swrl_rule(self):
        """
        Test the addition of a SWRL rule to an ontology.

        Ensures that the `OntologyAddSwrlRule` class correctly adds a SWRL rule
        and that the resulting ontology matches the expected output.
        """
        temp_path = "./tests/test_add_swrl_rule/temp_file.ttl"
        temp_source_xml_path = "/tmp/temp_source_file.xml"
        temp_destination_with_rule_xml_path = "/tmp/temp_file_with_rule.xml"

        # Convert ontology to XML format
        OntologyConverter(self.ontology_path).convert(temp_source_xml_path, "xml")

        # Read SWRL rule and add it to the ontology
        with open(self.swrl_rule_path, "r", encoding='utf-8') as file:
            swrl_rule = file.read()
        ontology_add_swrl_rule = OntologyAddSwrlRule(temp_source_xml_path)
        ontology_add_swrl_rule.add_swrl_rule(
            output_file=temp_destination_with_rule_xml_path,
            swrl_rule=swrl_rule
        )

        # Convert the modified ontology back to Turtle format
        OntologyConverter(temp_destination_with_rule_xml_path).convert(
            temp_path, "turtle"
        )

        # Compare the resulting ontology with the expected ontology
        graph_valid = Graph()
        graph_test = Graph()
        graph_valid.parse(self.ontology_with_rule_path, format="turtle")
        graph_test.parse(temp_path, format="turtle")

        try:
            os.remove(temp_path)
        except FileNotFoundError:
            print(f"File '{temp_path}' not found.")

        self.assertTrue(graph_test.isomorphic(graph_valid))


if __name__ == "__main__":
    unittest.main()
