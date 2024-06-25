#!/bin/bash

PARALLEL_JOBS="${PARALLEL_JOBS:=3}"

run_test() {
    ANSIBLE_RETRY_FILES_ENABLED=false ansible-test integration $(TEST_ARGS)
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
if ! make create-integration-config; then
    echo "Failed to create integration config..."
    exit 1
fi

if ! make create-e2e-firewall; then
    echo "Failed to create e2e firewall..."
    exit 1
fi

export -f run_test

# Run tests in parallel
if ! parallel -j $PARALLEL_JOBS --group --keep-order run_test ::: $(ls tests/integration/targets); then
    TEST_EXIT_CODE=$?
else
    TEST_EXIT_CODE=0
fi

cleanup

exit $TEST_EXIT_CODE
