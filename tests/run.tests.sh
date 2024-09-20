#!/bin/bash

set -e

export PYTHONPATH=..

run_tests() {
    echo "Running tests..."
    python -m unittest discover -v
}

if run_tests; then
    echo "All tests passed!"
else
    echo "Some tests failed. Check the output above."
fi

echo "Press any key to exit..."
read -n 1 -s
