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

# This script updates an ontology using a series of queries stored in a specified folder.
# It takes an input ontology file and produces an updated output ontology file.
# Usage: ./script_name.sh input_ontology_file output_ontology_file

set -euo pipefail

# Define the folder containing query files

#truc malin trouvé sur https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
DATA_GENERATOR_DIR="$( cd "${DIR}" && pwd )"

folder_path="${DATA_GENERATOR_DIR}/queries_update"

if [ ! -d "$folder_path" ]; then
  echo "Erreur : le dossier des requêtes '$folder_path' n'existe pas" >&2
  exit 1
fi




# Function to update the ontology using queries
# Arguments:
#   $1 - Input ontology file
#   $2 - Output ontology file
function ontology_update() {
  local in_file="$1"  # Input ontology file
  local out_file="$2" # Output ontology file

  # Create a temporary file to hold the ontology
  local F1
  F1=$(mktemp)
  cp -a "${in_file}" "${F1}"

  # Iterate over each query file in the specified folder
  for file in $(find "$folder_path" -type f | sort); do
    local F2
    F2=$(mktemp)  # Create a temporary file for the output of the update

    # Log the update process
    echo -e "updating ontology $F1 by using the query $file destination $F2"
    
    # Update the ontology using the current query
    libontology-update --ontology "${F1}" --query "${file}" --destination "${F2}"
    
    # Move the updated ontology back to the temporary file
    mv "${F2}" "${F1}"
    echo -e "update ${file} done\n"
  done

  # Move the final updated ontology to the specified output file
  mv "${F1}" "${out_file}"
}


function add_metadata () {
  TEMP_FILE=$(mktemp)
  local TMPDIR="$1"
  local FOLDER_NAME="$2"
  local CURRENT_DATE=$(date +"%Y-%m-%d %H:%M:%S")

  cat > $TEMP_FILE << EOF
  ### File: $(basename ${TMPDIR}/${FOLDER_NAME}/onto.ttl)
  ### Project: ${CI_PROJECT_NAME}
  ### Generation Date: ${CURRENT_DATE}
  ### Branch: ${CI_COMMIT_REF_NAME}
  ### BY: ${CI_COMMIT_AUTHOR}
  ###
  ### This file was generated automatically.

EOF

  cat ${TMPDIR}/${FOLDER_NAME}/onto.ttl >> $TEMP_FILE
  mv $TEMP_FILE ${TMPDIR}/${FOLDER_NAME}/onto.ttl
}

#Make sur to have yq installed
function get_sources_list() {
  local yaml_file="$1"
  sources_folders=$(yq -r '.sources_enabled[]' "$yaml_file" 2>/dev/null) 
  echo "$sources_folders" 
}

function run_all_retrievers() {
  # Enable retrievers based on the YAML configuration
  enabled_retrievers=$(get_sources_list "sources.yml")
  if [ -z "$enabled_retrievers" ]; then
    echo "No retrievers enabled in sources.yml"
    return
  fi

  for enabled_retriever in $enabled_retrievers; do
    if [ ! -d "${retrievers_folder}/${enabled_retriever}" ]; then
        echo "Retriever folder ${retrievers_folder}/${enabled_retriever} does not exist. Skipping."
        continue
    fi
    for retriever_file in $(find "${retrievers_folder}/${enabled_retriever}" -type f -name "retriever.sh" | sort); do
      echo "Running retriever script: ${retriever_file}"
      source "${retriever_file}" "${TMPDIR}" "${DATA_GENERATOR_DIR}"
    done
  done
  
}

function run_all_cleaners() {
  # Enable cleaners based on the YAML configuration
  enabled_cleaners=$(get_sources_list "sources.yml")
  if [ -z "$enabled_cleaners" ]; then
    echo "No cleaners enabled in sources.yml"
    return
  fi

  for enabled_cleaner in $enabled_cleaners; do
    if [ ! -d "${cleaners_folder}/${enabled_cleaner}" ]; then
        echo "Cleaner folder ${cleaners_folder}/${enabled_cleaner} does not exist. Skipping."
        continue
    fi
    for cleaner_file in $(find "${cleaners_folder}/${enabled_cleaner}" -type f -name "cleaner.sh" | sort); do
      echo "Running cleaner script: ${cleaner_file}"
      source "${cleaner_file}" "${TMPDIR}" "${DATA_GENERATOR_DIR}"
    done
  done
}

# Example usage:
# ontology_update "input_ontology.ttl" "output_ontology.ttl"
