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

"""Test module for the `ontology_compare` function."""

import unittest
from libontology.ontology_compare import ontology_compare


class TestOntologyCompare(unittest.TestCase):
    """Test cases for `ontology_compare`."""

    def test_compare_identical(self):
        """An ontology is isomorphic to itself."""
        path = "./tests/test_update/test_onto.ttl"
        self.assertTrue(ontology_compare(path, path))

    def test_compare_identical_but_different_files(self):
        """Two identical ontologies in different files are isomorphic."""
        path1 = "./tests/test_update/test_onto.ttl"
        path2 = "./tests/test_update/test_onto_2.ttl"
        self.assertTrue(ontology_compare(path1, path2))


    def test_compare_different(self):
        """Two different ontologies are not isomorphic."""
        self.assertFalse(
            ontology_compare(
                "./tests/test_update/test_onto.ttl",
                "./tests/test_update/test_onto_updated.ttl",
            )
        )


if __name__ == "__main__":
    unittest.main()
