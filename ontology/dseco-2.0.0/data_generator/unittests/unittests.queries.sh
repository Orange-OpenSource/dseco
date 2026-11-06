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

set -e

# Check that argument 1 is provided
if [ $# -lt 1 ]; then
    echo "Error: Argument 1 (input file) is mandatory"
    exit 1
fi
input_file="$1"


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
DATA_GENERATOR="$( cd "${DIR}/.." && pwd )"
. "${DATA_GENERATOR}"/functions.sh

# Find directories starting with "test_" or uc_ in the queries folder
test_directories=$(find "${DATA_GENERATOR}/queries" -type d \( -name "test_*" -o -name "uc_*" \) -exec realpath {} \; | sort)



for directory in ${test_directories}; do
    echo
    echo
    last_directory=$(basename "$directory")
    print_message info "Testing using ${last_directory} with input file ${input_file}..."

    diff_message="  vimdiff \"${directory}/test.csv\" /tmp/r.csv\n  libontology-query --ontology \"${input_file}\" --query \"${directory}/test.sparql\""

    # Perform the query
    libontology-query --ontology "${input_file}" --query "${directory}/test.sparql" > /tmp/r.csv

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
