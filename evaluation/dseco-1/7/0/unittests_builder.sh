#!/bin/bash

#
# Copyright (c) 2023-2025 Orange. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#     3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
#     This product includes software developed by Orange.
#     4. Neither the name of Orange nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Orange "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Orange BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#

set -e

#
# Copyright (c) 2024-2025. Orange. All rights reserved.
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

# Ensure cleanup is performed on script exit
trap cleanup_old_files EXIT

# Set the source directory
source_directory="${DIR}/builder/sources"

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
DATASET_FILE='datatest_rml.ttl'
# remove the copyright for the diff
DATASET_FILE_CONTROL="${temp_directory}/datatest_rml.control.ttl"
cat "${DATASET_FILE}" | sed '1,13'd > "${DATASET_FILE_CONTROL}"


ontology_temp_file_base=$(mktemp --tmpdir="${temp_directory}" datatest_rml.ttl.XXXXXX)
ontology_temp_file="${ontology_temp_file_base}.ttl"

#Build the dataset from RML and save it temporarily
print_message info "Building the dataset from RML mappings into ${ontology_temp_file}"

# Very important to remove the old sources
rm -rf "${temp_directory}/sources"
cp -r "${source_directory}" "${temp_directory}"


./builder.sh "builder/retrievers/" "${ontology_temp_file}" "builder/cleaners/"


# Check if the dataset file is exactly the same as the one in the repository
if diff -q "${DATASET_FILE_CONTROL}" "${ontology_temp_file}" ; then
    print_message success "The builder have created the latest datatest file"
    print_message success "${DATASET_FILE} gives ${DATASET_FILE_CONTROL} that is identical to "
    print_message success "${ontology_temp_file} "
else
    print_message error "${diff_message}"
    print_message error "   help : vimdiff ${DATASET_FILE} ${ontology_temp_file}"
    exit 1
fi
echo " "
echo " "

