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


import os
import unittest
import tempfile
from pathlib import Path
from rdflib import Graph, Literal, URIRef

from libontology.ontology_update import OntologyUpdate
from libontology.ontology_bulk_update import OntologyBulkUpdate


class TestOntologyBulkUpdate(unittest.TestCase):

    def setUp(self):
        self.ontology_path = "./tests/test_bulk_update/test_onto.ttl"
        self.query_files = sorted(Path("./tests/test_bulk_update").glob("*.sparql"))
        self.queries = [
            Path(p).read_text(encoding="utf-8") for p in self.query_files
        ]

    def test_bulk_matches_sequential_updates(self):
        out_dir = "./tests/test_bulk_update"

        with tempfile.TemporaryDirectory() as tmp:
            current = self.ontology_path
            for i, query in enumerate(self.queries):
                ou = OntologyUpdate(current)
                ou.update_ontology(query)
                current = os.path.join(tmp, f"step_{i}.ttl")
                ou.graph.serialize(destination=current, format="turtle")
            sequential = Graph()
            sequential.parse(current)

        sequential.serialize(destination=os.path.join(out_dir, "sequential_final.ttl"),
                              format="turtle")

       
        bulk = OntologyBulkUpdate(self.ontology_path)
        bulk.update_ontology_many(self.queries, infer_each=True)
        bulk.graph.serialize(destination=os.path.join(out_dir, "bulk.ttl"),
                             format="turtle")
        bulk_graph = Graph()
        bulk_graph.parse(os.path.join(out_dir, "bulk.ttl"))

        self.assertTrue(bulk_graph.isomorphic(sequential))


if __name__ == "__main__":
    unittest.main()