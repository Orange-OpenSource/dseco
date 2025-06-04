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
Module for adding SWRL rules to OWL ontologies.

This module provides functionality to add Semantic Web Rule Language (SWRL)
rules to existing ontologies using the Owlready2 library.

Classes
-------
OntologyAddSwrlRule
    Handles the addition of SWRL rules to ontologies.

Notes
-----
SWRL rules must follow the correct syntax and reference existing classes
and properties in the ontology.
"""

import argparse
import sys
import tempfile
import owlready2 as owl
from .base_ontology import BaseOntology
from .ontology_convert import OntologyConverter


class OntologyAddSwrlRule(BaseOntology):
    """
    Class for adding SWRL rules to ontologies.

    Methods
    -------
    add_swrl_rule(output_file: str, swrl_rule: str)
        Adds a SWRL rule to the ontology and saves the result.

    Parameters
    ----------
    output_file : str
        Path where the modified ontology will be saved.
    swrl_rule : str
        The SWRL rule to be added to the ontology.

    Raises
    ------
    Exception
        If the SWRL rule is invalid or cannot be added to the ontology.
    """

    def add_swrl_rule(self, output_file, swrl_rule):
        """
        Add the SWRL rule and execute it.

        Parameters
        ----------
        input_file : str
            The source ontology.
        output_file : str
            The destination ontology.
        swrl_rule : str
            The SWRL rule to execute.

        Returns
        -------
        """
        onto = owl.get_ontology(self.ontology_path).load()

        with onto:
            rule = owl.Imp()
            rule.set_as_rule(swrl_rule)
            onto.save(file=output_file, format="rdfxml")


def main():
    """Parse command line arguments and add swrl rule to the ontology."""
    parser = argparse.ArgumentParser(description="Add a swrl rule to the ontology.")
    parser.add_argument("--ontology", help="ontology turtle file", required=True)
    parser.add_argument("--rulefile", help="rule file", required=True)
    parser.add_argument(
        "--destination", help="destination ontology turtle file", required=True
    )

    args = parser.parse_args()

    with (
        tempfile.NamedTemporaryFile(delete=True, suffix=".xml") as temp_source,
        tempfile.NamedTemporaryFile(delete=True, suffix=".xml") as temp_destination,
    ):

        temp_source_xml_path = temp_source.name
        temp_destination_with_rule_xml_path = temp_destination.name

        # We convert our source ontology to xml format
        # because get_ontology can only read xml's formats
        ontology_converter = OntologyConverter(args.ontology)
        ontology_converter.convert(temp_source_xml_path, "xml")

        try:
            with open(args.rulefile, "r", encoding="utf-8") as file:
                swrl_rule = file.read()
        except FileNotFoundError:
            sys.stderr.write(
                f"\033[91m[-] The file {args.rulefile} not found.\033[0m\n"
            )
            sys.exit(1)

        try:
            # We add the SWRL rule to the xml source file and we save a xml destination file
            ontology_add_swrl_rule = OntologyAddSwrlRule(temp_source_xml_path)
            ontology_add_swrl_rule.add_swrl_rule(
                output_file=temp_destination_with_rule_xml_path, 
                swrl_rule=swrl_rule
            )

            # We finally convert the xml destination file into a turtle file
            ontology_converter = OntologyConverter(temp_destination_with_rule_xml_path)
            ontology_converter.convert(args.destination, "turtle")

            sys.stdout.write(
                f"\033[92m[+] Ontology updated and saved to {args.destination}\033[0m\n"
            )
        except Exception as e:
            sys.stderr.write(
                f"\033[91m[-] An error occurred while adding the rule to the ontology: {e}\033[0m\n"
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
