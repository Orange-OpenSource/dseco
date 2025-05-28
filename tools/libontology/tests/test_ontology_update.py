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
Test module for ontology update functionality.

This module contains unit tests for executing SPARQL UPDATE queries
and verifying the resulting ontology modifications.

Classes
-------
TestOntologyUpdate
    Test cases for ontology update operations.

Test Cases
----------
test_update
    Tests UPDATE query execution and verifies resulting changes.
"""

import unittest
import os
from rdflib import Graph
from libontology.ontology_update import OntologyUpdate


class TestOntologyUpdate(unittest.TestCase):
    """
    A class to test the `OntologyUpdate` class for updating an ontology.

    Methods
    -------
    setUp()
        Initializes paths for test ontologies and update query.
    test_update()
        Tests the update and verifies the resulting ontology.
    """
    def setUp(self):
        """
        Set up test paths for ontology and query file.
        """
        self.ontology_path = "./tests/test_update/test_onto.ttl"
        self.ontology_updated_path = (
            "./tests/test_update/test_onto_updated.ttl"
        )
        self.query_path = "./tests/test_update/add_class_hasName.sparql"

    def test_update(self):
        """
        Test the update of an ontology.

        Ensures that the `OntologyUpdate` class correctly adds concepts
        and that the resulting ontology matches the expected output.
        """
        # chemin du fichier temporaire où sera stockée onto_updated
        temp_path = "./tests/test_update/temp_file.ttl"

        with open(self.query_path, "r", encoding='utf-8') as file:
            update_query = file.read()
        ontology_update = OntologyUpdate(self.ontology_path)
        ontology_update.update_ontology(update_query)
        ontology_update.graph.serialize(destination=temp_path, format="turtle")

        # We parse the two graphs for comparison
        graph_valid = Graph()
        graph_test = Graph()
        graph_valid.parse(self.ontology_updated_path)
        graph_test.parse(temp_path)

        try:
            os.remove(temp_path)
        except FileNotFoundError:
            print(f"File '{temp_path}' not found.")
        self.assertTrue(graph_test.isomorphic(graph_valid))


if __name__ == "__main__":
    unittest.main()
