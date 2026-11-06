# Copyright (c) 2023-2026 Orange. All rights reserved.
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
Test module for ontology SELECT query functionality.

This module contains unit tests for executing SPARQL SELECT queries
and verifying their results against expected output.

Classes
-------
TestOntologyQuery
    Test cases for SELECT query operations.

Test Cases
----------
test_query
    Tests SELECT query execution and result formatting.
"""

import sys
import unittest
import io
import csv
from contextlib import redirect_stdout
from libontology.ontology_stats import OntologyStats


class TestOntologyStats(unittest.TestCase):
    """
    A class to test the `OntologyStats` class for querying an ontology.

    Methods
    -------
    setUp()
        Initializes paths for test ontologies and query path.
    test_query()
        Tests to query an ontology and verifies the resulting ontology.
    """
    def setUp(self):
        """
        Set up test paths for ontology and query file.
        """
        self.ontology_path = "./tests/test_stats/test_onto.ttl"
        self.result_path = "./tests/test_stats/stats.csv"

    def test_stats(self):
        """
        Test to query an ontology.

        Ensures that the `OntologyQuery` class correctly queries an ontology
        and that the resulting ontology matches the expected output.
        """
        ontology_stats = OntologyStats(self.ontology_path)
        output = io.StringIO()
        with redirect_stdout(output):
            ontology_stats.execute_all_queries()

        # Récupérer le contenu capturé
        stdout_content = output.getvalue()

        # Lire fichier csv de résultat valide
        with open(self.result_path, "r", encoding='utf-8') as valid_result_file:
            valid_result = valid_result_file.read()

        self.assertEqual(stdout_content.strip(), valid_result.strip())


if __name__ == "__main__":
    unittest.main()
