#!/bin/bash


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

which libontology-update > /dev/null
if [ $? -ne 0 ]; then
    echo "Error: libontology-update command not found in PATH, are you in the right virtualenv ?"
    exit 1
fi


set -euo pipefail

# Check that argument 1 is provided
if [ $# -lt 1 ]; then
    echo "Error: Argument 1 (output file) is mandatory"
    exit 1
fi

# Set temp_directory to the value of TMPDIR or default to /tmp/
temp_directory=${TMPDIR:-/tmp/}



#truc malin trouvé sur https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
DATA_GENERATOR="$( cd "${DIR}/.." && pwd )"
. "${DATA_GENERATOR}"/functions.sh

# Define environment variables
QUERY_ENGINE=''
ONTOLOGY_FILE="${DATA_GENERATOR}/../dseco.ttl"
DATASET_FILE="${DATA_GENERATOR}/datatest_rml.ttl"


# Create temporary files for ontology and inferred ontology
ontology_temp_file_base=$(mktemp --tmpdir="${temp_directory}" sec_onto_ttl.XXXXXX)
ontology_temp_file="${ontology_temp_file_base}.ttl"

inf1="${ontology_temp_file%.ttl}.i1.ttl"
inf2="${ontology_temp_file%.ttl}.i2.ttl"
inf3="${ontology_temp_file%.ttl}.i3.ttl"
inf4="${ontology_temp_file%.ttl}.i4.ttl"
inf5="${ontology_temp_file%.ttl}.i5.ttl"

# Ensure cleanup is performed on script exit
trap cleanup_old_files EXIT




# Concatenate ontology.ttl and dataset.ttl
print_message info "Concatenating ${ONTOLOGY_FILE} and ${DATASET_FILE} into ${ontology_temp_file}"
cat ${ONTOLOGY_FILE} ${DATASET_FILE} | envsubst> "${ontology_temp_file}"

echo " "
echo " "


# Build inferences
# print_message info "Building inferences into ${inf1}"
#libontology-infer --ontology "${ontology_temp_file}" --destination "${inf1}" --reasoner hermit

# Copy the ontology to inf1
print_message info "Copying ${ontology_temp_file} to ${inf1}"
cp "${ontology_temp_file}" "${inf1}"


echo " "
echo " "

# Build inferences by INSERT WHERE
print_message info "Building inferences add one prop"

source "${DATA_GENERATOR}/builder_functions.sh"
ontology_update "${inf1}" "${inf2}"

# # Here we choose the one that goes to tests
final_ontology_temp_file="${inf2}"


# Exit on error
set -e

arg1="$1"
mv "${final_ontology_temp_file}" "${arg1}"
# Test the inferred ontology
print_message info "outputing on ${arg1} ..."





