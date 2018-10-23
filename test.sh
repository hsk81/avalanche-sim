#!/usr/bin/env bash
###############################################################################
SIM_TEST_SCRIPT=$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)
###############################################################################

function _shunit2 {
    local shunit2_system ;
    shunit2_system="$(command -v shunit2)" ;
    if [[ -x "$shunit2_system" ]] ; then
        printf '%s' "$shunit2_system" ; return
    fi
    local shunit2_travis ;
    shunit2_travis="$SIM_TEST_SCRIPT/shunit2-2.1.8/shunit2" ;
    if [[ -x "$shunit2_travis" ]] ; then
        printf '%s' "$shunit2_travis" ; return
    fi
    exit 1 ;
}

function run {
    if [[ -z "$_SHUNIT2" ]] ; then
        _SHUNIT2="$(_shunit2)" ;
    fi
    "$_SHUNIT2" "$1" ;
}

###############################################################################

for script in $(find "$SIM_TEST_SCRIPT/${1}" -name '*.test.sh' | sort) ; do
    run "$script" ;
done

###############################################################################
###############################################################################
