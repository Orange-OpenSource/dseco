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
Module for SHACL validation of RDF ontologies.

This module provides functionality to validate RDF graphs against SHACL shapes
using the pyshacl library. It supports both data graph and shapes graph validation.

Classes
-------
OntologyShacl
    Handles SHACL validation of ontologies.

Functions
---------
main()
    Command-line interface for SHACL validation.

Notes
-----
SHACL validation requires both a data graph and a shapes graph. The shapes graph
contains the SHACL shapes that define the validation rules.
"""

import argparse
import sys
from pyshacl import validate
from .base_ontology import BaseOntology


class OntologyShacl(BaseOntology):
    """
    Class for SHACL validation of ontologies.

    This class extends BaseOntology to provide specific functionality
    for validating ontologies against SHACL shapes.

    Methods
    -------
    validate_shacl(shacl_graph: str) -> Tuple[bool, str]
        Validates the ontology against SHACL constraints.

    Parameters
    ----------
    shacl_graph : str
        Path to the SHACL shapes file.

    Returns
    -------
    tuple
        (bool, str) tuple containing validation result and detailed message.
    """

    def validate_shacl(self, shacl_graph):
        """
        Validate the shacl structure of the ontology .
        """
        conforms, _, results_text = validate(
            self.ontology_path, shacl_graph=shacl_graph
        )
        return conforms, results_text


def main():
    """Parse command line arguments and validate using shacl the ontology."""
    parser = argparse.ArgumentParser(description="Shacl validate the ontology.")
    parser.add_argument("--ontology", help="ontology file", required=True)
    parser.add_argument(
        "--shacl", help="file containing shacl's constraints", required=True
    )

    args = parser.parse_args()

    try:
        ontology_shacl = OntologyShacl(args.ontology)
        conforms, results_text = ontology_shacl.validate_shacl(args.shacl)
        if conforms:
            sys.stdout.write(f"\033[92m[+] Ontology {args.ontology} is valid.\033[0m\n")
        else:
            sys.stdout.write(
                f"\033[91m[-] Ontology {args.ontology} is not valid.\033[0m\n"
            )
            sys.stdout.write(f"{results_text}")
            sys.exit(1)
    except Exception as e:
        sys.stderr.write(
            f"\033[91m[-] Shacl validation failed for ontology {args.ontology}: {e}\033[0m\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
