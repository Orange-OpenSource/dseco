#!/usr/bin/env python3

# This program receives a directory as arg1, full of CycloneDX SBOM files
# It transforms all Routes values: strings become lists

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


from urllib.parse import unquote
import sys
import glob
import json
import argparse


class TransformSbom:
    def __init__(self, pattern, output_file):
        self.pattern = pattern
        self.output_file = output_file

    # I added this function to decode encoded URLs
    # We don't use it for now because apparently they are already decoded with transform
    # But at least if we ever need it, it's here
    def clean_urls(self, doc):
        if isinstance(doc, dict):
            for key, value in doc.items():
                doc[key] = self.clean_urls(value)
            return doc
        elif isinstance(doc, list):
            return [self.clean_urls(item) for item in doc]
        elif isinstance(doc, str):
            return unquote(doc)
        else:
            return doc

    def transform(self, doc):
        if "metadata" in doc and "properties" in doc["metadata"]:
            for prop in doc["metadata"]["properties"]:
                if prop.get("name") == "Routes" and isinstance(prop.get("value"), str):
                    # Transform the string into a list
                    prop["value"] = prop["value"].split()
        return doc

    def process(self):
        files = glob.glob(self.pattern)
        result = []
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                doc = json.load(f)
                result.append(self.transform(doc))
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", required=True, help="Input JSON file pattern")
    parser.add_argument("--output-file", required=True, help="Output JSON file")
    args = parser.parse_args()

    transformer = TransformSbom(args.pattern, args.output_file)
    transformer.process()
