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
Test module for SHACL validation functionality.

This module contains unit tests for validating ontologies against
SHACL shapes graphs.

Classes
-------
TestOntologyShacl
    Test cases for SHACL validation operations.

Test Cases
----------
test_shacl_valid
    Tests validation of conformant ontologies.
test_shacl_invalid
    Tests validation of non-conformant ontologies.
"""

import unittest
from libontology.ontology_shacl import OntologyShacl


class TestOntologyShacl(unittest.TestCase):
    """
    A class to test the `OntologyShacl` class for validate our terminology.

    Methods
    -------
    setUp()
        Initializes paths for test ontologies.
    test_shacl_valid()
        Tests our terminology by verifying a valid shacl graph.
     test_shacl_invalid()
        Tests our terminology by verifying an invalid shacl graph.
    """
    def setUp(self):
        """
        Set up test paths for ontology and query file.
        """
        self.ontology_shacl_path = "./tests/test_shacl/test_shacl.ttl"
        self.ontology_shacl_valid_path = (
            "./tests/test_shacl/test_shacl_valid.ttl"
        )
        self.ontology_shacl_invalid_path = (
            "./tests/test_shacl/test_shacl_invalid.ttl"
        )

    def test_shacl_valid(self):
        """
        Test to validate our terminology.

        Ensures that the `OntologyShacl` class correctly ckecks the terminology
        and that the resulting ontology matches the expected output.
        It should return a true statement.
        """
        ontology_shacl = OntologyShacl(self.ontology_shacl_valid_path)
        conforms, result_text = ontology_shacl.validate_shacl(self.ontology_shacl_path)
        self.assertTrue(conforms)

    def test_shacl_invalid(self):
        """
        Test to validate our terminology.

        Ensures that the `OntologyShacl` class correctly ckecks the terminology
        and that the resulting ontology matches the expected output.
        It should return a false statement.
        """
        ontology_shacl = OntologyShacl(self.ontology_shacl_invalid_path)
        conforms, result_text = ontology_shacl.validate_shacl(self.ontology_shacl_path)
        self.assertFalse(conforms)


if __name__ == "__main__":
    unittest.main()
