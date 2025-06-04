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
Base module for ontology operations using RDFLib.

This module provides an abstract base class for handling ontology operations
such as loading, querying, and manipulating RDF graphs.

Classes
-------
BaseOntology
    Abstract base class that implements common ontology operations.

Notes
-----
All derived classes should implement their specific operations while
inheriting from BaseOntology.
"""

import sys
from abc import ABC
from rdflib import Graph


class BaseOntology(ABC):
    """
    Abstract base class for ontology operations.

    This class provides the foundation for loading and managing ontologies
    using RDFLib Graph objects.

    Attributes
    ----------
    ontology_path : str
        Path to the ontology file.
    graph : rdflib.Graph
        RDF graph containing the loaded ontology.

    Methods
    -------
    load_ontology()
        Loads the ontology from the specified path into the RDF graph.
    """

    def __init__(self, ontology_path):
        """
        Initialize the base ontology with the path to the ontology file.

        Parameters
        ----------
        ontology_path : str
            Path to the ontology file.
        Raises
        ------
        FileNotFoundError
            If the ontology file does not exist.
        IOError
            If the ontology file cannot be read.
        Exception
            If the ontology file cannot be parsed.
        """
        self.ontology_path = ontology_path
        self.graph = Graph()
        self.load_ontology()

    def load_ontology(self):
        """
        Load the ontology into an RDF graph.

        Raises
        ------
        FileNotFoundError
            If the ontology file does not exist.
        IOError
            If the ontology file cannot be read.
        Exception
            If the ontology file cannot be parsed.
        """
        try:
            self.graph.parse(self.ontology_path)
            sys.stderr.write(
                f"\033[92m[+] Ontology loaded successfully from {self.ontology_path}\033[0m\n"
            )
        except FileNotFoundError:
            sys.stderr.write(
                f"\033[91m[-] Ontology file not found: {self.ontology_path}\033[0m\n"
            )
            raise
        except IOError as e:
            sys.stderr.write(
                f"\033[91m[-] Unable to read the ontology file: {e}\033[0m\n"
            )
            raise
        except Exception as e:
            sys.stderr.write(f"\033[91m[-] Failed to parse the ontology: {e}\033[0m\n")
            raise
