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
Module to clean our janus json file.
"""
import argparse
import logging
import json
import yaml
import ipaddress
import urllib.parse

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


class AddIpPartOfSubnet:
    """
    A class to clean data before creating our ontology.

    Attributes
    ----------
    json_file : str
        Path to the json file.

    Methods
    -------
    __init__(json_file: str)
        Initialize the subnet_manager with json_file
    clean()
        Clean all the unwanted data.
    """

    def __init__(self, tmpdir, destination):
        """
        Construct all the necessary attributes for the CleanJson object.

        Parameters
        ----------
        json_file : str
            Path to the json file.
        """
        self.janus = f"{tmpdir}/janus.json"
        self.subnets_file = f"{tmpdir}/subnets.json"
        self.destination = destination

    def get_subnets_list(self):
        with open(self.subnets_file, "r") as subnets_file:
            subnets_list = json.load(subnets_file)
        return subnets_list
    
    def get_ip_list(self):
        ip_list = []
        with open(self.janus, 'r') as janus_file:
            records = json.load(janus_file)
            for record in records:
                if record['recordtype'] in ('A RECORD', 'AAAA RECORD') and record['isAlive'] == True:
                    ip_list.append(record['recordtarget'])
            ip_list = list(set(ip_list))
            return ip_list

    
    def add_is_part_of(self):
        """A function to add is_part_of relation to the turtle file."""
        subnets_list = self.get_subnets_list()
        ip_list = self.get_ip_list()

        #This code isn't optimal but it's fast enough
        for ip in ip_list:
            ip = ipaddress.ip_address(ip)
            for subnet in subnets_list:
                subnet = subnet["prefix"]
                network = ipaddress.ip_network(subnet)
                if ip in network:
                    with open(self.destination, 'a') as destination_file:
                        destination_file.write(f"<https://w3id.org/dseco/mykg/IP_{ip}> a owl:NamedIndividual , observable:IPAddress .\n")
                        destination_file.write(f"<https://w3id.org/dseco/mykg/IP_{ip}> dseco:is_part_of <https://w3id.org/dseco/mykg/SUBNET_{subnet}> .\n")

def main():
    """Parse command line arguments and run the subnet_manager."""
    parser = argparse.ArgumentParser(
        description="A class to add subnets into our ontology."
    )
    parser.add_argument("--tmpdir", help="Temporary directory for input and output files", required=True)
    parser.add_argument("--destination", help="file to save the ontology", required=True)

    args = parser.parse_args()

    is_part_of_manager = AddIpPartOfSubnet(
        tmpdir=args.tmpdir,
        destination=args.destination
    )

    is_part_of_manager.add_is_part_of()


if __name__ == "__main__":
    main()