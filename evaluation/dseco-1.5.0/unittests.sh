#!/bin/bash

set -e

#
# Copyright (c) 2024. Orange. All rights reserved.
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


# Set temp_directory to the value of TMPDIR or default to /tmp/
temp_directory=${TMPDIR:-/tmp/}



#truc malin trouvé sur https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
. "${DIR}"/functions.sh

# Define environment variables
QUERY_ENGINE=''
ONTOLOGY_FILE='../../ontology/dseco-1.5.0/dseco.ttl'
DATASET_FILE='./datatest.ttl'


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
cat ${ONTOLOGY_FILE} ${DATASET_FILE} > "${ontology_temp_file}"

echo " "
echo " "


# Build inferences
print_message info "Building inferences into ${inf1}"
libontology-infer --ontology "${ontology_temp_file}" --destination "${inf1}"

echo " "
echo " "

# Build inferences by INSERT WHERE
print_message info "Building inferences add one prop"
libontology-update --ontology "${inf1}" --query queries_update/isinOurSubnet2.sparql --destination "${inf2}"

print_message info "Building inferences add classe and individuals"
libontology-update --ontology "${inf2}" --query queries_update/add_class_x0.sparql --destination "${inf3}"
libontology-update --ontology "${inf3}" --query queries_update/add_class_x1.sparql --destination "${inf4}"
libontology-update --ontology "${inf4}" --query queries_update/add_class_x2.sparql --destination "${inf5}"



# Here we choose the one that goes to tests
final_ontology_temp_file="${inf5}"


# Exit on error
set -e

# Find directories starting with "test_" or uc_
test_directories=$(find . -type d \( -name "test_*" -o -name "uc_*" \) -exec realpath {} \; | sort)

# Test the inferred ontology
print_message info "Testing on ${final_ontology_temp_file} ..."





for directory in ${test_directories}; do
    echo
    print_message info "Testing using ${directory}..."

    diff_message="  vimdiff \"${directory}/test.csv\" /tmp/r.csv\n  libontology-query --ontology \"${final_ontology_temp_file}\" --query \"${directory}/test.sparql\""

    # Perform the query
    libontology-query --ontology "${final_ontology_temp_file}" --query "${directory}/test.sparql" > /tmp/r.csv

    # Diff the results and handle errors
    if diff -q "${directory}/test.csv" /tmp/r.csv; then
        print_message success "Test ${directory} OK"
    else
        print_message error "${diff_message}"
        exit 1
    fi
    echo " "
    echo " "
done

print_message info "concatene : export C1=${ontology_temp_file}"
print_message info "concatene : export I1=${inf1}"
print_message info "concatene : export I2=${inf2}"
print_message info "concatene : export I3=${inf3}"
print_message info "concatene : export I4=${inf4}"
print_message info "concatene : export I5=${inf5}"
print_message info "concatene : export F1=${final_ontology_temp_file}"
print_message info 'libontology-query --ontology $F1  --query  queries/test_list_all_IP_Address/test.sparql'


# The cleanup will be triggered by the trap on script exit
