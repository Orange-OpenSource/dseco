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
Module for validating RDF ontologies.

This module provides functionality to validate ontologies by attempting to parse
them and checking for syntax errors using RDFLib.

Classes
-------
OntologyValidate
    Handles validation of ontology files.

Functions
---------
main()
    Command-line interface for ontology validation.
"""

import argparse
import sys
from .base_ontology import BaseOntology


class OntologyValidate(BaseOntology):
    """
    Class for validating ontology files.

    This class extends BaseOntology to provide specific functionality
    for validating ontology files by attempting to parse them.

    Methods
    -------
    validate() -> bool
        Validates the ontology by attempting to parse it.

    Returns
    -------
    bool
        True if the ontology is valid, raises an exception otherwise.

    Raises
    ------
    Exception
        If the ontology is invalid or cannot be parsed.
    """

    def validate(self):
        """
        Validate the ontology by attempting to parse it.
        """
        # The ontology is already parsed in the BaseOntology constructor.
        # If no exceptions were raised, the ontology is considered valid.
        return True


def main():
    """Parse command line arguments and validate the ontology."""
    parser = argparse.ArgumentParser(description="Validate the ontology.")
    parser.add_argument("--ontology", help="ontology file", required=True)

    args = parser.parse_args()

    try:
        ontology_validate = OntologyValidate(args.ontology)
        valid = ontology_validate.validate()
        if valid:
            sys.stdout.write(f"\033[92m[+] Ontology {args.ontology} is valid.\033[0m\n")
    except Exception as e:
        sys.stderr.write(
            f"\033[91m[-] Validation failed for ontology {args.ontology}: {e}\033[0m\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
