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
Test module for ontology ASK query functionality.

This module contains unit tests for the `OntologyAsk` class, verifying the
correct execution of SPARQL ASK queries against test ontologies.

Classes
-------
TestOntologyAsk
    Test cases for `OntologyAsk` class functionality.

Test Cases
----------
test_ask_valid
    Tests that valid ASK queries return True.
test_ask_invalid
    Tests that invalid ASK queries return False.
"""

import unittest
from libontology.ontology_ask import OntologyAsk


class TestOntologyAsk(unittest.TestCase):
    """
    A class to test the `OntologyAsk` class for SPARQL ASK queries.

    Methods
    -------
    setUp()
        Initializes paths for test ontologies and queries.
    test_ask_valid()
        Tests that a valid ASK query returns True.
    test_ask_invalid()
        Tests that an invalid ASK query returns False.
    """

    def setUp(self):
        """
        Set up test paths for ontology and SPARQL queries.
        """
        self.ontology_path = "./tests/test_ask/test_onto.ttl"
        self.ask_query_valid = "./tests/test_ask/ask_age_valid.sparql"
        self.ask_query_invalid = "./tests/test_ask/ask_age_invalid.sparql"

    def test_ask_valid(self):
        """
        Test a valid SPARQL ASK query.

        Ensures that the `OntologyAsk` class correctly evaluates a valid ASK
        query and returns True.
        """
        with open(self.ask_query_valid, "r", encoding='utf-8') as file:
            ask_query_valid = file.read()
        ontology_ask = OntologyAsk(self.ontology_path)
        self.assertTrue(ontology_ask.execute_query(ask_query_valid))

    def test_ask_invalid(self):
        """
        Test an invalid SPARQL ASK query.

        Ensures that the `OntologyAsk` class correctly evaluates an invalid
        ASK query and returns False.
        """
        with open(self.ask_query_invalid, "r", encoding='utf-8') as file:
            ask_query_invalid = file.read()
        ontology_ask = OntologyAsk(self.ontology_path)
        self.assertFalse(ontology_ask.execute_query(ask_query_invalid))


if __name__ == "__main__":
    unittest.main()
