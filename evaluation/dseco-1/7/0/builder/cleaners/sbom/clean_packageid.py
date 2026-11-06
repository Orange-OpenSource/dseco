#!/usr/bin/env python3

# This program receive a directory as arg1, full of cyclonedx sbom
# it changes all the Routes : string becomes list

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


import argparse
import json
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode
import json


class PackageIdCleaner:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def clean_url(self, url):
        url = urlparse(url)
        # Filtre tous les paramètres sauf package-id
        query_params = [(k, v) for k, v in parse_qsl(url.query) if k != "package-id"]
        query = urlencode(query_params)
        cleaned = urlunparse(
            (url.scheme, url.netloc, url.path, url.params, query, url.fragment)
        )
        return cleaned

    def get_data(self, file):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def clean_data(self, data):
        # Clean all the fields bom-ref
        if isinstance(data, dict):
            new_data = {}
            for key, value in data.items():
                if (key == "bom-ref" or key == "ref") and isinstance(value, str):
                    new_data[key] = self.clean_url(value)
                elif key == "dependsOn" and isinstance(value, list):
                    new_data[key] = [self.clean_url(ref) for ref in value]
                else:
                    new_data[key] = self.clean_data(value)
            return new_data
        elif isinstance(data, list):
            return [self.clean_data(item) for item in data]
        else:
            return data

    def process(self):
        data = self.get_data(self.input_file)
        # Clean all the fields bom-ref
        data = self.clean_data(data)
        with open(self.output_file, "w", encoding="utf-8") as output_file:
            json.dump(data, output_file, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", required=True, help="Fichier JSON d'entrée")
    parser.add_argument("--output-file", required=True, help="Fichier JSON de sortie")
    args = parser.parse_args()

    cleaner = PackageIdCleaner(args.input_file, args.output_file)
    cleaner.process()
