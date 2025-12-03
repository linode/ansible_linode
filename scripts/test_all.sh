#!/bin/bash

PARALLEL_JOBS="${PARALLEL_JOBS:=3}"

run_test() {
    ansible-test integration -vvv $1
}

cleanup() {
    if [[ -z "$CLEANUP_DONE" ]]; then
        make delete-e2e-firewall
        CLEANUP_DONE=1
    fi
}

trap cleanup EXIT

CLEANUP_DONE=0

make create-integration-config || exit 1
make create-e2e-firewall || exit 1

export -f run_test

parallel -j $PARALLEL_JOBS --group --keep-order --retries 3 run_test ::: $(ls tests/integration/targets)
TEST_EXIT_CODE=$?


exit $TEST_EXIT_CODE
