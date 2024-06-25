#!/bin/bash

PARALLEL_JOBS="${PARALLEL_JOBS:=3}"

run_test() {
    ANSIBLE_RETRY_FILES_ENABLED=false ansible-test integration $1
}

cleanup() {
    if [[ -z "$CLEANUP_DONE" ]]; then
        make delete-e2e-firewall
        CLEANUP_DONE=1
    fi
}

# Set trap to ensure cleanup is run on script exit
trap cleanup EXIT

# Create integration_yaml
make create-integration-config
make create-e2e-firewall

export -f run_test

# Run tests in parallel
parallel -j $PARALLEL_JOBS --group --keep-order run_test ::: $(ls tests/integration/targets)
TEST_EXIT_CODE=$?


cleanup

exit $TEST_EXIT_CODE
