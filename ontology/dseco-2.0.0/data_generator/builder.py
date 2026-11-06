#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
from jinja2 import Template
from concurrent.futures import ProcessPoolExecutor, as_completed

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
    """

    def __init__(self, tmpdir, withstats, workers, destination):
        """
        Construct all the necessary attributes for the OntologyExtractor object.
        """
        self.withstats = withstats
        self.destination = destination
        self.workers = workers
        self.tmpdir = tmpdir
        self.dict_variables = self.get_dict_variables(self.tmpdir)

    def run(self):
        """Run the ontology creating process."""
        self.add_headers(self.dict_variables)
        self.add_patch_mykg()
        self.add_mapping(self.dict_variables, self.workers)

    def add_headers(self,dict_variables):
        """Execute the ontology extraction process."""
        try:
            script_dir = Path(__file__).resolve().parent
            file_name = script_dir / "builder/headers.ttl"
            with open(file_name, "r") as header_file:
                headers_content_with_template = header_file.read()
            template = Template(headers_content_with_template)
            final_content = template.render(**dict_variables)
            with open(self.destination, "w") as destination_file:
                destination_file.write(final_content)
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
            script_dir = Path(__file__).resolve().parent
            file_name = script_dir / "builder/patch_mykg.ttl"
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
        return individus


    def get_sources_list(self, sources_file):
        """Retrieve the list of sources from the sources.yml file."""
        with open(sources_file, "r") as sources:
            sources_list = yaml.load(sources, yaml.FullLoader)
            sources_list = sources_list["sources_enabled"]
            return sources_list

    def get_dict_variables(self, TMPDIR):
        """Retrieve the dictionary of variables from the variables.yaml file."""
        current_dir = Path()
        variables_file_path = current_dir / "variables.yaml"
        with open(variables_file_path, "r") as variables_file:
            content_with_template = variables_file.read()
        template = Template(content_with_template)
        final_content = template.render(TMPDIR=TMPDIR)
        variables = yaml.safe_load(final_content)
        return variables["variables"]

    def process_rml_template(self, rml_file_path, dict_variables):
        """Process RML template file by replacing variables"""
        with open(rml_file_path, "r") as rml_file:
            rml_content_with_template = rml_file.read()
        template = Template(rml_content_with_template)
        final_content = template.render(**dict_variables)
        return final_content

    def get_rml_files_to_process(self, sources_list):
        """Get the list of RML files to process based on the sources list."""
        rml_files_to_process = []
        for source in sources_list:
            source_folder = Path(self.tmpdir) / "sources" / source
            if not os.path.isdir(source_folder):
                logger.error(f"(get_rml_files_to_process) The sources folder {source_folder} does not exist")
                sys.exit(1)

            mapping_folder = Path(source_folder) / "mapping_rml"
            for rml_file in Path(mapping_folder).glob("*.ttl"):
                rml_files_to_process.append(rml_file)
        return rml_files_to_process

    def process_single_rml_file(self, rml_file_path, dict_variables, rml_mapper_jar_path, withstats):
        """
        Process a single RML file. This function is defined at module level
        to be picklable for ProcessPoolExecutor.
        """
        try:
            processed_content = self.process_rml_template(rml_file_path, dict_variables)  
            
            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".ttl"
            ) as temp_rml_file:
                temp_rml_file.write(processed_content)
                temp_rml_file_path = temp_rml_file.name
            
            # Create temporary output file
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".ttl"
            ) as temp_destination:
                temp_destination_path = temp_destination.name
            
            command = [
                "java",
                "-jar",
                str(rml_mapper_jar_path),
                "-m",
                temp_rml_file_path,
                "-o",
                temp_destination_path,
            ]
            
            try:
                subprocess.run(command, check=True, capture_output=True)
                
                with open(temp_destination_path, "r") as temp_file:
                    content = temp_file.read()
                
                if withstats:
                    individus_count = self.stats(temp_destination_path)
                    logger.debug(
                        f"RML mapper successfully processed file \033[1;31m{rml_file_path}\033[0m\n"
                        f"\033[1;36m[*]\033[1;0m Individuals : {individus_count}\n"
                    )

                return content
                
            except subprocess.CalledProcessError as e:
                logger.error(f"Error while processing mapping file {rml_file_path}: {e}")
                    
        except Exception as e:
            logger.error(f"Error while processing mapping file {rml_file_path}: {e}")         
    
    def add_mapping(self, dict_variables, workers):
        """
        Retrieves data based on RML mapping files in the specified folder.
        Uses ProcessPoolExecutor for parallel processing.
        """
        script_dir = Path(__file__).resolve().parent
        rml_mapper_jar_path = script_dir / "builder/rmlmapper.jar"
        sources_list = self.get_sources_list("sources.yml")

        if not os.path.isdir(self.tmpdir):
            logger.error(f"(add_mapping) The sources folder {self.tmpdir} does not exist")
            sys.exit(1)

        rml_files_to_process = self.get_rml_files_to_process(sources_list)

        logger.info(f"Found {len(rml_files_to_process)} RML files to process\n")

        results = []
        with ProcessPoolExecutor(workers) as executor:
            future_to_file = {
                executor.submit(self.process_single_rml_file, rml_file, dict_variables, rml_mapper_jar_path, self.withstats): rml_file
                for rml_file in rml_files_to_process
            }
            
            for future in as_completed(future_to_file):
                results.append(future.result())

        with open(self.destination, "a") as destination_file:
            destination_file.write("\n".join(results))




def main():
    """Parse command line arguments and run the ontology extraction."""
    parser = argparse.ArgumentParser(description="Ontology Extractor for json data.")
    parser.add_argument("--tmpdir", help="temporary directory", required=True)
    parser.add_argument(
        "--stats", help="with stats", action="store_true", default=False
    )
    parser.add_argument(
        "--workers", help="number of workers for parallel processing", type=int, default=10
    )
    parser.add_argument(
        "--destination", help="file to save the ontology", required=True
    )

    args = parser.parse_args()

    extractor = OntologyExtractor(
        withstats=args.stats, destination=args.destination, tmpdir=args.tmpdir, workers=args.workers
    )
    extractor.run()


if __name__ == "__main__":
    main()
