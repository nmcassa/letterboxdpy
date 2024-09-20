#!/bin/bash

set -e

run_tests() {
    echo "Running tests..."
    python -m unittest discover -v
}

if run_tests; then
    echo "All tests passed!"
else
    echo "Some tests failed. Check the output above."
fi