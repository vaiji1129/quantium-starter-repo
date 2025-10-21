#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Print commands as they are executed (useful for debugging)
set -x

echo "Starting test suite execution..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please create a virtual environment first using: python -m venv venv"
    exit 1
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || {
    echo "Failed to activate virtual environment"
    exit 1
}

# Verify pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "pytest is not installed. Installing test dependencies..."
    pip install pytest
fi

# Run the test suite
echo "Running test suite..."
pytest tests/ -v --tb=short || TEST_RESULT=$?

# Store the exit code
if [ -z "$TEST_RESULT" ]; then
    TEST_RESULT=0
fi

# Deactivate virtual environment
deactivate

# Report results
if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ All tests passed successfully!"
    exit 0
else
    echo "❌ Some tests failed. Please review the output above."
    exit 1
fi