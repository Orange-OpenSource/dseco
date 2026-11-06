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

#truc malin trouvé sur https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
DATA_GENERATOR="$( cd "${DIR}/.." && pwd )"

which libontology-update > /dev/null
if [ $? -ne 0 ]; then
    echo "Error: libontology-update command not found in PATH, are you in the right virtualenv ?"
    exit 1
fi

#set -e
set -euo pipefail

. "${DATA_GENERATOR}"/functions.sh

# first testing sources little test
${DIR}/unittests.by_source.sh

# Then testing builder against datatest_rml.ttl
${DIR}/unittests.builder.sh

# Then testing queries
temp_directory=${TMPDIR:-/tmp/}
ontology_file_test=$(mktemp --tmpdir="${temp_directory}" sec_onto_ttl_tests.XXXXXX)

${DIR}/unittests.build_for_queries.sh "${ontology_file_test}"
${DIR}/unittests.queries.sh "${ontology_file_test}"
${DIR}/unittests.behave.sh "${ontology_file_test}"

echo "All tests passed successfully."
