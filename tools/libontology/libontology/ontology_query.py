#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
Module for executing SPARQL SELECT queries on RDF ontologies.

This module provides functionality to execute SELECT queries against
ontologies and format the results as CSV output.

Classes
-------
OntologyQuery
    Handles execution of SPARQL SELECT queries on ontologies.

Functions
---------
main()
    Command-line interface for executing SELECT queries.
"""

import argparse
import sys
import csv
from .base_ontology import BaseOntology


class OntologyQuery(BaseOntology):
    """
    Class for handling ontology SELECT queries.

    This class extends BaseOntology to provide specific functionality
    for executing SPARQL SELECT queries against RDF graphs.

    Methods
    -------
    execute_query(query: str) -> list
        Executes a SPARQL SELECT query and returns results as a list.
    """

    def execute_query(self, query):
        """
        Execute a SELECT query against the ontology.

        Parameters
        ----------
        query : str
            The SELECT query to execute.

        Returns
        -------
        result : list
            The list of results from the SELECT query.
        """
        return list(self.graph.query(query))


def main():
    """Parse command line arguments and execute the ontology SELECT query."""
    parser = argparse.ArgumentParser(description="Query the ontology in SPARQL.")
    parser.add_argument("--ontology", help="ontology file", required=True)
    parser.add_argument("--query", help="query file", required=True)

    args = parser.parse_args()

    try:
        with open(args.query, "r", encoding="utf-8") as file:
            query = file.read()
    except FileNotFoundError:
        sys.stderr.write(f"\033[91m[-] The file {args.query} not found.\033[0m\n")
        sys.exit(1)

    ontology_query = OntologyQuery(args.ontology)
    results = ontology_query.execute_query(query)

    csvwriter = csv.writer(sys.stdout, delimiter=" ", lineterminator="\n")
    sys.stderr.write("\033[96m[*] Query Results:\033[0m\n")
    for row in results:
        csvwriter.writerow(row)
    sys.stderr.write("\033[92m[+] Query executed successfully.\033[0m\n")


if __name__ == "__main__":
    main()
