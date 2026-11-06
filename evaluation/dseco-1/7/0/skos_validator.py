#!/usr/bin/env python3

#
# Copyright (c) 2025. Orange. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#     1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#     3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
#       This product includes software developed by Orange.
#     4. Neither the name of Orange nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Orange "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Orange BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

"""
SKOS Ontology Validation - Examples Verification
This script analyzes a SKOS ontology and verifies that concepts have appropriate examples.
"""

import rdflib
from rdflib import RDF, RDFS, OWL, Namespace
import argparse
import sys
import json
import os

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DSECO = Namespace("https://w3id.org/dseco/ontology/")

class SKOSValidator:
    def __init__(self, ontology):
        self.graph = rdflib.Graph()
        self.ontology_file = ontology
        
    
    def load_ontology(self):
        try:
            self.graph.parse(self.ontology_file, format='turtle')
        except Exception as e:
            print(f"Error while loading the ontology : {e}")
            sys.exit(1)
    
    def count_examples(self):
        count_skos_examples = 0
        for subject, predicate, obj in self.graph:
            if predicate == SKOS.example:
                count_skos_examples += 1
        return count_skos_examples
    
    def count_classes(self):
        count_classes = 0
        for classe in self.graph.subjects(RDF.type, OWL.Class):
            if str(classe).startswith(str(DSECO)):
                count_classes += 1
        return count_classes
    
    def count_object_properties(self):
        count_object_properties = 0
        for prop in self.graph.subjects(RDF.type, OWL.ObjectProperty):
            if str(prop).startswith(str(DSECO)):
                count_object_properties += 1
        return count_object_properties
    
    def count_datatype_properties(self):
        count_datatype_properties = 0
        for prop in self.graph.subjects(RDF.type, OWL.DatatypeProperty):
            if str(prop).startswith(str(DSECO)):
                count_datatype_properties += 1
        return count_datatype_properties
    
    def validate_skos_examples(self):
        self.load_ontology()
        
        count_skos_examples = self.count_examples()
        count_classes = self.count_classes()
        count_object_properties = self.count_object_properties()
        count_datatype_properties = self.count_datatype_properties()
        
        print(f"Number of SKOS concepts with examples: {count_skos_examples}")
        print(f"Number of OWL classes: {count_classes}")
        print(f"Number of OWL object properties: {count_object_properties}")
        print(f"Number of OWL datatype properties: {count_datatype_properties}")
        
        return count_skos_examples == count_classes+count_object_properties+count_datatype_properties

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SKOS Ontology Validation - Examples Verification")
    parser.add_argument("--ontology", required=True, help="Path to the SKOS ontology file in Turtle format (.ttl)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.ontology):
        print(f"The ontology file {args.ontology} does not exist.")
        sys.exit(1)
    
    validator = SKOSValidator(args.ontology)
    if validator.validate_skos_examples():
        print("Validation successful: all SKOS concepts have appropriate examples.")
    else:
        print("Validation failed: some SKOS concepts do not have appropriate examples.")
        sys.exit(1)

