#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
Module for executing many SPARQL UPDATE queries on an RDF ontology.

All queries are run on the same graph, then the result is serialized once.
"""

import argparse
from . import __version__
import sys
import owlrl
from pathlib import Path
from .base_ontology import BaseOntology, read_text_file


class OntologyBulkUpdate(BaseOntology):
    def infer(self):
        owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(self.graph)

    def update_ontology_many(self, update_queries, infer_each=False):
        for i, query in enumerate(update_queries):
            if i == 0 or infer_each:
                self.infer()
            self.graph.update(query)


def main():
    parser = argparse.ArgumentParser(
        description="Run all SPARQL UPDATE queries of a directory (in sorted order), "
        "then serialize the ontology once."
    )
    parser.add_argument("--ontology", help="ontology file", required=True)
    parser.add_argument(
        "--queries-dir",
        help="directory with the SPARQL update files",
        required=True,
    )
    parser.add_argument(
        "--infer-each",
        action="store_true",
        help="recompute the OWL-RL closure before each query ",
    )
    parser.add_argument(
        "--destination", help="destination ontology turtle file", required=True
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    query_files = sorted(Path(args.queries_dir).glob("*.sparql"))
    if not query_files:
        sys.stderr.write(f"\033[91m[-] No query files found in {args.queries_dir}\033[0m\n")
        sys.exit(1)
    update_queries = [read_text_file(str(p)) for p in query_files]

    ontology_bulk_update = OntologyBulkUpdate(args.ontology)
    try:
        ontology_bulk_update.update_ontology_many(update_queries, infer_each=args.infer_each)
        ontology_bulk_update.graph.serialize(destination=args.destination, format="turtle")
        sys.stdout.write(
            f"\033[92m[+] {len(update_queries)} queries applied, "
            f"ontology saved to {args.destination}\033[0m\n"
        )
    except Exception as e:
        sys.stderr.write(
            f"\033[91m[-] An error occurred while updating the ontology: {e}\033[0m\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
