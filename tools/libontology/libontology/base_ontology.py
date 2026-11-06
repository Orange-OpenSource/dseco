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
Base module for ontology operations using RDFLib.

This module provides an abstract base class for handling ontology operations
such as loading, querying, and manipulating RDF graphs.
"""

import sys
from abc import ABC
from rdflib import Graph
from pathlib import Path
import defusedxml.ElementTree as ET


def read_text_file(path):
    """Return the content of a text file, or exit(1) if it does not exist."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        sys.stderr.write(f"\033[91m[-] The file {path} not found.\033[0m\n")
        sys.exit(1)


class BaseOntology(ABC):
    """
    Abstract base class for ontology operations.

    This class provides the foundation for loading and managing ontologies
    using RDFLib Graph objects.
    """

    def __init__(self, ontology_path):
        """
        Initialize the base ontology with the path to the ontology file.
        """
        self.ontology_path = ontology_path
        self.graph = Graph()
        self.load_ontology()
    
    def _load_catalog(self, catalog_path: Path) -> dict[str, Path]:
        """Return {iri: local_file_path} from a catalog-v001.xml."""
        mapping = {}
        tree = ET.parse(catalog_path)
        for elem in tree.getroot():
            name = elem.get("name")
            uri  = elem.get("uri")
            if name and uri:
                mapping[name] = catalog_path.parent / uri
        return mapping

    def _load_all_catalogs(self) -> dict[str, Path]:
        """Merge all catalog-v001.xml found recursively under current_dir."""
        mapping = {}
        current_dir = Path.cwd() 
        for catalog_path in current_dir.rglob("catalog-v001.xml"):
            mapping.update(self._load_catalog(catalog_path))
        return mapping

    def load_ontology(self):
        """
        Load the ontology into an RDF graph.
        """
        try:
            # I disabled catalog for now because there is an issue with the path 
            # for local_path in self._load_all_catalogs().values():
            #     if not local_path.exists():
            #         sys.stderr.write(
            #             f"\033[93m[~] Catalog entry not found, skipping: {local_path}\033[0m\n"
            #         )
            #         continue
            #     self.graph.parse(str(local_path))
            if not Path(self.ontology_path).is_file():
                raise FileNotFoundError(self.ontology_path)
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
