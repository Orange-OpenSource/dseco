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

SBOM_ROUTES=$(mktemp -t sbom_routes.XXXX)
SBOM_COMPO=$(mktemp -t sbom_compo.XXXX)

# Temporary file to store intermediate results
F1=$(mktemp)
F2=$(mktemp)


# STEP 1
# We clean field value for "route" entry by splitting it
./builder/cleaners/sbom/transform_sbom.py --pattern "$1/sbom_routes_*.json" --output-file $SBOM_ROUTES
./builder/cleaners/sbom/transform_sbom.py --pattern "$1/sbom_components_*.json" --output-file $SBOM_COMPO

# STEP 2
# I put this step in comment for now because it is useless at the moment
# clean package-id by removing them from the bom-ref field
# For now, I suppose that we retrieved the input files and put them in the tmpdir folder
# But we can imagine to retrieve them from builder/sources/sbom, but we should keep in mind that these files are very large
# ./builder/cleaners/sbom/clean_packageid.py --input-file $F1 --output-file $SBOM_ROUTES
# ./builder/cleaners/sbom/clean_packageid.py --input-file $F2 --output-file $SBOM_COMPO

# STEP 3
# We add sha256 in bom_ref_sha field to help rml process
./builder/cleaners/sbom/transform_sbomref_sha256.py --input-file $SBOM_ROUTES --output-file $1/sbom_routes_sha.json
./builder/cleaners/sbom/transform_sbomref_sha256.py --input-file $SBOM_COMPO --output-file $1/sbom_components_sha.json