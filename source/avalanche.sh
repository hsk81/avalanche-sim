#!/usr/bin/env bash
###############################################################################
SIM_PATH_SCRIPT=$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)
###############################################################################

for _ in $(seq "${1-1}") ; do
   >&2 echo -n "." ; "${SIM_PATH_SCRIPT}/avalanche.py" "${@:2}" ;
done

###############################################################################
###############################################################################
