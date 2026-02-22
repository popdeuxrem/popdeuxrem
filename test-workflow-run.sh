#!/bin/bash

# Test workflow steps
echo "=== Workflow Test ==="
echo "1. Checking out repository"
pwd

echo "2. Setting up Python 3.12"
python3 --version

echo "3. Installing dependencies"
pip install -r requirements.txt

echo "4. Running quantum_build.sh"
./scripts/quantum_build.sh

echo "=== Workflow Test Complete ==="
