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
from . import __version__
from .ontology_query import OntologyQuery
from rdflib.term import URIRef

# Requêtes SPARQL prédéfinies pour les statistiques d'ontologie
PREDEFINED_QUERIES = {
    "Triples Count": """
        SELECT (COUNT(?s) AS ?triples) WHERE { ?s ?p ?o }
    """,
    
    "Classes Count": """
        SELECT ?o (COUNT(?s) AS ?count) WHERE { 
            ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o .
            FILTER(?o != <http://www.w3.org/2002/07/owl#Class>)
        } 
        GROUP BY ?o
        ORDER BY ?o
    """,
    
    "Properties Count": """
        SELECT ?p (COUNT(?s) AS ?count) WHERE { 
            ?s ?p ?o 
        } 
        GROUP BY ?p
        ORDER BY ?p

    """,
    
    "Individuals Count": """
        SELECT (COUNT(DISTINCT ?individual) AS ?count)
        WHERE {
            ?individual a <http://www.w3.org/2002/07/owl#NamedIndividual> .
        }
    """
}


class OntologyStats(OntologyQuery):
    """
    Class for handling ontology SELECT queries.

    This class extends BaseOntology to provide specific functionality
    for executing SPARQL SELECT queries against RDF graphs.

    Methods
    -------
    execute_query(query: str) -> list
        Executes a SPARQL SELECT query and returns results as a list.
    """
    
    def execute_all_queries(self):
        """
        Execute all predefined SPARQL queries and return their results.
        """
        
        namespace_manager = getattr(self, 'graph', None)
        if namespace_manager:
            namespace_manager = self.graph.namespace_manager
        for query_name, query in PREDEFINED_QUERIES.items():
            print(f"\n=== {query_name} ===")
            try:
                results = self.execute_query(query)
                if results:
                    for row in results:
                        new_row = list(row)
                        # Remplacer URI par qname pour la colonne 0 si c'est une URI
                        if namespace_manager and len(new_row) > 0:
                            try:
                                if new_row[0].startswith('http'):
                                    new_row[0] = namespace_manager.normalizeUri(URIRef(new_row[0]))
                            except Exception:
                                pass
                        print(" | ".join(map(str, new_row)))
                else:
                    print("No results found")
            except Exception as e:
                print(f"Error executing query: {e}")
        print(f"\n\033[92m[+] All statistics queries executed successfully.\033[0m")


def main():
    """Parse command line arguments and execute predefined ontology statistics queries."""
    parser = argparse.ArgumentParser(description="Generate statistics for the ontology using predefined SPARQL queries.")
    parser.add_argument("--ontology", help="ontology file", required=True)

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    ontology_stats = OntologyStats(args.ontology)
    ontology_stats.execute_all_queries()


if __name__ == "__main__":
    main()
