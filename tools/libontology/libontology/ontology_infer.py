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
Module for performing inference on RDF ontologies.

This module provides functionality to perform inference using different reasoners:
Hermit, Pellet, and OWL-RL. Each reasoner implements different inference strategies
and capabilities.

Classes
-------
OntologyInferHermit
    Performs inference using the Hermit reasoner.
OntologyInferPellet
    Performs inference using the Pellet reasoner.
OntologyInferOwlrl
    Performs inference using the OWL-RL reasoner.

Notes
-----
Different reasoners may produce different results based on their implementation
and the inference rules they support.
"""

import argparse
import sys
import tempfile
import owlrl
import owlready2 as owl
from owlready2 import default_world
import rdflib
from .base_ontology import BaseOntology
from .ontology_convert import OntologyConverter


class OntologyInferHermit(BaseOntology):
    """
    Class for performing inference using the Hermit reasoner.

    Methods
    -------
    perform_inference(destination: str)
        Performs inference and saves results to the specified destination.
    """

    def perform_inference(self, destination):
        """Perform inference on our ontology using reasoner hermit"""
        # We are required to create a world for inferences,
        # otherwise there is a conflict in the in-memory quadstore
        hermit_world = owl.World()
        onto = hermit_world.get_ontology(self.ontology_path).load()
        with onto:
            owl.sync_reasoner(hermit_world, infer_property_values=True)
            onto.save(file=destination, format="rdfxml")


class OntologyInferPellet(BaseOntology):
    """
    Class for performing inference using the Pellet reasoner.

    Methods
    -------
    perform_inference(destination: str)
        Performs inference and saves results to the specified destination.
    """

    def perform_inference(self, destination):
        """Perform inference on our ontology using reasoner pellet"""
        # We are required to create a world for inferences,
        # otherwise there is a conflict in the in-memory quadstore
        pellet_world = owl.World()
        onto = pellet_world.get_ontology(self.ontology_path).load()
        with onto:
            owl.sync_reasoner_pellet(
                pellet_world,
                infer_property_values=True,
                infer_data_property_values=True,
                debug=2,
                keep_tmp_file=True,
            )
            onto.save(file=destination, format="rdfxml")


class OntologyInferOwlrl(BaseOntology):
    """
    Class for performing inference using the OWL-RL reasoner.

    Methods
    -------
    perform_inference(destination: str)
        Performs inference and saves results to the specified destination.
    """

    def perform_inference(self, destination):
        """Perform inference on our ontology using reasoner owlrl"""
        owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(self.graph)
        self.graph.serialize(destination=destination, format="xml")


def get_infer_class(reasoner, ontology):
    """A method to retrieve an infer class based on the reasoner"""
    REASONER_CLASSES = {
        "hermit": OntologyInferHermit,
        "pellet": OntologyInferPellet,
        "owlrl": OntologyInferOwlrl,
    }

    try:
        InferClass = REASONER_CLASSES[reasoner.lower()]
        ontology_infer = InferClass(ontology)
    except KeyError:
        sys.stderr.write(
            f"""\033[91m[-] Invalid reasoner: {reasoner}. \
            Must be one of {list(REASONER_CLASSES.keys())}\033[0m\n"""
        )
        sys.exit(1)
    return ontology_infer


def infer_on_xml_ontology(source, destination, reasoner):
    """A method to perform inference on 2 xml ontologies.
        It gets the infer class by using the reasoner and the source.
        It clears the world of the reasoner.
        Finally, it performs inference usign the adequate class.
    """
    ontology_infer = get_infer_class(reasoner, source)
    default_world.ontologies.clear()
    ontology_infer.perform_inference(destination=destination)

def preserve_namespaces(original_path, destination_path):
    """
    Preserves the original namespaces in an inferred file using rdflib.

    Parameters
    ----------
    original_path : str
        Path to the original ontology.
    destination_path : str
        Path to the inferred ontology.
    """

    original_graph = rdflib.Graph()
    original_graph.parse(original_path, format="turtle")

    inferred_graph = rdflib.Graph()
    inferred_graph.parse(destination_path, format="turtle")

    for prefix, uri in original_graph.namespaces():
        inferred_graph.bind(prefix, uri, override=True)
    
    inferred_graph.serialize(destination=destination_path, format="turtle")

def main():
    """Parse command line arguments and perform OWL RL inference."""
    parser = argparse.ArgumentParser(
        description="Perform OWL RL inference on the ontology."
    )
    parser.add_argument("--ontology", help="ontology file", required=True)
    parser.add_argument(
        "--destination", help="destination ontology file", required=True
    )
    parser.add_argument(
        "--reasoner",
        help="reasoner to use (hermit, pellet, owlrl), owrl cannot parse SWRL rules",
        required=True,
    )

    args = parser.parse_args()

    with (
        tempfile.NamedTemporaryFile(delete=True, suffix=".xml") as temp_source,
        tempfile.NamedTemporaryFile(delete=True, suffix=".xml") as temp_destination,
    ):

        temp_source_xml_path = temp_source.name
        temp_destination_xml_path = temp_destination.name

        # We convert our source ontology to xml format \
        # because get_ontology can only read xml's formats
        ontology_converter = OntologyConverter(args.ontology)
        ontology_converter.convert(temp_source_xml_path, "xml")

        try:
            infer_on_xml_ontology(source=temp_source_xml_path,
                                  destination=temp_destination_xml_path,
                                  reasoner=args.reasoner)

            # We finally convert the xml destination file into a turtle file
            ontology_converter = OntologyConverter(temp_destination_xml_path)
            ontology_converter.convert(args.destination, "turtle")

            preserve_namespaces(args.ontology, args.destination)

            sys.stdout.write(
                f"\033[92m[+] Ontology inference completed and saved to {args.destination}\033[0m\n"
            )
        except Exception as e:
            sys.stderr.write(
                f"\033[91m[-] An error occurred while saving the ontology: {e}\033[0m\n"
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
