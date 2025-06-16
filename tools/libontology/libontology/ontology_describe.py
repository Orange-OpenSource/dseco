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
Module for executing SPARQL DESCRIBE queries on RDF ontologies.

This module provides functionality to execute DESCRIBE queries against ontologies
and format the results as RDF/XML output.

Classes
-------
OntologyDescribe
    Handles execution of SPARQL DESCRIBE queries on ontologies.

Methods
-------
execute_query(query: str)
    Executes a SPARQL DESCRIBE query and returns the results.
render_describe_graph(results)
    Renders the DESCRIBE query results as RDF/XML.
"""

import argparse
import sys
from .base_ontology import BaseOntology


class OntologyDescribe(BaseOntology):
    """
    Class for handling ontology DESCRIBE queries.

    This class extends BaseOntology to provide specific functionality
    for executing SPARQL DESCRIBE queries against RDF graphs.

    Methods
    -------
    execute_query(query: str) -> rdflib.Graph
        Executes a SPARQL DESCRIBE query and returns a graph of results.
    render_describe_graph(results: rdflib.Graph) -> str
        Converts the results graph to RDF/XML format.

    Raises
    ------
    Exception
        If the query execution fails or the results cannot be rendered.
    """

    def execute_query(self, query):
        """
        Execute a DESCRIBE query against the ontology.

        Parameters
        ----------
        query : str
            The DESCRIBE query to execute.

        Returns
        -------
        """
        return self.graph.query(query)

    def render_describe_graph(self, results):
        """A method to display the graph"""
        return results.serialize(format="xml").decode("utf-8")


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

    ontology_describe = OntologyDescribe(args.ontology)
    results = ontology_describe.execute_query(query)

    sys.stderr.write("\033[96m[*] Query Results:\033[0m\n")

    print(ontology_describe.render_describe_graph(results))

    sys.stderr.write("\033[92m[+] Query executed successfully.\033[0m\n")


if __name__ == "__main__":
    main()
