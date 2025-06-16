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
Test module for ontology DESCRIBE query functionality.

This module contains unit tests for executing SPARQL DESCRIBE queries and
verifying their output format and content.

Classes
-------
TestOntologyDescribe
    Test cases for DESCRIBE query functionality.

Test Cases
----------
test_describe
    Tests DESCRIBE query execution and output formatting.
"""

import unittest
import io
from contextlib import redirect_stdout
from libontology.ontology_describe import OntologyDescribe


class TestOntologyDescribe(unittest.TestCase):
    """
    A class to test the `OntologyDescribe` class for SPARQL DESCRIBE queries.

    Methods
    -------
    setUp()
        Initializes paths for test ontologies and queries.
    test_describe()
        Tests the execution of a DESCRIBE query and verifies the output.
    """

    def setUp(self):
        """
        Set up test paths for ontology and SPARQL query files.
        """
        self.ontology_path = "./tests/test_describe/test_onto.ttl"
        self.described_element_path = (
            "./tests/test_describe/described_didier.txt"
        )
        self.query_path = "./tests/test_describe/describe_didier.sparql"

    def test_describe(self):
        """
        Test the execution of a SPARQL DESCRIBE query.

        Ensures that the `OntologyDescribe` class correctly executes a DESCRIBE
        query and that the output matches the expected result.
        """
        with open(self.query_path, "r", encoding='utf-8') as file:
            describe_query = file.read()
        ontology_describe = OntologyDescribe(self.ontology_path)
        results = ontology_describe.execute_query(describe_query)

        # Capture the rendered output
        output = io.StringIO()
        with redirect_stdout(output):
            print(ontology_describe.render_describe_graph(results))
        test_render = output.getvalue().strip()

        # Compare the rendered output with the expected result
        with open(self.described_element_path, "r", encoding='utf-8') as described_file:
            element_described = described_file.read().strip()
        self.assertEqual(test_render, element_described)


if __name__ == "__main__":
    unittest.main()
