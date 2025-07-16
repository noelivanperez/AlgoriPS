#!/bin/bash
# Basic penetration test using Nikto against local endpoint
set -e
OUTPUT="$(dirname "$0")/security_scan.txt"
nikto -host http://localhost:8000 -o "$OUTPUT"
echo "Results saved to $OUTPUT"
