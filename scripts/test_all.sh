#!/bin/bash

PARALLEL_JOBS="${PARALLEL_JOBS:=3}"

run_test() {
  make TEST_ARGS="$1" test
}

export -f run_test

parallel -j $PARALLEL_JOBS --group --keep-order run_test ::: $(ls tests/integration/targets)