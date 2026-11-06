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


# set -e

set -euo pipefail



# Set temp_directory to the value of TMPDIR or default to /tmp/
temp_directory=${TMPDIR:-/tmp}


#truc malin trouvé sur https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
DATA_GENERATOR_DIR="$( cd "${DIR}/.." && pwd )"
. "${DATA_GENERATOR_DIR}"/functions.sh

# Ensure cleanup is performed on script exit
trap cleanup_old_files EXIT

# Set the source directory
source_directory="${DATA_GENERATOR_DIR}/builder/sources"

# Check if all the turtle's mapping files are valid
print_message info "Validating RML mappings syntax in ${source_directory}"
for mapping_file in $(find ${source_directory} -type f -name "*.ttl"); do
    if ! libontology-validate --ontology "${mapping_file}" ; then
        print_message error "Invalid RML mapping file: ${mapping_file}"
        exit 1
    fi
echo ""
print_message info "All rml mappings files are valid in ${source_directory}"
echo ""
done

# Define environment variables
DATASET_FILE_CONTROL="${DATA_GENERATOR_DIR}/datatest_rml.ttl"

ontology_temp_file_base=$(mktemp --tmpdir="${temp_directory}" datatest_rml.ttl.XXXXXX)
ontology_temp_file="${ontology_temp_file_base}.ttl"

#Build the dataset from RML and save it temporarily
print_message info "Building the dataset from RML mappings into ${ontology_temp_file}"

# Very important to remove the old sources
rm -rf "${temp_directory}/sources"
cp -r "${source_directory}" "${temp_directory}"

# I need to change the current directory to be in the DATA_GENERATOR_DIR 
# because otherwise the relative path to dseco in headers will not work
cd ../

"${DATA_GENERATOR_DIR}/builder.sh" "${DATA_GENERATOR_DIR}/builder/retrievers/" "${ontology_temp_file}" "${DATA_GENERATOR_DIR}/builder/cleaners/"

print_message info "Checking ${DATASET_FILE_CONTROL} vs ${ontology_temp_file}"

# The `if` prevents set -e from aborting before we can report the result
if compare_message=$(libontology-compare --ontology1 "${DATASET_FILE_CONTROL}" --ontology2 "${ontology_temp_file}" 2>&1); then
    print_message success "The builder have created the latest datatest file"
    print_message success "${DATASET_FILE_CONTROL} is isomorphic to "
    print_message success "${ontology_temp_file} "
else
    print_message error "${compare_message}"
    print_message error "   help : vimdiff ${DATASET_FILE_CONTROL} ${ontology_temp_file}"
    exit 1
fi
echo " "
echo " "

# Return to the initial directory
cd ${DIR}

