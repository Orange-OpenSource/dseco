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
Module for converting ontologies between different RDF formats.

This module provides functionality to convert ontologies between various
formats supported by RDFLib (e.g., Turtle, RDF/XML).

Classes
-------
OntologyConverter
    Handles conversion between different ontology formats.

Functions
---------
convert_ontology(output_format: str = None)
    Command-line interface for ontology format conversion.
convert_ttl_to_xmlrdf()
    Converts from Turtle to RDF/XML format.
convert_xmlrdf_to_ttl()
    Converts from RDF/XML to Turtle format.
"""

import argparse
import sys
from .base_ontology import BaseOntology


class OntologyConverter(BaseOntology):
    """
    Class for handling ontology format conversions.

    This class provides methods to convert ontologies between different
    RDF serialization formats.

    Methods
    -------
    convert(destination: str, output_format: str)
        Converts the ontology to specified format and saves to destination.
    """

    def convert(self, destination, output_format):
        """
        Convert the ontology to the specified format and save it to the destination.

        Parameters
        ----------
        destination : str
            The destination file path for the converted ontology.
        output_format : str
            The output format to convert the ontology to.
        """
        self.graph.serialize(destination=destination, format=output_format)


def convert_ontology(output_format=None):
    """Parse command line arguments and convert the ontology format."""
    parser = argparse.ArgumentParser(description="Convert the ontology format.")
    parser.add_argument("--ontology", help="input ontology file", required=True)
    parser.add_argument(
        "--destination", help="destination ontology file", required=True
    )

    args = parser.parse_args()

    ontology_converter = OntologyConverter(args.ontology)
    try:
        ontology_converter.convert(args.destination, output_format)
        sys.stdout.write(
            f"""\033[92m[+] Ontology converted to {output_format} \
            and saved to {args.destination}\033[0m\n"""
        )
    except Exception as e:
        sys.stderr.write(
            f"\033[91m[-] An error occurred during conversion: {e}\033[0m\n"
        )
        sys.exit(1)


def convert_ttl_to_xmlrdf():
    """Convert the ontology format to RDF/XML."""
    convert_ontology("xml")


def convert_xmlrdf_to_ttl():
    """Convert the ontology format to Turtle."""
    convert_ontology("turtle")
