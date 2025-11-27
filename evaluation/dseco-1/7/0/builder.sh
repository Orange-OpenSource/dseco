#!/bin/bash

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

set -e 

# Functions declarations 

function check_tmpdir(){
    if [ -z "$TMPDIR" ]; then
        TMPDIR="/tmp"
    fi
}

function get_script_dir(){
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    echo $SCRIPT_DIR
}

function check_input_variables(){
    if [ -z "$retrievers_folder" ] || [ -z "$out_file" ] || [ -z "$cleaners_folder" ]; then
        echo "Usage: $0 <retrievers_folder> <output_ontology_file> <cleaners_folder>"
        exit 1
    fi
}


# Variables initialization
check_tmpdir
SCRIPT_DIR=$(get_script_dir)
PROFILING_FILE=${TMPDIR}/profiling.log
F1=$(mktemp)

# Sourcing out of script functions 
source "${SCRIPT_DIR}/functions.sh"
source "${SCRIPT_DIR}/builder_functions.sh"

# Redirect script output in terminal + profiling file
exec > >(tee "$PROFILING_FILE")
exec 2>&1

# Main build script

print_message step "Step 1: Initializing variables and checking input parameters"

retrievers_folder="$1" # Folder containing retrievers
out_file="$2" # Output ontology file
cleaners_folder="$3" # Folder containing cleaners

check_input_variables

print_message step "Step 2: Converting dseco.ttl to dseco.xml"
# We create each time the xml version, we copy it next to dseco.ttl but it is in the git ignore not ro be commited
libontology-convert-ttl-to-xmlrdf --ontology "${SCRIPT_DIR}/../dseco.ttl"  --destination "${TMPDIR}/dseco.xml"
cp "${TMPDIR}/dseco.xml" "${SCRIPT_DIR}/../"

print_message step "Step 3: Running retrievers from folder: $retrievers_folder"
# Run all retrievers
run_all_retrievers

print_message step "Step 4: Running cleaners from folder: $cleaners_folder"
# Run all cleaners
run_all_cleaners


#clean main data
# ./builder/sources/janus/cleaner.sh "${TMPDIR}/janus.json"  #I did the same thing as retrievers

print_message step "Step 5: Building dynamic zones"

#Source 6 : complete data
#Build dynamic zone file 
"${SCRIPT_DIR}/build_zone_dynamic.py" --tmpdir "${TMPDIR}"

print_message step "Step 6: Main build of the ontology"

#Main build of the ontology
"${SCRIPT_DIR}/builder.py"  --tmpdir "${TMPDIR}" --stats --destination "${out_file}"

print_message step "Step 7: Adding triplets to the ontology"

"${SCRIPT_DIR}/builder/add_triplets/add_ip_part_of_subnet.py" --tmpdir "${TMPDIR}" --destination "${out_file}" 

print_message step "Step 8: Inferring the ontology"

#Infer on the ontology using hermit
### We are using pellet for now because it has more error explanations and extends inferences on datatype properties
#libontology-infer --ontology "${out_file}" --destination "${F1}" --reasoner pellet
libontology-infer --ontology "${out_file}" --destination "${F1}" --reasoner pellet 2>&1 | grep -E "(Owlready)" 
mv "${F1}"  "${out_file}"

print_message step "Step 9: Updating the ontology"

#Update the ontology
ontology_update "${out_file}" "${F1}"
mv "${F1}"  "${out_file}"

print_message step "End of the build process. Output file: $out_file"

# End of build script

# Example usage:
# ./builder.sh "retrievers_folder" "output_ontology.ttl" "cleaners_folder"

