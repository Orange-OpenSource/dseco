#!/usr/bin/env python3

# This program receive a file as arg1, a json list of cyclone dx sbom
# it changes all the bom ref by a sha256

#
# Copyright (c) 2023-2026 Orange. All rights reserved.
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

import sys
import json
import argparse
import hashlib
from unittest import result


class TransformSbomSha256:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def hash_bomref(self, value):
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def add_sha_to_bomrefs(self, obj):
        """Ajoute bom_ref_sha à tous les objets avec bom-ref, ref ou component_bom_ref."""
        if isinstance(obj, dict):
            new_obj = {}
            for k, v in obj.items():
                if k in ("bom-ref", "ref") and isinstance(v, str):
                    new_obj[k] = v
                    new_obj["bom_ref_sha"] = self.hash_bomref(v)
                elif k == "component_bom_ref" and isinstance(v, str):
                    new_obj[k] = v
                    new_obj["component_bom_ref_sha"] = self.hash_bomref(v)
                elif k == "dependsOn" and isinstance(v, list):
                    new_obj[k] = [self.hash_bomref(dep) for dep in v]
                else:
                    new_obj[k] = self.add_sha_to_bomrefs(v)
            return new_obj
        elif isinstance(obj, list):
            return [self.add_sha_to_bomrefs(item) for item in obj]
        return obj

    def transform_sbom(self, sbom):
        """Transforme un SBOM et ajoute bom_ref_sha_parent aux composants."""
        sbom = self.add_sha_to_bomrefs(sbom)
        
        parent_sha = sbom.get("metadata").get("component").get("bom_ref_sha")
        if parent_sha and "components" in sbom:
            for component in sbom["components"]:
                component["bom_ref_sha_parent"] = parent_sha
        
        return sbom

    def process(self):
        with open(self.input_file, "r", encoding="utf-8") as input_file:
            doc = json.load(input_file)
        
        result = [self.transform_sbom(sbom) for sbom in doc] if isinstance(doc, list) else self.transform_sbom(doc)
        
        with open(self.output_file, "w", encoding="utf-8") as output_file:
            json.dump(result, output_file, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", required=True, help="Fichier JSON d'entrée")
    parser.add_argument("--output-file", required=True, help="Fichier JSON de sortie")
    args = parser.parse_args()

    transformer = TransformSbomSha256(args.input_file, args.output_file)
    transformer.process()
