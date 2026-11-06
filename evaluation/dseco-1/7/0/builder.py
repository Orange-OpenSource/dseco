#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
Module to generate the ontology from data in a json file.

This module provides an OntologyExtractor class that reads configuration from a YAML file,
reads the json, and retrieves ontology-related data using various plugins.
"""
import argparse
import logging
import sys
import subprocess
import tempfile
import os
from pathlib import Path
import yaml


from rdflib import Graph, OWL
from rdflib.namespace import RDF


# Set up colored logging output
logging.addLevelName(logging.INFO, "\033[1;36m[*]\033[1;0m")
logging.addLevelName(logging.WARNING, "\033[1;31m[-]\033[1;0m")
logging.addLevelName(logging.ERROR, "\033[1;31m[-]\033[1;0m")
logging.addLevelName(logging.DEBUG, "\033[1;32m[+]\033[1;0m")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class OntologyExtractor:
    """
    A class to extract ontology data using various plugins.

    This class orchestrates the extraction process by:
    - Reading configuration from a YAML file
    - Managing data retrieval limits
    - Supporting local or remote data sources
    - Executing multiple data retrieval plugins

    Attributes
    ----------
    config_file : str
        Path to the YAML configuration file
    no_limit : bool
        Flag to disable data retrieval limits
    local : bool
        Flag to use local files instead of remote sources
    config : Config
        Configuration manager instance
    config_data : dict
        Parsed YAML configuration data

    Methods
    -------
    __init__(config_file: str, no_limit: bool, local: bool)
        Initialize the extractor with configuration settings
    run()
        Execute the configured extraction plugins
    """

    def __init__(self, tmpdir, withstats, destination):
        """
        Construct all the necessary attributes for the OntologyExtractor object.

        Parameters
        ----------
        sources_folder : str
            Path to the sources folder
        withstats : bool
            Flag to indicate if stats should be generated
        destination : str
            Path to the destination file
        janus_json_path : str, optional
            Path to the cleaned janus JSON file
        """
        self.withstats = withstats
        self.destination = destination
        self.tmpdir = tmpdir

    def run(self):
        """Run the ontology creating process."""
        self.add_headers()
        self.add_patch_mykg()
        self.add_mapping()

    def add_headers(self):
        """Execute the ontology extraction process."""
        try:
            # Get the directory where this script is located
            current_dir = Path.cwd()
            file_name = current_dir / "builder/headers.ttl"
            with open(file_name, "r") as header_file:
                content = header_file.read()
            with open(self.destination, "w") as destination_file:
                destination_file.write(content)
        except FileNotFoundError:
            logger.error("The %s file was not found.", file_name)
            sys.exit(1)
        except PermissionError:
            logger.error("Permission denied when trying to read %s.", file_name)
            sys.exit(1)
        except Exception as exce:
            logger.error(
                "An unexpected error occurred while reading %s: %s", file_name, exce
            )
            sys.exit(1)

    def add_patch_mykg(self):
        """Execute the ontology extraction process."""
        try:
            # Get the directory where this script is located
            current_dir = Path.cwd()
            file_name = current_dir / "builder/patch_mykg.ttl"
            with open(file_name, "r") as patch_mykg_file:
                content = patch_mykg_file.read()
            with open(self.destination, "a") as destination_file:
                destination_file.write(content)
        except FileNotFoundError:
            logger.error("The %s file was not found.", file_name)
            sys.exit(1)
        except PermissionError:
            logger.error("Permission denied when trying to read %s.", file_name)
            sys.exit(1)
        except Exception as exce:
            logger.error(
                "An unexpected error occurred while reading %s: %s", file_name, exce
            )
            sys.exit(1)

    def stats(self, filettl):
        g = Graph()
        g.parse(filettl, format="turtle")
        # Compter les individus (de type owl:NamedIndividual)
        individus = 0
        for s, p, o in g.triples((None, RDF.type, OWL.NamedIndividual)):
            individus += 1
        logger.info(f"Individuals : {individus}")

        # Compter les relations (prédicats uniques)
        relations = set(p for s, p, o in g)
        # logger.info(f"Uniq relations : {len(relations)}")

        for rel in relations:
            rela = 0
            for s, p, o in g.triples((None, rel, None)):
                # ici on ne compte pas les individus
                if o != OWL.NamedIndividual:
                    rela += 1
            # logger.info(f"Relations {rel} : {rela}")

    def get_sources_list(self):
        """Retrieve the list of sources from the sources.yml file."""
        sources_file = Path(self.tmpdir) / "sources/sources.yml"
        with open(sources_file, "r") as sources:
            sources_list = yaml.load(sources, yaml.FullLoader)
            sources_list = sources_list["sources"]
            return sources_list

    def get_dict_variables(self):
        """Retrieve the dictionary of variables from the variables.yaml file."""
        with open(Path.cwd() / "variables.yaml", "r") as variables_file:
            variables = yaml.safe_load(variables_file)
            return variables["variables"]

    def process_rml_template(self, rml_file_path, TMPDIR, dict_variables):
        """Process RML template file by replacing variables"""
        with open(rml_file_path, "r") as file:
            content = file.read()
        content = content.replace("${TMPDIR}", TMPDIR)
        for variable, value in dict_variables.items():
            content = content.replace(f"${{{variable}}}", value)
        return content

    def add_mapping(self):
        """Retrieves data based on RML mapping files in the specified folder"""
        # Get the directory where this script is located
        current_dir = Path.cwd()
        rml_mapper_jar_path = current_dir / "builder/rmlmapper.jar"

        if not os.path.isdir(self.tmpdir):
            logger.error(f"The sources folder {self.tmpdir} does not exist")
            sys.exit(1)

        sources_list = self.get_sources_list()
        dict_variables = self.get_dict_variables()
        TMPDIR = os.getenv("TMPDIR", "/tmp")

        for source in sources_list:
            source_folder = Path(self.tmpdir) / "sources" / source
            if not os.path.isdir(source_folder):
                logger.error(f"The sources folder {source_folder} does not exist")
                sys.exit(1)

            mapping_folder = Path(source_folder) / "mapping_rml"
            for rml_file in Path(mapping_folder).glob("*.ttl"):
                logger.info(f"Processing mapping file: \033[1;31m{rml_file}\033[0m")

                # # Process the RML file as a template
                # processed_content = self.process_rml_template(rml_file, TMPDIR, serviceid)
                processed_content = self.process_rml_template(
                    rml_file, TMPDIR, dict_variables
                )

                # Create a temporary file with the processed content
                with tempfile.NamedTemporaryFile(
                    mode="w", delete=False, suffix=".ttl"
                ) as temp_rml_file:
                    temp_rml_file.write(processed_content)
                    temp_rml_file_path = temp_rml_file.name

                with tempfile.NamedTemporaryFile(
                    delete=True, suffix=".ttl"
                ) as temp_destination:
                    temp_destination_path = temp_destination.name

                    command = [
                        "java",
                        "-jar",
                        rml_mapper_jar_path,
                        "-m",
                        temp_rml_file_path,  # Use processed template file
                        "-o",
                        temp_destination_path,
                        # on enlève le format turtle parce que sinon on a des bugs pour les caractères encodés
                        # "-s", "turtle"
                    ]

                    try:
                        subprocess.run(command, check=True)
                        logger.info(
                            f"RML mapper successfully processed file {rml_file}"
                        )
                        if self.withstats:
                            self.stats(temp_destination.name)
                    except subprocess.CalledProcessError as e:
                        logger.error(
                            f"Error while processing mapping file {rml_file}: {e}"
                        )

                    finally:
                        os.unlink(temp_rml_file_path)
                        logger.debug(f"Cleaned up temporary file: {temp_rml_file_path}")

                    with open(temp_destination_path, "r") as temp_file:
                        content = temp_file.read()
                    with open(self.destination, "a") as destination_file:
                        destination_file.write(content)


def main():
    """Parse command line arguments and run the ontology extraction."""
    parser = argparse.ArgumentParser(description="Ontology Extractor for json data.")
    parser.add_argument("--tmpdir", help="temporary directory", required=True)
    parser.add_argument(
        "--stats", help="with stats", action="store_true", default=False
    )
    parser.add_argument(
        "--destination", help="file to save the ontology", required=True
    )

    args = parser.parse_args()

    extractor = OntologyExtractor(
        withstats=args.stats, destination=args.destination, tmpdir=args.tmpdir
    )
    extractor.run()


if __name__ == "__main__":
    main()
