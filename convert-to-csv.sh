#!/usr/bin/env bash
#
# Convert Table E1 from ascii to CSV format.

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
    echo 'Usage: '$0'

    Convert Table E1 from ascii to CSV format.

    '
    exit
fi

#cd "$(dirname "$0")"

main() {
    exec tail -c +2  data/table-e1.ascii | awk '{
    for (i=1; i<=NF-1; i++) {if ($i ~ /--/) {
        printf(",")
    } else {
    printf("%s,",$i)
    }};
    if ($NF ~ /--/) {print ""} else {print $NF}}'
}

main "$@"
