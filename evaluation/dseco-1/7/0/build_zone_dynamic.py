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
Module to generate zone data dynamically from a JSON file.

This module extracts domain information from a JSON file, filters out domains already 
present in a static reference file, and prepares the data for integration with 
an RML mapping process. It handles the conversion from JSONL format to standard JSON
and renames domain keys to match ontology requirements.

The primary purpose is to identify domains that aren't managed by Top or Int,
marking them as "managedBySomeoneElse" for the security ontology.
"""

import argparse
import logging
import duckdb
import json

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


class BuildZoneDynamic:
    """
    A class to build dynamic zone data for ontology creation.

    This class extracts domain information from JSON data, filters for active domains
    that are not already present in a static reference file, normalizes domain names,
    and reformats the data to be compatible with RML mapping tools.

    Attributes
    ----------
    json_file : str
        Path to the input JSON file containing domain records.
    zone_dynamic_file : str
        Path to the output file where processed zone data will be saved.
    zone_static_file : str
        Path to the static reference file containing domains to be excluded.

    Methods
    -------
    build_zone_dynamic_file()
        Extract distinct active domains from the input JSON file, excluding those in the static file.
    get_static_zone()
        Load and process domains from the static reference file.
    jsonl_to_json()
        Convert JSONL format to JSON and rename the domain key to managedBySomeoneElse.
    """

    def __init__(self, tmpdir):
        """
        Construct all the necessary attributes for the BuildzoneDynamic object.

        Parameters
        ----------
        json_file : str
            Path to the input JSON file containing domain records.
        zone_dynamic_file : str
            Path to the output file where processed zone data will be saved.
        """

        self.json_file = f"{tmpdir}/janus.json"
        self.zone_dynamic_file = f"{tmpdir}/zone_dynamic.json"
        self.zone_static_file = f"{tmpdir}/zone_static.json"



    def build_zone_dynamic_file(self):
        """
        Extract distinct active domains from the input JSON file.
        
        This method:
        1. Loads the input JSON file into a DuckDB table
        2. Retrieves the list of static domains to exclude
        3. Creates a table of these static domains
        4. Executes a SQL query to select active domains not in the static list
        5. Outputs the results to a JSON file
        
        The SQL query filters domains that:
        - Are marked as active (isAlive = true)
        - Are not error values (domain != 'ERROR')
        - Do not exist in the static domains list
        
        Raises
        ------
        Exception
            If there's an error writing to the output file
        """
        con = duckdb.connect()
        con.execute(
            f"CREATE TABLE temp_json_file AS SELECT * FROM read_json('{self.json_file}')"
        )

        static_domains = self.get_static_zone()
        con.execute(
                f"CREATE TABLE static_domains AS SELECT unnest({static_domains}) as domain"
            )

        query = """
                SELECT DISTINCT temp.domain 
                FROM temp_json_file AS temp
                WHERE temp.isAlive = true
                AND temp.domain != 'ERROR'
                AND NOT EXISTS (
                    SELECT * FROM static_domains 
                    WHERE static_domains.domain = temp.domain
                )
            """

        con.execute("CREATE TABLE zone_dynamic AS " + query)
        try:
            con.execute(f"COPY zone_dynamic TO '{self.zone_dynamic_file}' (FORMAT JSON)")
            logger.info(f"{self.zone_dynamic_file} has been sucessfully built.")
        except Exception as e:
            logger.error(f"Error while building {self.zone_dynamic_file}: {e}")
    

    def get_static_zone(self):
        """
        Load and process domains from the static reference file.
        
        This method:
        1. Reads the static zone data file
        2. Extracts all domain values regardless of their key names
        3. Normalizes domains by removing trailing dots
        4. Returns a list of domain names to exclude
        
        Returns
        -------
        list
            A list of domain names (strings) from the static file
        """

        with open(self.zone_static_file, "r") as static_file:
            static_data = json.load(static_file)
        
        static_domains = []
        for record in static_data:
            for key in record.keys():
                domain = record[key]
                if domain.endswith('.'):
                    domain = domain[:-1]
                static_domains.append(domain)
        return static_domains


    def jsonl_to_json(self):
        """
        Convert JSONL format to JSON and rename the domain key to managedBySomeoneElse.
        
        This method:
        1. Reads the JSONL file produced by DuckDB
        2. Converts each line to a JSON object
        3. Renames the "domain" key to "managedBySomeoneElse"
        4. Adds a trailing dot to domain names
        5. Writes the data back as a properly formatted JSON array
        
        Raises
        ------
        Exception
            If there's an error reformatting or writing the JSON file
        """

        with open(self.zone_dynamic_file, "r") as zone_file:
            data = []
            for line in zone_file:
                record = json.loads(line)
                record["managedByExt"] = record["domain"] + '.'
                del record["domain"]  
                data.append(record)

        with open(self.zone_dynamic_file, "w") as zone_file:
            try:
                json.dump(data, zone_file, indent=4)
                logger.info(f"{self.zone_dynamic_file} has been reformated to json format.")
            except Exception as e:
                logger.error(f"Error while reformating {self.zone_dynamic_file}: {e}")


def main():
    """Parse command line arguments and run the builder."""
    parser = argparse.ArgumentParser(
        description="Generate dynamic zone data from JSON."
    )
    parser.add_argument("--tmpdir", help="Temporary directory for input and output files", required=True)

    args = parser.parse_args()

    builder = BuildZoneDynamic(
        tmpdir=args.tmpdir
    )
    builder.build_zone_dynamic_file()
    builder.jsonl_to_json()


if __name__ == "__main__":
    main()
