#!/bin/bash

# this script gather rmlmapper from github, rmlmapper....jar and the link are gitgnored, hence not commited (because too big)

# sometimes github refuses download and then send an html page, I put a sha256 to break the pipeline in this case

#TODO => faire un seul rml mapper avec une variable 

RML=rmlmapper-7.3.1-r374-all.jar
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 15.5; rv:140.0) Gecko/20100101 Firefox/140.0"
RML_URL="https://github.com/RMLio/rmlmapper-java/releases/download/v7.3.1"
SHA256_FILE="rmlmapper.sha256"

# Parse command line options
while getopts "u:s:" opt; do
    case $opt in
        u)
            RML_URL="$OPTARG"
            ;;
        s)
            SHA256_FILE="$OPTARG"
            ;;
        \?)
            echo "Usage: $0 [-u custom_url] [-s sha256_file]"
            exit 1
            ;;
    esac
done

curl -L "${RML_URL}/${RML}" -o "${RML}" --user-agent "${UA}"

#sha256sum -c "${SHA256_FILE}"

ln -s "${RML}" "rmlmapper.jar"
