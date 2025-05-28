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
Module for executing SPARQL UPDATE queries on RDF ontologies.

This module provides functionality to execute UPDATE queries against ontologies
and save the modified results to a new file.

Classes
-------
OntologyUpdate
    Handles execution of SPARQL UPDATE queries on ontologies.

Functions
---------
main()
    Command-line interface for executing UPDATE queries.
"""

import argparse
import sys
from .base_ontology import BaseOntology


class OntologyUpdate(BaseOntology):
    """
    Class for handling ontology UPDATE queries.

    This class extends BaseOntology to provide specific functionality
    for executing SPARQL UPDATE queries against RDF graphs.

    Methods
    -------
    update_ontology(update_query: str)
        Executes a SPARQL UPDATE query on the ontology.

    Parameters
    ----------
    update_query : str
        The SPARQL UPDATE query to execute.

    Raises
    ------
    Exception
        If the query execution fails or the ontology cannot be updated.
    """

    def update_ontology(self, update_query):
        """
        Update the ontology using a SPARQL UPDATE query.

        Parameters
        ----------
        update_query : str
            The SPARQL UPDATE query to execute.
        """
        self.graph.update(update_query)


def main():
    """Parse command line arguments and update the ontology."""
    parser = argparse.ArgumentParser(
        description="Update the ontology using a SPARQL UPDATE query."
    )
    parser.add_argument("--ontology", help="ontology file", required=True)
    parser.add_argument("--query", help="SPARQL update query file", required=True)
    parser.add_argument(
        "--destination", help="destination ontology file", required=True
    )

    args = parser.parse_args()

    try:
        with open(args.query, "r", encoding="utf-8") as file:
            update_query = file.read()
    except FileNotFoundError:
        sys.stderr.write(f"\033[91m[-] The file {args.query} not found.\033[0m\n")
        sys.exit(1)

    ontology_update = OntologyUpdate(args.ontology)
    try:
        ontology_update.update_ontology(update_query)
        ontology_update.graph.serialize(destination=args.destination, format="turtle")
        sys.stdout.write(
            f"\033[92m[+] Ontology updated and saved to {args.destination}\033[0m\n"
        )
    except Exception as e:
        sys.stderr.write(
            f"\033[91m[-] An error occurred while updating the ontology: {e}\033[0m\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
