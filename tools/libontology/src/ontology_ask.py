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
Module for executing SPARQL ASK queries on RDF ontologies.

This module provides functionality to execute ASK queries against ontologies
and return boolean results.

Classes
-------
OntologyAsk
    Handles execution of SPARQL ASK queries on ontologies.

Functions
---------
main()
    Command-line interface for executing ASK queries.
"""

import argparse
import sys
from .base_ontology import BaseOntology


class OntologyAsk(BaseOntology):
    """
    Class for handling ontology ASK queries.

    This class extends BaseOntology to provide specific functionality
    for executing SPARQL ASK queries against RDF graphs.

    Methods
    -------
    execute_query(query: str) -> bool
        Executes a SPARQL ASK query and returns a boolean result.

    Parameters
    ----------
    query : str
        The SPARQL ASK query to execute.

    Returns
    -------
    bool
        True if the query matches, False otherwise.

    Raises
    ------
    Exception
        If the query execution fails.
    """

    def execute_query(self, query):
        """
        Execute an ASK query against the ontology.

        Parameters
        ----------
        query : str
            The ASK query to execute.

        Returns
        -------
        result : bool
            The boolean result of the ASK query.
        """
        return bool(self.graph.query(query))


def main():
    """Parse command line arguments and execute the ontology ASK query."""
    parser = argparse.ArgumentParser(
        description="Perform a boolean ASK query on the ontology."
    )
    parser.add_argument("--ontology", help="ontology file", required=True)
    parser.add_argument("--query", help="ASK query file", required=True)

    args = parser.parse_args()

    try:
        with open(args.query, "r", encoding="utf-8") as file:
            query = file.read()
    except FileNotFoundError:
        sys.stderr.write(f"\033[91m[-] The file {args.query} not found.\033[0m\n")
        sys.exit(1)

    ontology_ask = OntologyAsk(args.ontology)
    result = ontology_ask.execute_query(query)

    sys.stderr.write(f"\033[96m[*] Answer: {result}\033[0m\n")
    if result:
        sys.stdout.write("\033[92m[+] The ASK query returned true.\033[0m\n")
    else:
        sys.stdout.write("\033[91m[-] The ASK query returned false.\033[0m\n")


if __name__ == "__main__":
    main()
