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

import unittest
import io
from contextlib import redirect_stdout
from libontology.ontology_smart_diff import OntologySmartDiff, get_stats_file_path, print_formatted_output
from libontology.ontology_stats import OntologyStats


class TestOntologySmartDiff(unittest.TestCase):
    """
    A class to test the `OntologySmartDiff` class.
    """
    def setUp(self):
        """
        Set up test paths for ontology and query file.
        """
        self.new_ontology_path = "./tests/test_smart_diff/test_onto_new.ttl"
        self.old_ontology_path = "./tests/test_smart_diff/test_onto_old.ttl"
        self.result_path = "./tests/test_smart_diff/smart_diff.txt"

    def test_smart_diff(self):
        """
        Ensures that the `OntologySmartDiff` class correctly smart diffs two ontologies
        and that the resulting matches the expected output.
        """
        new_stats_path = get_stats_file_path(self.new_ontology_path)
        old_stats_path = get_stats_file_path(self.old_ontology_path)

        ontology_smart_diff = OntologySmartDiff(new_stats_path, old_stats_path)
        differences = ontology_smart_diff.compare_stats()

        output = io.StringIO()
        with redirect_stdout(output):
            print_formatted_output(differences)

        print_formatted_output(differences)
        # Récupérer le contenu capturé
        stdout_content = output.getvalue()

        # Lire fichier txt de résultat valide
        with open(self.result_path, "r", encoding='utf-8') as valid_result_file:
            valid_result = valid_result_file.read()

        self.assertEqual(stdout_content.strip(), valid_result.strip())


if __name__ == "__main__":
    unittest.main()
