
# Define ANSI color codes
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NO_COLOR='\033[0m'


# Function to print messages with appropriate color
print_message() {
    local type=${1}
    local message=${2}
    case "${type}" in
        info) echo -e "${CYAN}[*] ${message}${NO_COLOR}" ;;
        success) echo -e "${GREEN}[+] ${message}${NO_COLOR}" ;;
        error) echo -e "${RED}[-] ${message}${NO_COLOR}" ;;
    esac
}

# Function to clean up temporary files older than 1 day
cleanup_old_files() {
    print_message info "Cleaning files older than 1 day in ${temp_directory}"
    find "${temp_directory}" -type f -name "security_ontology_ttl_*" -mtime +1 -delete 2>/dev/null || true
}

