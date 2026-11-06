set -euo pipefail

CONTROL_FILE="sbom.json"
OUTPUT_FILE="${TMPDIR}/sbom.json"

syft scan plot_example.py --output cyclonedx-json | jq '. | del (.metadata.timestamp, .serialNumber)'  > "${OUTPUT_FILE}"

diff_output=$(diff "${CONTROL_FILE}" "${OUTPUT_FILE}" || true)
if [ -z "$diff_output" ]; then
    echo -e "\033[0;32m[+] SBOM test passed: Generated SBOM matches the control file.\033[0m"
else
    echo -e "\033[0;31m[-] SBOM test failed: Generated SBOM does not match the control file.\033[0m"
    echo -e "\033[0;33m[!] Differences:\033[0m"
    echo -e "\033[0;33m$diff_output\033[0m"
    exit 1
fi

