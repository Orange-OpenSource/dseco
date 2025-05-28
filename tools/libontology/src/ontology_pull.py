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
ontology_pull.py
Script to download and update an ontology from a given URL.
"""

import os
import sys
import configparser
import requests


class OntologyPull:
    """
    Class to handle the downloading and updating of an ontology.
    """

    def __init__(self, config_path):
        """
        Initialize the OntologyPull with the given configuration.

        Parameters
        ----------
        config_path : str
            Path to the configuration file.
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.url = self.config.get("Ontology", "update-url")
        self.destination = self.config.get("Ontology", "update-destination")
        self.cacert = self.config.get(
            "DEFAULT", "cacert", fallback="/etc/ssl/certs/ca-certificates.crt"
        )

    def download_ontology(self):
        """
        Download the ontology from the configured URL and save it to the configured destination.
        """
        try:

            response = requests.get(self.url, verify=self.cacert)
            response.raise_for_status()
            with open(self.destination, "wb") as file:
                file.write(response.content)
            sys.stdout.write(
                f"\033[92m[+] Ontology downloaded and saved to {self.destination}\033[0m\n"
            )
        except requests.exceptions.RequestException as e:
            sys.stderr.write(f"\033[91m[-] Error downloading ontology: {e}\033[0m\n")
            sys.exit(1)
        except IOError as e:
            sys.stderr.write(f"\033[91m[-] I/O Error: {e}\033[0m\n")
            sys.exit(1)


def main():
    """Main function to execute the ontology update process."""
    config_path = os.getenv("CONFIG_FILE")
    ontology_pull = OntologyPull(config_path)
    ontology_pull.download_ontology()


if __name__ == "__main__":
    main()
