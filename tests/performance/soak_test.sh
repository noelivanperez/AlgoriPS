#!/bin/bash
# Run a soak test with Locust for 4 hours and capture CPU/memory usage
set -e
OUTPUT_DIR="$(dirname "$0")"
REPORT="$OUTPUT_DIR/soak_report"
DURATION="4h"

# start system monitoring in background
mpstat 5 > "$REPORT.cpu" &
MPSTAT_PID=$!

locust -f "$OUTPUT_DIR/locustfile.py" --headless -u 60 -r 5 -t $DURATION --csv="$REPORT" 

kill $MPSTAT_PID
