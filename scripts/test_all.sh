#!/bin/bash

PARALLEL_JOBS="${PARALLEL_JOBS:=3}"

run_test() {
    ansible-test integration $(TEST_ARGS)
}

cleanup() {
    make delete-e2e-firewall
}

# Set trap to ensure cleanup is run on script exit
trap cleanup EXIT

make create-integration-config
make create-e2e-firewall

export -f run_test

parallel -j $PARALLEL_JOBS --group --keep-order run_test ::: $(ls tests/integration/targets)
TEST_EXIT_CODE=$?

cleanup

exit $TEST_EXIT_CODE
