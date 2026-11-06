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
Module for comparing two RDF ontologies.

Functions
---------
ontology_compare(ontology1, ontology2)
    Returns True if both ontologies are isomorphic.
main()
    Command-line interface for comparing two ontologies.
"""

import argparse
import sys
from rdflib.compare import to_isomorphic
from . import __version__
from .base_ontology import BaseOntology


class _Ontology(BaseOntology):
    """Minimal concrete ontology used to load a file into a graph."""


def ontology_compare(ontology1, ontology2):
    """
    Compare two ontologies using canonical (isomorphic) graphs.

    Parameters
    ----------
    ontology1, ontology2 : str
        Paths of the ontology files to compare.

    Returns
    -------
    bool
        True if both graphs are isomorphic (blank node labels are ignored).
    """
    iso1 = to_isomorphic(_Ontology(ontology1).graph)
    iso2 = to_isomorphic(_Ontology(ontology2).graph)
    return iso1 == iso2


def main():
    """Parse command line arguments and compare two ontologies."""
    parser = argparse.ArgumentParser(
        description="Compare two ontologies (graph isomorphism)."
    )
    parser.add_argument("--ontology1", help="first ontology file", required=True)
    parser.add_argument("--ontology2", help="second ontology file", required=True)
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    if ontology_compare(args.ontology1, args.ontology2):
        sys.stdout.write("\033[92m[+] The ontologies are isomorphic.\033[0m\n")
    else:
        sys.stdout.write("\033[91m[-] The ontologies are different.\033[0m\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
